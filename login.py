import tkinter
import customtkinter
import firebase_admin
from firebase_admin import credentials, db, auth
import json
import requests
cred = credentials.Certificate('/Users/kushalb/Documents/VSCode/OakridgeHacks2023/admin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oakridgecodefest2023-default-rtdb.firebaseio.com/'
})

customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("390x844")

def button_function():
    auth.create_user(email=emailEntry.get(), password=passwordEntry.get())

# Use CTkButton instead of tkinter Button
frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack()
emailEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Email.")
emailEntry.pack(anchor=tkinter.CENTER)
passwordEntry = customtkinter.CTkEntry(master=frame_1, show="*", placeholder_text="Password.")
passwordEntry.pack(anchor=tkinter.CENTER)
button = customtkinter.CTkButton(master=app, text="Sign Up.", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()