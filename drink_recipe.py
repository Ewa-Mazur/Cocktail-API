import tkinter as tk
from PIL import ImageTk, Image
import requests
import json
from io import BytesIO


def drink_preparation(selected_drink, content):

    drink_content = content['drinks'][0]
    img_url = drink_content["strDrinkThumb"]+"/preview"
    required_ing = []
    
    for i in range(1, 16):
       if (drink_content["strIngredient"+str(i)]) is not None:
           required_ing.append(drink_content["strIngredient"+str(i)])

    required_qty = []

    for i in range(1, len(required_ing)+1):
        required_qty.append(drink_content["strMeasure"+str(i)])

    root = tk.Tk()
    root.geometry("700x600")
    root.title('Drink preparation')
    root.configure(bg='white')

    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    tk.Label(root, text=selected_drink, font='Helvetica 14 bold', bg='white').pack()

    tk.Label(root, text="\nList of required ingredients:", font='Helvetica 10 bold', bg='white').pack()

    for i in range(0, (len(required_ing))):
        tk.Label(root, bg='white', text=str(required_ing[i]) + " - " + str(required_qty[i])).pack()

    tk.Label(root, text="\nInstructions:", font='Helvetica 10 bold', bg='white').pack()

    instructions = drink_content["strInstructions"]

    """
    Workaround for long text instruction, dividing the text after ~100 characters
    """
    if len(instructions) > 100:
        for i in range(100, 600, 100):
            index_to_div = instructions.find(" ", i, i+30)
            if index_to_div != -1:
               instructions = instructions[:index_to_div]+"\n"+instructions[index_to_div:]

    tk.Label(root, text=instructions, bg='white').pack()

    panel = tk.Label(root, image=img, height=100, bg='white')
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()


def drink_recipe(selected_drink):
    r = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s="+selected_drink)
    try:
        content = r.json()
    except json.decoder.JSONDecodeError:
        print("Incorrect format")
    else:
        drink_preparation(selected_drink, content)
