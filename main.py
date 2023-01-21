import tkinter
import customtkinter
import firebase_admin
from firebase_admin import credentials, db, auth

cred = credentials.Certificate('/Users/kushalb/Documents/VSCode/OakridgeHacks2023/admin.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://oakridgecodefest2023-default-rtdb.firebaseio.com/'
})

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

ref = db.reference('/')
# ref.child('John Deer').set({
#     'Image': 'no img right now',
#     'Name': 'Ashwin Ganapathy',
#     'Age': 16,
#     'Blood-type': 'B+',
#     'Height': '165cm',
#     'Allergies': 'Nuts',
#     'Phobias': 'Arachnophobia',
#     'Prior Vaccinations': 'COVID-19'
# })
customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("390x844")
def button_function():
    data = ref.get()
    print(data)
    for key, value in data.items():
        print(value['age'])

def button_function_two():
    auth.create_user(email=emailEntry.get(), password=passwordEntry.get())
    frame_2.tkraise()
    ref.child(f'{emailEntry.get().replace("@", "").replace(".", "")}_{nameEntry.get()}').set({
        'Image': 'no img right now',
        'Name': f'{nameEntry.get()}',
        'Age': f'{ageEntry.get()}',
        'Blood-type': f'{bloodEntry.get()}',
        'Height': f'{heightEntry.get()}',
        'Allergies': f'{allergyEntry.get()}',
        'Phobias': f'{phobiaEntry.get()}',
        'Prior Vaccinations': f'{vaxEntry.get()}'
    })

# Use CTkButton instead of tkinter Button
frame_2 = customtkinter.CTkFrame(master=app)
frame_2.place(relx=0.5, rely=0.5, anchor='center')
frame_1 = customtkinter.CTkFrame(master=app)
frame_1.place(relx=0.5, rely=0.5, anchor='center')
emailEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Email.")
emailEntry.pack(padx=30, pady=20)
passwordEntry = customtkinter.CTkEntry(master=frame_1, show="*", placeholder_text="Password.")
passwordEntry.pack(padx=30, pady=20)
nameEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Name.")
nameEntry.pack(padx=30, pady=20)
ageEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Age.")
ageEntry.pack(padx=30, pady=20)
heightEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Height (in cm).")
heightEntry.pack(padx=30, pady=20)
bloodEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Blood type.")
bloodEntry.pack(padx=30, pady=20)
allergyEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Allergies.")
allergyEntry.pack(padx=30, pady=20)
phobiaEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Phobias.")
phobiaEntry.pack(padx=30, pady=20)
vaxEntry = customtkinter.CTkEntry(master=frame_1, placeholder_text="Prior vaccinations.")
vaxEntry.pack(padx=30, pady=20)
button = customtkinter.CTkButton(master=frame_1, text="Sign Up.", command=button_function_two)
button.pack(padx=30, pady=20)
# Use CTkButton instead of tkinter Button
button = customtkinter.CTkButton(master=frame_2, text="CTkButton", command=button_function)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()
