import pandas as pd
from tkinter import messagebox as mb


class FlashcardBrain:
    def __init__(self):
        self.flip_counter = 1
        self.canvas_2 = None
        self.q_entry = []
        self.a_entry = []
        self.current_card = {}
        self.to_learn = {}

    def check_data(self):
        try:
            self.data = pd.read_csv("data/questions_and_answers.csv")
            self.to_learn = self.data.to_dict(orient="records")
        except FileNotFoundError:
            mb.showerror("No data found", "No data found")
            return False
        else:
            return True
        


    def is_known(self):
        self.to_learn.remove(self.current_card)

        # Update the existing CSV file
        csv_file_path = 'data/questions_and_answers.csv'
        data = pd.read_csv(csv_file_path)
        data = data[data['Question'] != self.current_card['Question']]
        data.to_csv(csv_file_path, index=False)

