from tkinter import *
from pandas import *
from random import *



BACKGROUND_COLOR = "#B1DDC6"
timer = None
french_word = ""
english_word = ""

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)


# ------------------obtain data--------------------#
try:
    csv_data = read_csv("data/words_to_learn.csv")
    data = csv_data.to_dict(orient="records")
except FileNotFoundError:
    csv_data = read_csv("data/french_words.csv")
    data = csv_data.to_dict(orient="records")



# ----------------generate random word--------------------#
random_list = {}


def generate_word():
    global french_word, english_word, random_list
    random_list = choice(data)

    french_word = random_list['French']
    english_word = random_list['English']


# ---------------------------sorting words=-------------------#
data_to_sort = [_ for _ in data]


def sort():
    global random_list
    generate_word()
    try:
        data_to_sort.remove(random_list)
    except ValueError:
        update_word()
    sorted_data = DataFrame(data_to_sort)
    sorted_data.to_csv("data/words_to_learn.csv", index=False)
    # print(random_list)
    print(len(data_to_sort))
    update_word()


# ----------------update GUI word --------------------#
def translate():
    canvas.itemconfig(word, text=english_word)
    canvas.itemconfig(language, text="English")
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(word, fill="white")
    canvas.itemconfig(language, fill="white")


def update_canvas():
    canvas.itemconfig(canvas_image, image=front_card)
    canvas.itemconfig(word, fill="black")
    canvas.itemconfig(language, fill="black")


def update_word():
    global timer
    update_canvas()
    generate_word()
    canvas.itemconfig(word, text=french_word)
    canvas.itemconfig(language, text="French")
    timer = window.after(2000, translate)


# -----------canvas--------------#
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_card)
canvas.grid(column=0, columnspan=2, row=0)

# -------------canvas text-------------- #
language = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

# -------------buttons-------------------#

wrong_img = PhotoImage(file="images/wrong.png")
wrong = Button(image=wrong_img, highlightthickness=0, command=update_word)
wrong.grid(row=1, column=0)
wrong.config(bg=BACKGROUND_COLOR)

right_img = PhotoImage(file="images/right.png")
right = Button(image=right_img, highlightthickness=0, command=sort)
right.grid(row=1, column=1)
right.config(bg=BACKGROUND_COLOR)

window.mainloop()
