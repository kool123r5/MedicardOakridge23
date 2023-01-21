import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from firebase_admin import credentials, db, auth
import firebase_admin
import time
from tkinter import ttk
from customtkinter import filedialog
import qrcode
import pytesseract
import cv2
import requests
import webbrowser
from gingerit.gingerit import GingerIt
import language_tool_python


#todo
# ocr with camera
# navigation buttons
# styling
# buttons to shwinn + ando work


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
        self.geometry("390x644")
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
        self.basic_info_label.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER)


        
        
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

        
        

        if(self.times == 0):
            qrcode.make(f'https://codefest23.netlify.app/?data={self.currentEmail}').save(f"{self.currentEmail}.png")
            self.qrImage = tk.PhotoImage(file = f"{self.currentEmail}.png")
            self.qrLabel = tk.Label(self, image = self.qrImage)
            
            self.qrLabel.place(relx = 0.1, rely = 0.9, anchor = tk.CENTER)
            self.times = 1

            self.editBtn = ctk.CTkButton(self, text = "Edit Card", command = self.editCard)
            self.editBtn.place(relx = 0.8, rely = 0.05, anchor = tk.CENTER)

            self.OCRBtn = ctk.CTkButton(self, text = "Scan Document", command = self.OCRCard)
            self.OCRBtn.place(relx = 0.2, rely = 0.05, anchor = tk.CENTER)

            self.goback = ctk.CTkButton(self, text = "Go Back", command = self.goback)
            self.goback.place(relx = 0.8, rely = 0.95, anchor = tk.CENTER)
            



    def editCard(self):
        self.container.editcard.tkraise()
    def OCRCard(self):
        self.container.ocr.tkraise()
    
    def goback(self):
        self.container.homepage.tkraise()
        

class Editcard(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container

        

        label = ctk.CTkLabel(self, text = "Add or Edit Info", font = ("Comic Sans MS", 35, "bold"))
        label.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

        self.enterTopic = ctk.CTkEntry(master = self, placeholder_text = "New data topic", font = ("Helvatica", 20))
        self.enterTopic.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER, width = 200)

        self.enterData = ctk.CTkEntry(master=self, placeholder_text="New Data.")
        self.enterData.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER, width = 350)

        self.addBtn = ctk.CTkButton(self, text = "Add", command = self.add)
        self.addBtn.place(relx = 0.5, rely = 0.7, anchor = tk.CENTER)


        self.currentEmail = ''

        self.gobackBtn = ctk.CTkButton(self, text = "Go Back", command = self.goback)
        self.gobackBtn.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)

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
        self.container =  container
        self.text = ""
        self.li = []

        self.img = ImageTk.PhotoImage(Image.open("logo.png"))
        self.logoLabel=tk.Label(self, image = self.img, bg = "#2B2B2B")
        self.logoLabel.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)
        
        self.company_name = ctk.CTkLabel(self, text= "MEDICARD", font = ("Comic Sans MS", 50, "bold"))
        self.company_name.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

        self.cardBtn = ctk.CTkButton(self, text = "Show Main Card", command = self.showmaincard, font=('Helvetica', 30))
        self.cardBtn.place(relx = 0.5, rely = 0.25, anchor = tk.CENTER)

        self.dataLabel = tk.Label(self, text = "", bg = "#1e6ca4", fg = "white", font=('Helvetica', 15), padx = 20, pady = 20)
        self.dataLabel.place(relx = 0.5, rely = 0.4, anchor = tk.CENTER)

        
        self.open_scheduleBtn = ctk.CTkButton(self, text = "Open Schedule", command = self.open_schedule, font=('Helvetica', 20))
        self.open_scheduleBtn.place(relx = 0.8, rely = 0.6, anchor = tk.CENTER)
        
        self.open_calendarBtn = ctk.CTkButton(self, text = "Open Calendar", command = self.open_calendar, font=('Helvetica', 20))
        self.open_calendarBtn.place(relx = 0.2, rely = 0.6, anchor = tk.CENTER)

    def open_calendar(self):
        new = 1
        url = "https://medicard-calender-1.netlify.app/"    
        webbrowser.open(url,new=new)

    def showmaincard(self):
        self.container.maincard.showcard()
        self.container.maincard.tkraise()

    def showcard(self):
        self.dataLabel["text"] = ""
        data = ref.get()
        for key, value in data.items():
            if(key == self.currentEmail):
                self.li = value

        for i in self.li:
            if(i.lower() == "name"):
                self.text = self.text + f"\nname: {self.li[i]}"
            elif(i.lower() == "height"):
                self.text = self.text + f"height: {self.li[i]} cm"
            elif(i.lower() == "weight"):
                self.text = self.text + f"\nweight: {self.li[i]} kg"
        
        self.dataLabel["text"] = self.text

    def open_schedule(self):
        pass


    

class OCR(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)
        self.container = container
        self.currentEmail = ""

        self.label = ctk.CTkLabel(self, text = "Scan Prescriptions", font = ("Comic Sans MS", 35, "bold"))
        self.label.place(relx = 0.5, rely = 0.1, anchor = tk.CENTER)

        self.enterTopic = ctk.CTkEntry(master = self, placeholder_text = "New data topic")
        self.enterTopic.place(relx = 0.5, rely = 0.3, anchor = tk.CENTER, width = 300)


        self.scanImg = ctk.CTkButton(self, text = "Take Picture", command = self.uploadPicture)
        self.scanImg.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

        self.uploadImg = ctk.CTkButton(self, text = "Upload File", command = self.upload)
        self.uploadImg.place(relx = 0.5, rely = 0.6, anchor = tk.CENTER)

        self.addBtn = ctk.CTkButton(self, text = "Add", command = self.add)
        self.addBtn.place(relx = 0.5, rely = 0.8, anchor = tk.CENTER)

        self.gobackBtn = ctk.CTkButton(self, text = "Go Back", command = self.goback)
        self.gobackBtn.place(relx = 0.5, rely = 0.9, anchor = tk.CENTER)

    def uploadPicture(self):
        pass

    def upload(self):
        
        self.filename = filedialog.askopenfilename(initialdir = "D:\\python grind\\oakridge hackathon", title = "select a file", filetypes = (("png files", "*.png"),("jpg files", "*.jpg")))
        self.image = cv2.imread(self.filename)
        self.data = pytesseract.image_to_string(self.image)

        self.label = ctk.CTkLabel(self, text = self.data)
        self.label.pack()

        

    def add(self):
        self.topic = self.enterTopic.get()
        ref.child(f'{self.currentEmail}').update({f'{self.topic}': f'{self.data}'})
        

   

    def goback(self):
        self.container.maincard.showcard()
        self.container.maincard.tkraise()
        


    
        

class LoginFrame(ctk.CTkFrame):
    def __init__(self, container):
        super().__init__(container)

         
        
        self.container = container
        self.emailEntry = ctk.CTkEntry(master=self, placeholder_text="Email.")
        self.emailEntry.pack(padx=30, pady=10)
        self.passwordEntry = ctk.CTkEntry(master=self, show="*", placeholder_text="Password.")
        self.passwordEntry.pack(padx=30, pady=10)
        self.nameEntry = ctk.CTkEntry(master=self, placeholder_text="Name.")
        self.nameEntry.pack(padx=30, pady=10)
        self.ageEntry = ctk.CTkEntry(master=self, placeholder_text="Age.")
        self.ageEntry.pack(padx=30, pady=10)
        self.heightEntry = ctk.CTkEntry(master=self, placeholder_text="Height (in cm).")
        self.heightEntry.pack(padx=30, pady=10)
        self.bloodEntry = ctk.CTkEntry(master=self, placeholder_text="Blood type.")
        self.bloodEntry.pack(padx=30, pady=10)
        self.allergyEntry = ctk.CTkEntry(master=self, placeholder_text="Allergies.")
        self.allergyEntry.pack(padx=30, pady=10)
        self.phobiaEntry = ctk.CTkEntry(master=self, placeholder_text="Phobias.")
        self.phobiaEntry.pack(padx=30, pady=10)
        self.vaxEntry = ctk.CTkEntry(master=self, placeholder_text="Prior vaccinations.")
        self.vaxEntry.pack(padx=30, pady=10)
        self.weightEntry = ctk.CTkEntry(master=self, placeholder_text="Weight (in kg).")
        self.weightEntry.pack(padx=30, pady=10)
        self.pfp = ctk.CTkButton(self, text = "Upload picture of yourself.", command = self.uploadpfp)
        self.pfp.pack(padx=30, pady=10)
        self.button = ctk.CTkButton(master=self, text="Sign Up.", command=self.button_function_two)
        self.button.pack(padx=30, pady=10)  
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
