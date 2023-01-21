import tkinter as tk
import customtkinter as ctk
import PIL
from firebase_admin import credentials, db, auth
import firebase_admin
import time
from tkinter import ttk
from customtkinter import filedialog
import qrcode
import pytesseract
import cv2



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

        self.pfpImage = tk.PhotoImage(file = "pfp.png")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.homepage = Homepage(self)
        self.homepage.grid(row = 0, column = 0, sticky = "NSEW")

        self.maincard = Maincard(self)
        self.maincard.grid(row = 0, column = 0, sticky = "NSEW")

        self.editcard = Editcard(self)
        self.editcard.grid(row = 0, column = 0, sticky = "NSEW")
        
        self.ocr = OCR(self)
        self.ocr.grid(row = 0, column = 0, sticky = "NSEW")

        self.loginframe = LoginFrame(self)
        self.loginframe.grid(row = 0, column = 0, sticky = "NSEW")
        
class Maincard(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.times = 0
        self.currentEmail = ""
        self.container = container
        self.basic_info_label = tk.Label(self, text = "",bg='#1e6ca4',
    fg='#ffffff',
    bd=0,
    font=('calibri', 20, 'bold'))
        self.basic_info_label.pack()
        
        
    def showcard(self): 
        self.basic_info_label["text"] = ""
        self.curr_data = self.basic_info_label.cget("text")
        self.li = []
        self.curr_data = self.basic_info_label.cget("text")
        data = ref.get()
        for key, value in data.items():
            if(key == self.currentEmail):
                self.li = value

        for i in self.li:
            if(i.lower() == "image"):
                continue
            
            self.curr_data = self.basic_info_label.cget("text")
            self.new_text  = f"\n {i} : {self.li[i]}"
            self.final_text = self.curr_data + self.new_text
            self.basic_info_label["text"] = self.final_text

        
        qrcode.make(f'https://codefest23.netlify.app/?data={self.currentEmail}').save(f"{self.currentEmail}.png")
        self.qrImage = tk.PhotoImage(file = f"{self.currentEmail}.png")

        if(self.times == 0):
            self.qrLabel = tk.Label(self, image = self.qrImage)
            self.qrLabel.pack()
            self.times == 1
        
        

        self.editBtn = ctk.CTkButton(self, text = "Edit Card", command = self.editCard)
        self.editBtn.pack()

        self.OCRBtn = ctk.CTkButton(self, text = "Scan Document", command = self.OCRCard)
        self.OCRBtn.pack()

    def editCard(self):
        self.container.editcard.tkraise()
    def OCRCard(self):
        self.container.ocr.tkraise()
    
    def goback(self):
        self.container.homepage.showcard()
        self.container.homepage.showcard.tkraise()
        

class Editcard(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.enterTopic = ctk.CTkEntry(master = self, placeholder_text = "New data topic")
        self.enterData = ctk.CTkEntry(master=self, placeholder_text="New Data.")
        self.addBtn = ctk.CTkButton(self, text = "Add", command = self.add)
        self.enterTopic.pack()
        self.enterData.pack()
        self.addBtn.pack()
        self.currentEmail = ''

        self.gobackBtn = ctk.CTkButton(self, text = "Go Back", command = self.goback)
        self.gobackBtn.pack()

    def add(self):
        self.topic = self.enterTopic.get()
        self.data = self.enterData.get()
        ref.child(f'{self.currentEmail}').update({f'{self.topic}': f'{self.data}'})

    def goback(self):
        self.container.maincard.showcard()
        self.container.maincard.tkraise()


        



class Homepage(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.currentEmail = ""
        self.container =  container
        self.pfpImage = self.container.pfpImage
        self.pfpBtn = tk.Button(self, bg = "white", border = 0, width = 100, height = 100, image = self.pfpImage)
        self.pfpBtn.place(x = 10, y = 10)
        self.company_name = ctk.CTkLabel(self, text= "MEDICARD")
        self.company_name.pack()
        self.li = []
        self.cardBtn = tk.Button(self, text = "",bg='#1e6ca4',
    fg='#ffffff',
    bd=0,
    font=('calibri', 20, 'bold'), command = self.showmaincard)
        self.cardBtn.pack()

        self.showcard()

    def showmaincard(self):
        self.container.maincard.showcard()
        self.container.maincard.tkraise()

    def showcard(self): 
        self.cardBtn["text"] = ""
        
        self.curr_data = self.cardBtn.cget("text")
        data = ref.get()
        for key, value in data.items():
            if(key == self.currentEmail):
                self.li = value
          

        for i in self.li:
            if(i.lower() == "image"):
                continue
            
            self.curr_data = self.cardBtn.cget("text")
            self.new_text  = f"\n {i} : {self.li[i]}"
            self.final_text = self.curr_data + self.new_text
            self.cardBtn["text"] = self.final_text
            if(i.lower() == "weight"):
                break

class OCR(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.currentEmail = ""

        self.enterTopic = ctk.CTkEntry(master = self, placeholder_text = "New data topic")
        self.enterTopic.pack()

        self.button = ctk.CTkButton(self, text = "upload file", command = self.upload)
        self.button.pack()

        self.addBtn = ctk.CTkButton(self, text = "Add", command = self.add)
        self.addBtn.pack()

        self.gobackBtn = ctk.CTkButton(self, text = "Go Back", command = self.goback)
        self.gobackBtn.pack()

    def upload(self):
        
        self.filename = filedialog.askopenfilename(initialdir = "D:\\python grind\\oakridge hackathon", title = "select a file", filetypes = (("png files", "*.png"),("jpg files", "*.jpg")))
        self.image = cv2.imread(self.filename)
        self.data = pytesseract.image_to_string(self.image)

        self.label = ctk.CTkLabel(self, text = self.data)
        self.label.pack()

    def add(self):
        
        self.gobackBtn = ctk.CTkButton(self, text = "Go Back", command = self.goback)
        self.gobackBtn.pack()

   

    def goback(self):
        self.container.maincard.showcard()
        self.container.maincard.tkraise()
        


    
        

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
        self.pfp = ctk.CTkButton(self, text = "Upload picture of yourself.", command = self.uploadpfp)
        self.pfp.pack(padx=30, pady=20)
        self.button = ctk.CTkButton(master=self, text="Sign Up.", command=self.button_function_two)
        self.button.pack(padx=30, pady=20)  
    def uploadpfp(self):
        self.filename = filedialog.askopenfilename(initialdir = "D:\\python grind\\oakridge hackathon", title = "select a file", filetypes = (("png files", "*.png"),("jpg files", "*.jpg")))
    def button_function_two(self):
        auth.create_user(email=self.emailEntry.get(), password=self.passwordEntry.get())
        
        self.currentEmail = f'{self.emailEntry.get().replace("@", "").replace(".", "")}_{self.nameEntry.get()}'
        ref.child(f'{self.emailEntry.get().replace("@", "").replace(".", "")}_{self.nameEntry.get()}').set({
            'Image': f'{self.filename}',
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
        self.container.maincard.currentEmail = self.currentEmail
        self.container.homepage.showcard()
        self.container.editcard.currentEmail = self.currentEmail
        self.container.ocr.currentEmail = self.currentEmail
    


root = Window()
root.mainloop()
