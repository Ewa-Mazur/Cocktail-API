import requests
import json
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import collections
import drink_recipe


def ingredients_selection(content, ingredients_list, message=""):
    root = Tk()
    root.title('Ingredients')
    root.geometry('300x500')
    root.configure(bg='white')
    if message == "":
        message = "\nChoose the ingredients from\n which you want to make a drink"

    Label(root, bg='white', text=message, anchor='n').pack()

    Button(root, text="Confirm", anchor='n',
           command=lambda: [root.destroy(), drinks_proposal(content, selected_ing)]).pack()

    # mask
    Label(height=2, bg='white').pack()

    text = ScrolledText(root, width=20, height=300, background="white")
    text.pack()
    text.configure(borderwidth=0)
                   
    selected_ing = []
    for x in range(len(ingredients_list)):
        l = Checkbutton(root, bg='white', text=ingredients_list[x], variable=ingredients_list[x],
                        command=lambda x=ingredients_list[x]: selected_ing.append(x))
        l.pack(anchor='w')
        text.window_create('end', window=l)
        text.insert('end', '\n')

    root.mainloop()


def ingredients_choice(content, message=""):
    ingredients = content['drinks']
    ingredients_list = []
    for i in range(0, len(ingredients)):
        ingredients_list.append((ingredients[i].get('strIngredient1')))

    ingredients_list = sorted(ingredients_list)
    ingredients_selection(content, ingredients_list, message)


def drinks_proposal(content, selected_ing):
    possible_drinks = []
    drinks_to_delete = []
    
    """
    checkbutton appends ingredients again when they unclicked, workaround for removed ingredients
    """
    
    for i in selected_ing:
        counter = selected_ing.count(i)
        if counter % 2 == 0:
            drinks_to_delete.append(i)

    for i in drinks_to_delete:
        selected_ing.remove(i)

    """
    removed duplicated after checkbutton was checked,unchecked and checked again to minimalize requests
    """
    selected_ing = list(set(selected_ing))

    for i in range(0, len(selected_ing)):
        r = requests.get("https://www.thecocktaildb.com/api/json/v1/1/filter.php?i="+str(selected_ing[i]))
        drink = r.json()
        drink = drink['drinks']

        for j in range(0, len(drink)):
            possible_drinks.append(drink[j]['strDrink'])
    """
    finding common drink based on given ingredients
    """
    
    final_drink_list = [item for item, count in collections.Counter(possible_drinks).items()
                        if count == len(selected_ing)]

    if len(final_drink_list) != 0:
        drink_choosing(content, final_drink_list)
    else:
        message = "Sorry, no drinks matching selected ingredients,\n try to narrow down your list of ingredients\n"
        ingredients_choice(content, message)
    

def drink_choosing(content, final_drink_list):
    root2 = Tk()
    root2.title('Choose the drink!')
    root2.geometry('300x500')
    root2.configure(bg='white')

    Label(root2, bg='white', text="\nGreat, now choose the drink of your interest!\n", anchor='n').pack()
    Button(root2, text="Confirm", anchor='n', command=lambda: [root2.destroy()]).pack()
    # mask
    Label(height=2, bg='white').pack()
        
    text = ScrolledText(root2, width=30, height=300, background="white")
    text.pack()
    text.configure(borderwidth=0)
               
    var = StringVar(root2, "Not_chosen")
        
    for x in range(len(final_drink_list)):
        l = Radiobutton(root2, bg='white', text=final_drink_list[x], variable=var, value=final_drink_list[x])
        l.pack(anchor='w')
        text.window_create('end', window=l)
        text.insert('end', '\n')
            
    root2.mainloop()
        
    selected_drink = str(var.get())

    if selected_drink == "Not_chosen":
        drink_choosing(content, final_drink_list)
    elif selected_drink != "Not_chosen":
        drink_recipe.drink_recipe(selected_drink)


def drink_by_ingredient():
    r = requests.get("https://www.thecocktaildb.com/api/json/v1/1/list.php?i=list")

    try:
        content = r.json()
    except json.decoder.JSONDecodeError:
        print("Incorrect format")
    else:
        ingredients_choice(content, message="")
