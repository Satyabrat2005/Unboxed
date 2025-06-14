from flask import Flask, render_template, request, redirect, url_for, session
from quiz_engine import QuizEngine
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load questions
quiz = QuizEngine('mock_tests/jee_paper1.csv')

# 3-hour timer logic
def get_time_left():
    start_time = session.get('start_time')
    if start_time:
        elapsed = int(time.time()) - int(start_time)
        return max(0, 3 * 60 * 60 - elapsed)
    return 3 * 60 * 60

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        session['start_time'] = int(time.time())
        quiz.score = 0  # Reset score
        return redirect(url_for('quiz_question', qid=0))
    return render_template('welcome.html')

@app.route('/quiz/<int:qid>', methods=['GET', 'POST'])
def quiz_question(qid):
    if get_time_left() <= 0:
        return redirect(url_for('result'))

    if request.method == 'POST':
        selected_option = request.form.get('option')
        if quiz.check_answer(qid, selected_option):
            quiz.score += 1

        if qid + 1 < quiz.total_questions:
            return redirect(url_for('quiz_question', qid=qid + 1))
        else:
            return redirect(url_for('result'))

    question_data = quiz.get_question(qid)
    return render_template(
        'quiz.html',
        qid=qid,
        question=question_data,
        total=quiz.total_questions,
        username=session.get('username'),
        time_left=get_time_left()
    )

@app.route('/result')
def result():
    username = session.get('username', 'Guest')
    return render_template('result.html', name=username, score=quiz.score, total=quiz.total_questions)

if __name__ == '__main__':
    app.run(debug=True)
