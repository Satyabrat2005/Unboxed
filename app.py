from flask import Flask, render_template, request, redirect, url_for, session
from quiz_engine import QuizEngine
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Load questions
quiz = QuizEngine('mock_tests/jee_paper1.csv')

# ⏱️ Timer helper function
def get_time_left():
    start_time = session.get('start_time')
    if start_time:
        elapsed = int(time.time()) - int(start_time)
        return max(0, 3 * 60 * 60 - elapsed)  # 3 hours
    return 3 * 60 * 60

# 🏠 Home Page
@app.route('/')
def home():
    return render_template('home.html')

# 📝 Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        session['registered_user'] = {'username': username, 'password': password}
        return redirect(url_for('login'))
    return render_template('register.html')

# 🔐 Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        reg_user = session.get('registered_user')

        if reg_user and reg_user['username'] == username and reg_user['password'] == password:
            session['username'] = username
            session['start_time'] = int(time.time())  # 🕒 Start timer here!
            quiz.score = 0  # Reset quiz score
            quiz.shuffle_questions()  # Optional: reshuffle on new login
            return redirect(url_for('dashboard'))
        else:
            return "❌ Invalid credentials", 401

    return render_template('login.html')

# 📊 Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

# ❓ Quiz per Question
@app.route('/quiz/<int:qid>', methods=['GET', 'POST'])
def quiz_question(qid):
    if 'username' not in session:
        return redirect(url_for('login'))

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

# 🧾 Result Page
@app.route('/result')
def result():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session.get('username', 'Guest')
    return render_template(
        'result.html',
        name=username,
        score=quiz.score,
        total=quiz.total_questions
    )

# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ▶️ Run the app
if __name__ == '__main__':
    app.run(debug=True)
