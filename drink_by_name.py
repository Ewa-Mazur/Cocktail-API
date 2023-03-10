import requests
import json
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import drink_by_ingredient


def drink_category(content):

    categories = content['drinks']
    categories_list = []
    for i in range(0, len(categories)):
        categories_list.append(categories[i].get("strCategory"))

    root = Tk()
    root.title('Drinks categories')
    root.geometry('300x500')
    root.configure(bg='white')

    Label(root, bg='white', text="\nChoose the type of the drink\n", anchor='n').pack()

    Button(root, text="Confirm", anchor='n', command=lambda: [root.destroy()]).pack()

    # mask
    Label(height=2, bg='white').pack()

    text = ScrolledText(root, width=20, height=300, background="white")
    text.pack()
    text.configure(borderwidth=0)
                   
    var = StringVar(root, "Not_chosen")
    
    for x in range(len(categories_list)):
        l = Radiobutton(root, bg='white', text=categories_list[x], variable=var, value=str(categories_list[x]))
        l.pack(anchor='w')
        text.window_create('end', window=l)
        text.insert('end', '\n')

    root.mainloop()
    selected_cat = str(var.get())

    if selected_cat != "Not_chosen":
        drink_list(content, selected_cat)
    elif selected_cat == "Not_chosen":
        drink_category(content)


def drink_list(content, selected_cat):

    r = requests.get("https://www.thecocktaildb.com/api/json/v1/1/filter.php?c="+str(selected_cat))
    drink_list = r.json()
    drink_list = drink_list["drinks"]

    final_drink_list = []

    for i in range(0, len(drink_list)):
        final_drink_list.append(drink_list[i]['strDrink'])

    drink_by_ingredient.drink_choosing(content, final_drink_list)


def drink_by_name():
    r = requests.get("https://www.thecocktaildb.com/api/json/v1/1/list.php?c=list")

    try:
        content = r.json()
    except json.decoder.JSONDecodeError:
        print("Incorrect format")
    else:
        drink_category(content)


    
