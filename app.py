import tkinter as tk
import customtkinter as ctk
import PIL
from firebase_admin import credentials, db, auth
import firebase_admin
import time

currentEmail = ''
cred = credentials.Certificate('api_creds.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://oakridgecodefest2023-default-rtdb.firebaseio.com/'})
ref = db.reference('/')
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MediCard")
        self.geometry("390x844")
        self.resizable(False, False)

        self.homepage = Homepage(self)
        self.homepage.grid(row = 0, column = 0, sticky = "NSEW")

        self.loginframe = LoginFrame(self)
        self.loginframe.grid(row = 0, column = 0, sticky = "NSEW")
        

class Homepage(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.currentEmail = ""

        self.company_name = ctk.CTkLabel(self, text= "MEDICARD")
        self.company_name.pack()
        self.cardBtn = tk.Button(self, text = "")
        self.cardBtn.pack()

        self.showcard()


    def showcard(self): 
        
        li = []
        print(self.currentEmail)
        self.curr_data = self.cardBtn.cget("text")
        data = ref.get()
        for key, value in data.items():
            if(key == self.currentEmail):
                li = value
          

        for i in li:
            self.curr_data = self.cardBtn.cget("text")
            self.new_text  = f"\n {i} : {li[i]}"
            self.final_text = self.curr_data + self.new_text
            self.cardBtn["text"] = self.final_text
            print(self.final_text)


        

class LoginFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.emailEntry = ctk.CTkEntry(master=self, placeholder_text="Email.")
        self.emailEntry.pack(padx=30, pady=20)
        self.passwordEntry = ctk.CTkEntry(master=self, show="*", placeholder_text="Password.")
        self.passwordEntry.pack(padx=30, pady=20)
        self.nameEntry = ctk.CTkEntry(master=self, placeholder_text="Name.")
        self.nameEntry.pack(padx=30, pady=20)
        self.ageEntry = ctk.CTkEntry(master=self, placeholder_text="Age.")
        self.ageEntry.pack(padx=30, pady=20)
        self.heightEntry = ctk.CTkEntry(master=self, placeholder_text="Height (in cm).")
        self.heightEntry.pack(padx=30, pady=20)
        self.bloodEntry = ctk.CTkEntry(master=self, placeholder_text="Blood type.")
        self.bloodEntry.pack(padx=30, pady=20)
        self.allergyEntry = ctk.CTkEntry(master=self, placeholder_text="Allergies.")
        self.allergyEntry.pack(padx=30, pady=20)
        self.phobiaEntry = ctk.CTkEntry(master=self, placeholder_text="Phobias.")
        self.phobiaEntry.pack(padx=30, pady=20)
        self.vaxEntry = ctk.CTkEntry(master=self, placeholder_text="Prior vaccinations.")
        self.vaxEntry.pack(padx=30, pady=20)
        self.weightEntry = ctk.CTkEntry(master=self, placeholder_text="Weight (in kg).")
        self.weightEntry.pack(padx=30, pady=20)
        self.button = ctk.CTkButton(master=self, text="Sign Up.", command=self.button_function_two)
        self.button.pack(padx=30, pady=20)  
    def button_function_two(self):
        auth.create_user(email=self.emailEntry.get(), password=self.passwordEntry.get())
        
        self.currentEmail = f'{self.emailEntry.get().replace("@", "").replace(".", "")}_{self.nameEntry.get()}'
        ref.child(f'{self.emailEntry.get().replace("@", "").replace(".", "")}_{self.nameEntry.get()}').set({
            'Image': 'no img right now',
            'Name': f'{self.nameEntry.get()}',
            'Age': f'{self.ageEntry.get()}',
            'Blood-type': f'{self.bloodEntry.get()}',
            'Height': f'{self.heightEntry.get()}',
            'Allergies': f'{self.allergyEntry.get()}',
            'Phobias': f'{self.phobiaEntry.get()}',
            'Prior Vaccinations': f'{self.vaxEntry.get()}',
            'Weight': f'{self.weightEntry.get()}'
        })
        self.container.homepage.tkraise()
        self.container.homepage.currentEmail = self.currentEmail
        self.container.homepage.showcard()



root = Window()
root.mainloop()
