import tkinter
import customtkinter
import firebase_admin
from firebase_admin import credentials, db
cred = credentials.Certificate('/Users/kushalb/Documents/VSCode/OakridgeHacks2023/admin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oakridgecodefest2023-default-rtdb.firebaseio.com/'
})

ref = db.reference('/')
import json
with open("/Users/kushalb/Documents/VSCode/OakridgeHacks2023/book_info.json", "r") as f:
	file_contents = json.load(f)
ref.set(file_contents)
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("390x844")

def button_function():
    print("button pressed")

# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()