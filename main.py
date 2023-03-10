import requests
from tkinter import *
from PIL import ImageTk, Image
from io import BytesIO
import drink_by_ingredient
import drink_by_name


def menu():
    root = Tk()
    root.title('Cocktail API')
    root.geometry('350x500')
    root.configure(bg='white')

    message = "This project is based on TheCocktailDB open database.\nThis is a non-commercial project" \
              " made with tkinter GUI\n to improve my skills.\n\nHope you enjoy it!"
    
    Label(root, bg='white', text="\nHello, welcome to the Cocktail API\n", font='Helvetica 12 bold', anchor='n').pack()
    
    Label(root, bg='white', text=message, anchor='n').pack()
    
    Label(root, bg='white', text="\n\nWhat would you like to do?\n", anchor='n').pack()

    Button(root, text="Search for drink recipe by ingredients", width=40, anchor='n',
           command=lambda: [root.destroy(), drink_by_ingredient.drink_by_ingredient()]).pack()
    
    Label(root, bg='white', text="").pack()
    
    Button(root, text="Search for drink recipe by its type", width=40, anchor='n',
           command=lambda: [root.destroy(), drink_by_name.drink_by_name()]).pack()

    img_url = "https://www.thecocktaildb.com/images/media/drink/qyr51e1504888618.jpg/preview"

    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    panel = Label(root, image=img, height=100, bg='white')
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()


menu()
