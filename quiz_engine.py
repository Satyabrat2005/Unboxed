import pandas as pd
import random

class QuizEngine:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.score = 0
        self.total_questions = len(self.df)
        self.shuffle_questions()

    def shuffle_questions(self):
        self.df = self.df.sample(frac=1).reset_index(drop=True)

    def get_question(self, index):
        row = self.df.loc[index]

        # 🧠 Build options from OptionA–D
        options = []
        for opt in ['OptionA', 'OptionB', 'OptionC', 'OptionD']:
            if pd.notna(row.get(opt)):
                options.append(str(row[opt]))

        random.shuffle(options)

        return {
            "question": row['Question'],
            "options": options,
            "answer": row['CorrectOptions'].split(',')[0].strip()  # takes first correct answer
        }

    def check_answer(self, index, user_choice):
        # ✅ Compare against the first correct answer in CorrectOptions
        correct_answer = self.df.loc[index, 'CorrectOptions'].split(',')[0].strip().lower()
        return str(user_choice).strip().lower() == correct_answer
