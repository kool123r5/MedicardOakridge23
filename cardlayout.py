import tkinter
from tkinter import *
from tkinter import messagebox
import tkinter.font as font



root = tkinter.Tk()
root.geometry("800x800")

photo = PhotoImage(file="group.png")


Dp_photo = PhotoImage(file="dp.png")

myFont = font.Font(family='Helvetica')


btn = Button(
    root,
    image=photo,
    border=0,
    # foreground="black",
    # text="Name: Aneesh Mamidi"
    
)



btn2 = Button(
    root,
    bg='white',
    border=0,
    width=8,
    height=2,
    text="Scan",
    foreground="black",
    font= myFont
    
    
)

btn3 = Button(
    root,
    bg='white',
    border=0,
    width=100,
    height=115,
    image=Dp_photo
    
    
)






btn.pack(pady=50)
btn2.pack(pady=50)
btn2.place(rely=0.0636, relx=0.7475)

btn3.place(rely=0.055, relx=0.2)



root.mainloop()
