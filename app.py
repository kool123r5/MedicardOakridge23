import tkinter as tk
import customtkinter as ctk
import PIL
from firebase_admin import credentials, db
import firebase_admin


username = "ashwin"
cred = credentials.Certificate('api_creds.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://oakridgecodefest2023-default-rtdb.firebaseio.com/'})
ref = db.reference('/')
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MediCard")
        self.geometry("400x700")
        self.resizable(False, False)

        homepage = Homepage(self)
        homepage.pack()
        
        

        
        
        

class Homepage(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        
        self.company_name = ctk.CTkLabel(self, text= "MEDICARD")
        self.company_name.pack()

        li = []
        
        data = ref.get()
        for key, value in data.items():
            if(key == username):
                li = value
                
        
        
        

        self.text = ""

        for i in li:
            self.text = self.text + f"\n {i} : {li[i]}"

        self.cardBtn = ctk.CTkButton(self, text = self.text)
        self.cardBtn.pack()

        

       

        
    
    
        

        
        

    



root = Window()
root.mainloop()