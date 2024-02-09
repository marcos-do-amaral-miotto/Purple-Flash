from customtkinter import *
from tkinter import filedialog
import pytube
import os

# Função que executa o download das musicas
def musicDownload():
    destination = selection_button.cget('text')
    form = formato.get()
    if destination == 'Pendrive':
        return
    if URL.get() == '':
        return
    if URL.get().find('list') == -1:
        yt = pytube.YouTube(URL.get())
        if form == 'mp4':
            yt.streams.filter(type='video', file_extension='mp4', progressive=True).get_highest_resolution().download(output_path=destination)
        else:
            out_file = yt.streams.filter(only_audio=True, file_extension='mp4', progressive=False).get_audio_only().download(output_path=destination)
            base, ext = os.path.splitext(out_file) 
            new_file = base + f'.{form}'
            os.rename(out_file, new_file)
    else:
        p = pytube.Playlist(URL.get())
        if not p:
            print('Playlist não existe ou modo de exibição é particular, tente mudar para não listada ou pública!')
        else:
            print('Download')

        # if form == 'mp4':
        #     for video in p.videos:
        #         print(video.title)
        #         video.streams.filter(type='video', file_extension='mp4', progressive=True).get_highest_resolution().download(output_path=destination)
        # else:
        #     for video in p.videos:
        #         print(video.title)
        #         out_file = video.streams.filter(only_audio=True, file_extension='mp4', progressive=False).get_audio_only().download(output_path=destination)
        #         base, ext = os.path.splitext(out_file) 
        #         new_file = base + f'.{form}'
        #         os.rename(out_file, new_file)

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
                placeholder_text_color='#7b2cbf', font=('Roboto', 18), width=860)
URL.place(x=170, y=350)
formato = CTkOptionMenu(master=app, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                        button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                        width=90, values=['mp4', 'mp3', 'wav'])
formato.place(x=1010, y=400)
selection_button = CTkButton(master=app, text='Pendrive', font=('Roboto', 20), width=170, command=flashSelection)
selection_button.place(x=200, y=550)
download_button = CTkButton(master=app, text='Download', font=('Roboto', 20), width=170, command=musicDownload)
download_button.place(x=200, y=450)

app.mainloop()
