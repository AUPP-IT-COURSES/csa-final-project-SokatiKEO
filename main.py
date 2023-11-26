from tkinter import *
import pandas as pd
import random
from tkinter import messagebox as mb
import csv

# Global variables
flip_counter = 1
canvas_2 = None
q_entry = []
a_entry = []
current_card = {}
to_learn = {}

# Load data from CSV file


# Set up the main window
BACKGROUND_COLOR = "#E0F4FF"
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.geometry("1170x900")

# Load images for flashcards
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
study_buddy_img = PhotoImage(file="images/Study_Buddy.png")
check_image = PhotoImage(file="images/right.png")
flip_image = PhotoImage(file="images/flip.png")
cross_image = PhotoImage(file="images/wrong.png")
start_img = PhotoImage(file="images/start.png")
create_img = PhotoImage(file="images/create.png")
about_img = PhotoImage(file="images/about.png")
quit_img = PhotoImage(file="images/quit.png")
back_img = PhotoImage(file="images/back.png")
add_img = PhotoImage(file="images/add.png")

# Functions for managing flashcards
def check_data():
    global to_learn
    try:
        data = pd.read_csv("data/words_to_learn.csv")
        to_learn = data.to_dict(orient="records")
    except FileNotFoundError:
        mb.showerror("No data found", "No data found")
        
        
def next_card():
    global current_card, flip_timer, canvas_2
    window.after_cancel(flip_timer)
    try:
        current_card = random.choice(to_learn)
        canvas_2.itemconfig(card_title, text="Question", fill="black")
        canvas_2.itemconfig(card_word, text=current_card["Question"], fill="black")
        canvas_2.itemconfig(card_background, image=card_front_img)
    except IndexError:
        mb.showinfo("Out of questions", "Congratulations! You have learned all of the questions!")
        back()


def flip_button_func():
    global canvas_2, flip_counter
    flip_states = {
        0: {"title": "Question", "word_fill": "black", "background_image": card_front_img},
        1: {"title": "Answer", "word_fill": "white", "background_image": card_back_img}
    }
    current_state = flip_states[flip_counter % 2]

    canvas_2.itemconfig(card_title, text=current_state["title"], fill=current_state["word_fill"])
    canvas_2.itemconfig(card_word, text=current_card[current_state["title"]], fill=current_state["word_fill"])
    canvas_2.itemconfig(card_background, image=current_state["background_image"])

    flip_counter += 1


def is_known():
    global to_learn
    to_learn.remove(current_card)
    print(len(to_learn))

    # Update the existing CSV file
    csv_file_path = 'data/words_to_learn.csv'
    data = pd.read_csv(csv_file_path)
    data = data[data['Question'] != current_card['Question']]
    data.to_csv(csv_file_path, index=False)
    next_card()


def add():
    global to_learn
    empty_q = [q.get() for q in q_entry if len(q.get()) != 0]
    empty_a = [a.get() for a in a_entry if len(a.get()) != 0]

    if not len(empty_q) == len(empty_a):
        mb.showerror("Uneven question and answer", "Please input all the questions and answers")
    else:
        q_and_a = {k: v for (k, v) in zip(empty_q, empty_a)}
        df = pd.DataFrame(list(q_and_a.items()), columns=['Question', 'Answer'])
        # Update the existing CSV file
        csv_file_path = 'data/words_to_learn.csv'
        try:
            existing_df = pd.read_csv(csv_file_path)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.to_csv(csv_file_path, index=False)

            # Update the to_learn variable
            to_learn = updated_df.to_dict(orient="records")
        except FileNotFoundError:
            with open('data/words_to_learn.csv', 'w', newline='') as csvfile:
                fieldnames = ['Question', 'Answer']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for key in q_and_a:
                    writer.writerow({'Question': key, 'Answer': q_and_a[key]})
                data = pd.read_csv("data/words_to_learn.csv")
                to_learn = data.to_dict(orient="records")
        mb.showinfo("Question updated", "Questions and Answers have been updated successfully")
        for entry in q_entry + a_entry:
            entry.delete(0, END)
            
            
# Functions and setup for the second stage (back side of flashcards)
def init_start():
    global card_background, card_title, card_word, canvas_2, back_frame
    back_frame = Frame(window, bg=BACKGROUND_COLOR)
    back_frame.grid(row=0, column=0, columnspan=3)
    canvas_2 = Canvas(back_frame, width=1066, height=701)

    card_background = canvas_2.create_image(533, 350, image=card_front_img)
    card_title = canvas_2.create_text(533, 150, text="", font=("Ariel", 40, "italic"))
    card_word = canvas_2.create_text(533, 350, text="", font=("Ariel", 30, "bold"))
    canvas_2.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas_2.grid(row=0, column=0, columnspan=3)

    unknown_button = Button(back_frame, image=cross_image, highlightthickness=0, command=next_card)
    unknown_button.grid(row=1, column=0)

    flip_button = Button(back_frame, image=flip_image, highlightthickness=0, command=flip_button_func)
    flip_button.grid(row=1, column=2)

    known_button = Button(back_frame, image=check_image, highlightthickness=0, command=is_known)
    known_button.grid(row=1, column=1)

    back_button = Button(image=back_img, highlightthickness=0, command=back)
    back_button.place(x=0, y=0)

    next_card()


def init_create():
    global card_background, card_title, card_word, canvas_2, back_frame, add_button
    back_frame = Frame(window, bg=BACKGROUND_COLOR)
    back_frame.grid(row=0, column=0, columnspan=3)
    canvas_3 = Canvas(back_frame, width=1066, height=701)
    card_background = canvas_3.create_image(533, 350, image=card_front_img)

    canvas_3.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas_3.grid(row=0, column=0, columnspan=3)

    add_button = Button(image=add_img, highlightthickness=0, command=add)
    add_button.place(x=400, y= 720)

    back_button = Button(back_frame, image=back_img, highlightthickness=0, command=back)
    back_button.place(x=0, y=0)
    for i in range(5):
        q_text_box = Entry()  # create a new textbox
        q_text_box.place(x=160, y=75+(i*100), width=300, height=40)
        q_entry.append(q_text_box)

        a_text_box = Entry()  # create a new textbox
        a_text_box.place(x=660, y=75+(i*100), width=300, height=40)
        a_entry.append(a_text_box)

        q_label = Label(back_frame, text=f"Q{i+1}", font=("Ariel", 40, "italic"), bg="white")
        q_label.place(x=75, y=65+(i*100))

        a_label = Label(back_frame, text=f"A{i+1}", font=("Ariel", 40, "italic"), bg="white")
        a_label.place(x=575, y=65+(i*100))


# Functions for initializing the application
def front_page_start():
    global front_frame, card_background, study_buddy_logo, card_title, card_word
    front_frame = Frame(window, bg=BACKGROUND_COLOR)
    front_frame.grid(row=0, column=0, columnspan=3)
    canvas = Canvas(front_frame, width=1066, height=701)

    start_button = Button(front_frame, image=start_img, highlightthickness=0, command=start)
    start_button.place(x=480, y=250)

    create_button = Button(front_frame, image=create_img, highlightthickness=0, command=create)
    create_button.place(x=480, y=350)

    about_button = Button(front_frame, image=about_img, highlightthickness=0)
    about_button.place(x=480, y=450)

    quit_button = Button(front_frame, image=quit_img, highlightthickness=0, command=window.destroy)
    quit_button.place(x=480, y=550)
    card_background = canvas.create_image(533, 350, image=card_front_img)
    study_buddy_logo = canvas.create_image(533, 150, image=study_buddy_img)
    card_title = canvas.create_text(533, 150, text="", font=("Ariel", 40, "italic"))
    card_word = canvas.create_text(533, 350, text="", font=("Ariel", 60, "bold"))
    canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=3)


def start():
    check_data()
    front_frame.destroy()
    try:
        random.choice(to_learn)
    except IndexError:
        mb.showerror("Error", "No cards to study")
        front_page_start()
    else:
        init_start()


def create():
    front_frame.destroy()
    init_create()


def back():
    global back_frame, add_button
    try:
        add_button.destroy()
    except NameError:
        back_frame.destroy()
        front_page_start()
    else:
        back_frame.destroy()
        front_page_start()

front_page_start()
window.mainloop()