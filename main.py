import random
from tkinter import *
import pandas
import os

FilE1 = "words.csv"
FILE2 = "word_to_learn.csv"


current_pair = {}
BACKGROUND_COLOR = "#B1DDC6"

# Read CSV file and create a list of dictionaries
try:
    data = pandas.read_csv(FILE2)
except FileNotFoundError:
    data = pandas.read_csv(FilE1)
    result_list = data.to_dict(orient="records")
else:
    result_list = data.to_dict(orient="records")


def flip_card():
    global current_pair
    canvas.itemconfig(card_background, image=card_back_img)
    new_word_kr = current_pair["Korean"]
    canvas.itemconfig(card_title, text="Korean", fill="White")
    canvas.itemconfig(card_word, text=new_word_kr, fill="White")


def back_card(button_value):
    global current_pair, fill_timer
    if button_value == 1:
        result_list.remove(current_pair)
    else:
        write_header = not os.path.exists(FILE2)
        with open(FILE2, "a", newline="") as f:
            pandas.DataFrame([current_pair]).to_csv(f, header=write_header, index=False)

    random_word_en()
    window.after_cancel(fill_timer)
    new_word_en = current_pair["English"]
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=new_word_en, fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    fill_timer = window.after(3000, flip_card)
    # current_pair = None


def random_word_en():
    global current_pair
    current_pair = random.choice(result_list)
    new_word_en = current_pair["English"]
    canvas.itemconfig(card_title, text="English")
    canvas.itemconfig(card_word, text=new_word_en)


# U#I setup


window = Tk()
window.title("Flash Card")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
fill_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img, tags="img")
card_title = canvas.create_text(400, 158, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))  # 태그 생성해서 바꿀 수 있게
canvas.grid(column=0, row=0, columnspan=2)

button_ok_img = PhotoImage(file="./images/right.png")
button_ok = Button(window, image=button_ok_img, bd=0, highlightthickness=0, command=lambda: back_card(1))
button_ok.grid(column=1, row=1)

button_no_img = PhotoImage(file="./images/wrong.png")
button_no = Button(window, image=button_no_img, bd=0, highlightthickness=0, command=lambda: back_card(2))
button_no.grid(column=0, row=1)

random_word_en()
window.mainloop()
