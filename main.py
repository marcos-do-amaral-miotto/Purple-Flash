from customtkinter import *

app = CTk()
set_appearance_mode('dark')
height = app.winfo_screenheight()
width = app.winfo_screenwidth()
app.geometry(f"{int(width*0.7)}x{int(height*0.7)}+{int(width/2-width*0.35)}+{int(height/2-height*0.40)}")
URL = CTkEntry(master=app, placeholder_text='URL...')
URL.place(x=0, y=0)
app.mainloop()
