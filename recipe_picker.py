import tkinter as tk
from tkmacosx import Button
from PIL import ImageTk
import sqlite3
from numpy import random

BG_COLOR = "#3d6466"

def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def fetch_db():
    connection = sqlite3.connect("data/recipes.db")
    cursor = connection.cursor()

    # fetch all table names
    cursor.execute("SELECT * FROM sqlite_schema WHERE type='table'")
    all_tables = cursor.fetchall()

    idx = random.randint(0, len(all_tables)-1)

    # fetch ingredients
    table_name = all_tables[idx][1]
    cursor.execute("SELECT * FROM " + table_name + ";")
    table_records = cursor.fetchall()

    connection.close()
    return table_name, table_records

def pre_process(table_name, table_records):
    title = table_name[:-6]
    title = "".join([char if char.islower() else " " + char for char in title])

    ingredients = []
    # ingredients
    for i in table_records:
        name = i[1]
        qty = i[2]
        unit = i[3]
        ingredients.append(f"{qty} {unit} of {name}")
    return title, ingredients

def load_frame1():
    clear_widgets(frame2)
    frame1.tkraise()
    frame1.pack_propagate(False)
    # logo widget
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo.png")
    logo_widget = tk.Label(frame1, image=logo_img, bg=BG_COLOR)
    logo_widget.image = logo_img
    logo_widget.pack()

    # instructions widget
    tk.Label(
        frame1,
        text="ready for your random recipe?",
        bg=BG_COLOR,
        fg="white",
        font=("TkMenuFont", 14)
        ).pack()


    # button widget
    Button(
        frame1,
        text="SHUFFLE",
        font=("TkHeadingFont", 20),
        background="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda:load_frame2()
        ).pack(pady=20)

def load_frame2():
    clear_widgets(frame1)
    frame2.tkraise()

    table_name, table_records = fetch_db()
    title, ingredients = pre_process(table_name, table_records)

    # logo widget
    logo_img = ImageTk.PhotoImage(file="assets/RRecipe_logo_bottom.png")
    logo_widget = tk.Label(frame2, image=logo_img, bg=BG_COLOR)
    logo_widget.image = logo_img
    logo_widget.pack(pady=20)

    tk.Label(
        frame2,
        text=title,
        bg=BG_COLOR,
        fg="white",
        font=("TkHeadingFont", 20)
        ).pack(pady=25)
    
    for ingredient in ingredients:
        tk.Label(
            frame2,
            text=ingredient,
            bg="#28393a",
            fg="white",
            font=("TkMenuFont", 12)
            ).pack(fill="both")
        
    Button(
        frame2,
        text="BACK",
        font=("TkHeadingFont", 18),
        background="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda:load_frame1()
        ).pack(pady=20)


# initialize app
root = tk.Tk()
root.title("Recipe Picker")

root.eval("tk::PlaceWindow . center")

# place app in the center of the screen
# x = root.winfo_screenwidth()//2
# y = int(root.winfo_screenheight() * 0.1)
# root.geometry('500x600+' + str(x) + '+' + str(y))

# create a frame widget
frame1 = tk.Frame(root, width=500, height=600, bg=BG_COLOR)
frame2 = tk.Frame(root, bg=BG_COLOR)

for frame in (frame1, frame2):
    frame.grid(row=0, column=0, sticky="nesw")

load_frame1()


# run app
root.mainloop()