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

    def load_questions(self, csv_file):
        """Reloads questions from a different test (CSV file)."""
        self.df = pd.read_csv(csv_file)
        self.total_questions = len(self.df)
        self.score = 0
        self.shuffle_questions()

    def get_question(self, index):
        """Returns a dictionary with question, options, answer, and optional image."""
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
            "answer": row['CorrectOptions'].split(',')[0].strip(),  # first correct option only
            "image": row['Image'] if 'Image' in row and pd.notna(row['Image']) else None
        }

    def check_answer(self, index, user_choice):
        """Checks if user's answer matches the correct one."""
        correct_answer = self.df.loc[index, 'CorrectOptions'].split(',')[0].strip().lower()
        return str(user_choice).strip().lower() == correct_answer
