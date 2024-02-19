from customtkinter import *
from tkinter import filedialog
from PIL import Image
from threading import Thread
from pathlib import Path
from moviepy.editor import *
from urllib import request
from io import BytesIO
import pytube
import os


# Função que executa o download das musicas
def musicDownload():
    message_box.configure(text = '')
    url = URL.get()
    vid_aud = type_menu.get()
    quality = quality_menu.get()
    extension = extension_menu.get()
    destination = Path(destination_label.cget('text'))
    if url == '':
        return
    if url.find('youtube.com/') == -1:
        message_box.configure(text='Esse não é um link válido, tente colocar o link de um vídeo ou playlist do YouTube!')
        return
    if vid_aud == 'Vídeo📽' and extension.find('🔈') != -1:
        message_box.configure(text=f'Escolher o formato de Vídeo e a extenção {extension[0:len(extension)-1]} é incongruente. Por favor, selecione outra combinação!')
        return
    # Vídeo isolado
    if url.find('list') == -1:
        yt = pytube.YouTube(url)
        try:
            vid = yt.streams
        except:
            message_box.configure(text='Ocorreu um erro! O vídeo está com visibilidade "Privado", tente alterar para "Não listado" ou "Público"!')
            return
        # mexe aqui pra colocar as thumbnails no GUI principal
        if vid_aud == 'Áud/Víd':
            if quality == 'Alta Definição':
                vid.get_highest_resolution().download(output_path=destination)
            else:
                vid.get_highest_resolution().download(output_path=destination)
        elif vid_aud == 'Áudio🔈':
            filtered = vid.filter(only_audio=True)
            if quality == 'Alta Definição':
                itag = [0, 0]
                for i in filtered:
                    value = int(i.abr[0:len(i.abr)-4])
                    if value > itag[1]:
                        itag[0] = i.itag
                        itag[1] = value
            else:
                itag = [0, 10000]
                for i in filtered:
                    value = int(i.abr[0:len(i.abr)-4])
                    if value < itag[1]:
                        itag[0] = i.itag
                        itag[1] = value
            music = vid.get_by_itag(itag[0]).download(output_path='files')
            name, ext = os.path.splitext(os.listdir('files')[0])
            converted = AudioFileClip(music)
            converted.write_audiofile(Path(fr"{destination}\{name}.{extension}"))
            converted.close()
            os.remove(music)
        else:
            if quality == 'Alta Definição':
                itag = vid.filter(mime_type=f'video/{extension}', only_video=True)[0].itag
            else:
                filtered = vid.filter(mime_type=f'video/{extension}', only_video=True)
                itag = filtered[len(filtered)-1].itag
            vid.get_by_itag(itag).download(output_path=destination)
    # Playlist
    else:
        pl = pytube.Playlist(url)
        try:
            pl.videos[0].streams
        except:
            message_box.configure(text='Ocorreu um erro! A playlist está com visibilidade "Privado" ou é um Mix do YouTube, tente alterar a visibilidade ou escolher uma playlist válida!')
            return
        title = pl.title.replace("/", "-").replace("\\", '-').replace(":", '-').replace("*", '°').replace("?", '❔').replace('"', "'").replace('>', "}").replace('<', "{").replace('|', "!")
        if title == "con" or title == "prn" or title == "aux" or title == "com1" or title == "ltp1":
            title = 'Playlist'
        try:
            destination = destination / title
        except:
            message_box.configure(text='Ocorreu um erro! A playlist está com um nome que não pode ser transformado em uma pasta, tente renomea-la!')
            return
        # mexe aqui pra colocar as thumbnails no GUI principal
        if vid_aud == 'Áud/Víd':
            if quality == 'Alta Definição':
                for i in pl.videos:
                    vid = i.streams
                    file = vid.filter(file_extension='mp4').get_highest_resolution().download(output_path=destination)
                    if extension != 'mp4':
                        os.rename(file, f'{file[0:len(file)-3]}{extension}')
            else:
                for vid in pl.videos.streams:
                    vid = vid.filter(file_extension='mp4')
                    file = vid.filter(file_extension='mp4').get_lowest_resolution().download(output_path=destination)
                    if extension != 'mp4':
                        os.rename(file, f'{file[0:len(file)-3]}{extension}')
        elif vid_aud == 'Áudio🔈':
            for i in pl.videos:
                vid = i.streams
                filtered = vid.filter(only_audio=True)
                if quality == 'Alta Definição':
                    itag = [0, 0]
                    for i in filtered:
                        value = int(i.abr[0:len(i.abr)-4])
                        if value > itag[1]:
                            itag[0] = i.itag
                            itag[1] = value
                else:
                    itag = [0, 10000]
                    for i in filtered:
                        value = int(i.abr[0:len(i.abr)-4])
                        if value < itag[1]:
                            itag[0] = i.itag
                            itag[1] = value
                music = vid.get_by_itag(itag[0]).download(output_path=destination)
                name, ext = os.path.splitext(music)
                os.rename(music, fr'{name}.{extension}')
        else:
            for i in pl.videos:
                vid = i.streams
                if quality == 'Alta Definição':
                    itag = vid.filter(mime_type=f'video/webm', only_video=True)[0].itag
                else:
                    filtered = vid.filter(mime_type=f'video/webm', only_video=True)
                    itag = filtered[len(filtered)-1].itag
                vid.get_by_itag(itag).download(output_path=destination)


def validUrl(event):
    message_box.configure(text = '')
    url = URL.get()
    vid_aud = type_menu.get()
    quality = quality_menu.get()
    extension = extension_menu.get()
    destination = Path(destination_label.cget('text'))
    if url == '':
        return
    if url.find('youtube.com/') == -1:
        message_box.configure(text='Esse não é um link válido, tente colocar o link de um vídeo ou playlist do YouTube!')
        return
    if vid_aud == 'Vídeo📽' and extension.find('🔈') != -1:
        message_box.configure(text=f'Escolher o formato de Vídeo e a extenção {extension[0:len(extension)-1]} é incongruente. Por favor, selecione outra combinação!')
        return
    # Vídeo isolado
    if url.find('list') == -1:
        yt = pytube.YouTube(url)
        try:
            vid = yt.streams
            print('deu certo')
        except:
            message_box.configure(text='Ocorreu um erro! O vídeo está com visibilidade "Privado", tente alterar para "Não listado" ou "Público"!')
            return

# Dividir o processamento do programa entre a tela GUI e o download dos vídeos
def execDownload():
    thread = Thread(target=musicDownload)
    thread.start()


# Função para selecionar o pendrive
def flashSelection():
    directory = filedialog.askdirectory()
    if directory != '':
        directory = Path(directory)
        destination_label.configure(text=directory)


def formatSelection(value):
    if value == 'Áud/Víd':
        formatos = ['mp4', 'mov', 'wkv', 'm4v', 'webm']
        vformato = StringVar()
        vformato.set(formatos[0])
    elif value == 'Áudio🔈':
        formatos = ['mp3', 'wma', 'ogg', 'aac', 'wav']
        vformato = StringVar()
        vformato.set(formatos[0])
    else:
        formatos = ['webm', 'mp4', 'mov', 'wkv', 'm4v']
        vformato = StringVar()
        vformato.set(formatos[0])
    extension_menu.configure(variable = vformato)
    extension_menu.configure(values = formatos)


# Pegar o diretorio padrão da pasta downloads do pc do usuário
diretorio_home = Path.home()
diretorio_downloads = diretorio_home / "Downloads"
if diretorio_downloads.is_dir():
    pass
else:
    diretorio_downloads = 'Selecione uma pasta para download'

# Configurações da janela
set_appearance_mode("dark")
app = CTk()
height = app.winfo_screenheight()
width = app.winfo_screenwidth()
app.geometry(f"1200x600+{int(width/2-600)}+{int(height/2-300)}")
app.resizable(width=False, height=False)
app.iconbitmap(bitmap='icon.ico')
app.title('Purple Flash')

# Widgets
imagem = CTkImage(Image.open('icone.png'), size=(300, 300))
CTkLabel(master=app, text='', image=imagem).place(y=20, x=430, anchor='n')
CTkLabel(master=app, text='purple', font=('Bebas Neue', 120), text_color='#7b2cbf').place(y=20, x=680, anchor='n')
CTkLabel(master=app, text='flash', font=('Bebas Neue', 150), text_color='#7b2cbf').place(y=140, x=680, anchor='n')
URL = CTkEntry(master=app, placeholder_text='Link da playlist, vídeo ou música', border_color='#7b2cbf', 
                placeholder_text_color='#7b2cbf', font=('Roboto', 18), corner_radius=12, width=860)
# URL.bind("<KeyRelease>", validUrl)
URL.place(x=170, y=350)
message_box = CTkLabel(master=app, text='', font=('Roboto', 16), text_color='#7b2cbf', anchor='center',
                width=1200, height=20)
message_box.place(x=0, y=385)
type_menu = CTkOptionMenu(master=app, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                        button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                        corner_radius=10, width=120, anchor='center', values=['Áud/Víd', 'Áudio🔈', 'Vídeo📽'], 
                        command=formatSelection)
type_menu.place(x=390, y=410, anchor='nw')
quality_menu = CTkOptionMenu(master=app, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                        button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                        corner_radius=10, width=190, anchor='center', values=['Alta Definição', 'Baixa Definição'])
quality_menu.place(x=520, y=410, anchor='nw')
extension_menu = CTkOptionMenu(master=app, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                        button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                        corner_radius=10, width=100, anchor='center', values=['mp4', 'mov', 'wkv', 'm4v', 'webm'])
extension_menu.place(x=720, y=410, anchor='nw')
selection_button = CTkButton(master=app, text='Pendrive', fg_color='#7b2cbf', hover_color='#5a189a', 
                        font=('Roboto', 20), corner_radius=12, width=120, anchor='center', command=flashSelection)
selection_button.place(x=390, y=448, anchor='nw')
destination_label = CTkLabel(master=app, text=diretorio_downloads, text_color='#7b2cbf', font=('Roboto', 20))
destination_label.place(x=520, y=448, anchor='nw')
download_button = CTkButton(master=app, text='Download', fg_color='#7b2cbf', font=('Roboto', 20), 
                        hover_color='#5a189a', corner_radius=12, width=170, command=execDownload)
download_button.place(x=600, y=490, anchor='n')

app.mainloop()
