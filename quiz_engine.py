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
        options = eval(row['Options']) if isinstance(row['Options'], str) else row['Options']
        random.shuffle(options)
        return {
            "question": row['Question'],
            "options": options,
            "answer": row['Answer']
        }

    def check_answer(self, index, user_choice):
        correct_answer = str(self.df.loc[index, 'Answer']).strip().lower()
        return str(user_choice).strip().lower() == correct_answer
