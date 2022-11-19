from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"


# use pandas to import csv data as a DataFrame
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

# create a list containing multiple dictionaries (one for each record.  two key/value pairs.  keys are column
# name.  value is word in that column. ex? {'French': 'partie', 'English': 'part'}
data_dict_list = data.to_dict(orient="records")

word_choice = {}


# ----------------------------- GENERATE WORDS --------------------------------------- #
def green_check():
    global data, data_dict_list
    data_dict_list.remove(word_choice)
    data = pandas.DataFrame(data_dict_list)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_french_word()


def new_french_word():
    global word_choice, flip_timer
    window.after_cancel(flip_timer)
    print(f"words left = {len(data_dict_list)}")
    word_choice = random.choice(data_dict_list)
    flashcard.itemconfigure(language, text="French", fill="black")
    flashcard.itemconfigure(word, text=word_choice["French"], fill="black")
    flashcard.itemconfig(card_image, image=card_front)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    flashcard.itemconfig(language, text="English", fill="white")
    flashcard.itemconfig(word, text=word_choice["English"], fill="white")
    flashcard.itemconfigure(card_image, image=card_back)

# create program window
window = Tk()
window.title("Flashy")
# window.minsize(width=800, height=526)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# set up flash card (canvas)
flashcard = Canvas()
flashcard.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
flashcard.grid(column=0, row=0, columnspan=2)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = flashcard.create_image(400, 263, image=card_front)
language = flashcard.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word_choice = random.choice(data_dict_list)
word = flashcard.create_text(400, 263, text=word_choice["French"], font=("Ariel", 60, "bold"))


# set up buttons
incorrect_button = Button()
incorrect_image = PhotoImage(file="images/wrong.png")
incorrect_button.config(image=incorrect_image, highlightthickness=0)
incorrect_button.grid(column=0, row=1)
incorrect_button["command"] = new_french_word
correct_button = Button()
correct_image = PhotoImage(file="images/right.png")
correct_button.config(image=correct_image, highlightthickness=0)
correct_button.grid(column=1, row=1)
correct_button["command"] = green_check



mainloop()