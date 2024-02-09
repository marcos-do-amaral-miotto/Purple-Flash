from customtkinter import *
from tkinter import filedialog
from threading import Thread
import pytube
import os

# Função que executa o download das musicas
def musicDownload():
    destination = selection_button.cget('text')
    extension = extension_menu.get()
    if destination == 'Pendrive':
        return
    if URL.get() == '':
        return
    if URL.get().find('list') == -1:
        yt = pytube.YouTube(URL.get())
        if extension == 'mp4':
            yt.streams.filter(type='video', file_extension='mp4', progressive=True).get_highest_resolution().download(output_path=destination)
        else:
            out_file = yt.streams.filter(file_extension='mp4', progressive=False).get_audio_only().download(output_path=destination)
            base, ext = os.path.splitext(out_file) 
            new_file = base + f'.{extension}'
            os.rename(out_file, new_file)
    else:
        p = pytube.Playlist(URL.get())
        destination = destination + f'/{p.title}'
        if extension == 'mp4':
            for video in p.videos:
                print(video.title)
                video.streams.filter(type='video', file_extension='mp4', progressive=True).get_lowest_resolution().download(output_path=destination)
        else:
            for video in p.videos:
                print(video.title)
                out_file = video.streams.filter(only_audio=True, file_extension='mp4', progressive=False).get_audio_only().download(output_path=destination)
                base, ext = os.path.splitext(out_file) 
                new_file = base + f'.{extension}'
                os.rename(out_file, new_file)

def execDownload():
    thread = Thread(target=musicDownload)
    thread.start()

# Função para selecionar o pendrive
def flashSelection():
    directory = filedialog.askdirectory()
    if directory != '':
        selection_button.configure(text=directory)

# Configurações da janela
set_appearance_mode("dark")
app = CTk()
height = app.winfo_screenheight()
width = app.winfo_screenwidth()
app.configure(resizable=False)
app.geometry(f"1200x600+{int(width/2-600)}+{int(height/2-300)}")
app.resizable(width=False, height=False)
app.iconbitmap(bitmap='icon.ico')
app.title('Purple Flash')

# Widgets
URL = CTkEntry(master=app, placeholder_text='Link da playlist, vídeo ou música', border_color='#7b2cbf', 
                placeholder_text_color='#7b2cbf', font=('Roboto', 18), corner_radius=12, width=860)
URL.place(x=170, y=350)
message_box = CTkLabel(master=app, text='espaço reservado', font=('Roboto', 16), text_color='#7b2cbf', anchor='center',
                width=860, height=20)
message_box.place(x=170, y=385)
type_menu = CTkOptionMenu(master=app, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                        button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                        corner_radius=10, width=90, values=['Vídeo', 'Áudio'])
type_menu.place(x=300, y=410)
extension_menu = CTkOptionMenu(master=app, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                        button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                        corner_radius=10, width=90, values=['mp4', 'mp3', 'wav'])
extension_menu.place(x=400, y=410)
selection_button = CTkButton(master=app, text='Pendrive', fg_color='#7b2cbf', hover_color='#5a189a', 
                        font=('Roboto', 20), corner_radius=12, width=170, command=flashSelection)
selection_button.place(x=500, y=410)
download_button = CTkButton(master=app, text='Download', fg_color='#7b2cbf', font=('Roboto', 20), 
                        hover_color='#5a189a', corner_radius=12, width=170, command=execDownload)
download_button.place(x=690, y=410)

app.mainloop()
