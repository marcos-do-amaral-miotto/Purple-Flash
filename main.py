from customtkinter import *
from tkinter import filedialog
from PIL import Image
from threading import Thread
from pathlib import Path
from moviepy.editor import *
from urllib import request
from io import BytesIO
import pytube
from time import sleep
import os
import tkinter as tk

def musicDownload(url, vid_aud, quality, extension, destination):
    # Vídeo isolado
    if url.find('list') == -1:
        yt = pytube.YouTube(url)
        vid = yt.streams
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
        title = pl.title.replace("/", "-").replace("\\", '-').replace(":", '-').replace("*", '°').replace("?", '❔').replace('"', "'").replace('>', "}").replace('<', "{").replace('|', "!")
        if title == "con" or title == "prn" or title == "aux" or title == "com1" or title == "ltp1":
            title = 'Playlist'
        try:
            destination = destination / title
        except:
            title = 'Playlist'
            destination = destination / title
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


class window(CTk):
    def __init__(self):
        # Pegar o diretorio padrão da pasta downloads do pc do usuário
        diretorio_downloads = Path.home() / "Downloads"
        if diretorio_downloads.is_dir() is False:
            diretorio_downloads = 'Selecione uma pasta para download'
        
        # Definição das caracteristicas da window
        super().__init__()
        set_appearance_mode("dark")
        self.geometry(f"1200x600+{int(self.winfo_screenwidth()/2-600)}+{int(self.winfo_screenheight()/2-300)}")
        self.resizable(width=False, height=False)
        self.iconbitmap(bitmap='img/icon.ico')
        self.title('Purple Flash')

        # Widgets
        self.logo = CTkLabel(master=self, text='', image=CTkImage(Image.open('img/icone.png'), size=(300, 300)))
        self.logo.place(y=30, x=430, anchor='n')
        self.purple_text = CTkLabel(master=self, text='purple', font=('Bebas Neue', 120), text_color='#7b2cbf')
        self.purple_text.place(y=30, x=680, anchor='n')
        self.flash_text = CTkLabel(master=self, text='flash', font=('Bebas Neue', 150), text_color='#7b2cbf')
        self.flash_text.place(y=150, x=680, anchor='n')
        self.minilogo = CTkLabel(master=self, text='', image=CTkImage(Image.open('img/icone.png'), size=(200, 200)))
        self.minipurple_text = CTkLabel(master=self, text='purple', font=('Bebas Neue', 79), text_color='#7b2cbf')
        self.miniflash_text = CTkLabel(master=self, text='flash', font=('Bebas Neue', 99), text_color='#7b2cbf')
        self.URL = CTkEntry(master=self, placeholder_text='Link da playlist, vídeo ou música', border_color='#7b2cbf',
                        placeholder_text_color='#7b2cbf', font=('Roboto', 18), corner_radius=12, width=860)
        self.URL.bind("<KeyRelease>", self.createFrame)
        self.URL.place(x=170, y=390)
        self.message_box = CTkLabel(master=self, text='', font=('Roboto', 16), text_color='#7b2cbf', anchor='center',
                        width=1200, height=20)
        self.message_box.place(x=0, y=425)
        self.quality_menu = CTkOptionMenu(master=self, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                                button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                                corner_radius=10, width=190, anchor='center', values=['Alta Definição', 'Baixa Definição'])
        self.quality_menu.place(x=520, y=450, anchor='nw')
        self.extension_menu = CTkOptionMenu(master=self, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                                button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                                corner_radius=10, width=100, anchor='center', values=['mp4', 'mov', 'wkv', 'm4v', 'webm'])
        self.extension_menu.place(x=720, y=450, anchor='nw')
        self.type_menu = CTkOptionMenu(master=self, font=('Roboto', 20), dropdown_font=('Roboto', 20), fg_color='#7b2cbf',
                                button_color='#7b2cbf', button_hover_color='#5a189a', dropdown_hover_color='#7b2cbf',
                                corner_radius=10, width=120, anchor='center', values=['Áud/Víd', 'Áudio🔈', 'Vídeo📽'],
                                command=self.formatSelection)
        self.type_menu.place(x=390, y=450, anchor='nw')
        self.selection_button = CTkButton(master=self, text='Pendrive', fg_color='#7b2cbf', hover_color='#5a189a', 
                                font=('Roboto', 20), corner_radius=12, width=120, anchor='center', command=self.flashSelection)
        self.selection_button.place(x=390, y=488, anchor='nw')
        self.destination_label = CTkLabel(master=self, text=diretorio_downloads, text_color='#7b2cbf', font=('Roboto', 20))
        self.destination_label.place(x=520, y=488, anchor='nw')
        self.download_button = CTkButton(master=self, text='Download', fg_color='#7b2cbf', font=('Roboto', 20), 
                                hover_color='#5a189a', corner_radius=12, width=170, command=self.execDownload)
        self.download_button.place(x=600, y=530, anchor='n')
        
        # Configurações do load
        self.frame = CTkFrame(self, width=1180, height=152)
        self.clip = CTkFrame(self.frame, fg_color='transparent')
        self.clip.place(x=590, y=76, anchor='center')
        self.clipInfo = CTkFrame(self.clip, fg_color='transparent')
        self.clipImg = CTkLabel(master=self.clip, text='')
        self.clipImg.pack(side='left', padx=10)
        self.clipInfo.pack(side='left', padx=10)
        self.clipName = CTkLabel(master=self.clipInfo, text='', font=('Roboto', 28))
        self.clipName.pack()
        self.clipAuthor = CTkLabel(master=self.clipInfo, text='', font=('Roboto', 20))
        self.clipAuthor.pack()
        self.canvas = CTkCanvas(master=self.frame, width=1475, height=190, bg='#2b2b2b')
        self.raio1 = 20
        self.raio2 = 20
        self.raio3 = 20
        self.status1 = 'growing'
        self.status2 = 'static'
        self.status3 = 'static'
        self.canvas.create_aa_circle(667,95,self.raio1, fill='#7b2cbf')
        self.canvas.create_aa_circle(737,95,self.raio2, fill='#7b2cbf')
        self.canvas.create_aa_circle(807,95,self.raio3, fill='#7b2cbf')
        self.after(15, self.loading)

        self.mainloop()
    
    def formatSelection(self, value):
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
        self.extension_menu.configure(variable = vformato)
        self.extension_menu.configure(values = formatos)

    def flashSelection(self):
        directory = filedialog.askdirectory()
        if directory != '':
            directory = Path(directory)
            self.destination_label.configure(text=directory)

    def createFrame(self, event):
        try:
            youtube = pytube.YouTube(self.URL.get())
        except:
            if self.URL.get().find('youtube.com/playlist?list=') != -1:
                self.message_box.configure(text='Por favor, tente colocar o link da playlist com um de seus vídeos abertos para o funcionamento do programa!')
            self.frame.place_forget()
            self.minilogo.place_forget()
            self.minipurple_text.place_forget()
            self.miniflash_text.place_forget()
            self.clipName.configure(text='')
            self.logo.place(y=30, x=430, anchor='n')
            self.purple_text.place(y=30, x=680, anchor='n')
            self.flash_text.place(y=150, x=680, anchor='n')
            return
        self.logo.place_forget()
        self.purple_text.place_forget()
        self.flash_text.place_forget()
        self.minilogo.place(y=10, x=500, anchor='n')
        self.minipurple_text.place(y=10, x=670, anchor='n')
        self.miniflash_text.place(y=90, x=670, anchor='n')
        self.canvas.place(x=-2, y=-2)
        self.canvas.config(cursor='watch')
        self.frame.place(x=10, y=230)
        thread = Thread(target=self.validUrl)
        thread.start()
    
    def validUrl(self):
        # Vídeo isolado
        if self.URL.get().find('list') == -1:
            try:
                yt = pytube.YouTube(self.URL.get())
                vid = yt.streams
            except:
                self.message_box.configure(text='Ocorreu um erro! O vídeo está com visibilidade "Privado", tente alterar para "Não listado" ou "Público"!')
                self.frame.place_forget()
                self.minilogo.place_forget()
                self.minipurple_text.place_forget()
                self.miniflash_text.place_forget()
                self.logo.place(y=30, x=430, anchor='n')
                self.purple_text.place(y=30, x=680, anchor='n')
                self.flash_text.place(y=150, x=680, anchor='n')
                return
            self.message_box.configure(text='')
            imagem_bytes = BytesIO(request.urlopen(yt.thumbnail_url).read())
            img = Image.open(imagem_bytes)
            largura_original, altura_original = img.size
            imagem = CTkImage(img, size=((largura_original * 148 / altura_original), (148)))
            self.canvas.place_forget()
            self.clipImg.configure(image=imagem)
            self.clipName.configure(text=yt.title)
            self.clipAuthor.configure(text=yt.author)
            self.canvas.config(cursor='arrow')
        else:
            try:
                pl = pytube.Playlist(self.URL.get())
                pl.videos[0].streams
            except:
                message_box.configure(text='Ocorreu um erro! A playlist está com visibilidade "Privado" ou é um Mix do YouTube, tente alterar a visibilidade ou escolher uma playlist válida!')
                self.frame.place_forget()
                self.minilogo.place_forget()
                self.minipurple_text.place_forget()
                self.miniflash_text.place_forget()
                self.logo.place(y=30, x=430, anchor='n')
                self.purple_text.place(y=30, x=680, anchor='n')
                self.flash_text.place(y=150, x=680, anchor='n')
                return
            self.message_box.configure(text='')
            if len(pl.videos) >= 4:
                first = Image.open(BytesIO(request.urlopen(pl.videos[0].thumbnail_url).read()))
                first_width, first_height = first.size
                if first_width != first_height:
                    values = (((first_width - first_height) / 2), 0, ((first_width - first_height) / 2 + first_height), first_height)
                    first = first.crop(values)
                first = first.resize((74, 74))
                second = Image.open(BytesIO(request.urlopen(pl.videos[1].thumbnail_url).read()))
                second_width, second_height = second.size
                if second_width != second_height:
                    values = (((second_width - second_height) / 2), 0, ((second_width - second_height) / 2 + second_height), second_height)
                    second = second.crop(values)
                second = second.resize((74, 74))
                third = Image.open(BytesIO(request.urlopen(pl.videos[2].thumbnail_url).read()))
                third_width, third_height = third.size
                if third_width != third_height:
                    values = (((third_width - third_height) / 2), 0, ((third_width - third_height) / 2 + third_height), third_height)
                    third = third.crop(values)
                third = third.resize((74, 74))
                fourth = Image.open(BytesIO(request.urlopen(pl.videos[3].thumbnail_url).read()))
                fourth_width, fourth_height = fourth.size
                if fourth_width != fourth_height:
                    values = (((fourth_width - fourth_height) / 2), 0, ((fourth_width - fourth_height) / 2 + fourth_height), fourth_height)
                    fourth = fourth.crop(values)
                fourth = fourth.resize((74, 74))
                img = Image.new("RGB", (148, 148))
                img.paste(first, (0, 0))
                img.paste(second, (74, 0))
                img.paste(third, (0, 74))
                img.paste(fourth, (74, 74))
                imagem = CTkImage(img, size=(148, 148))
            else:
                img = Image.open(BytesIO(request.urlopen(pl.videos[0].thumbnail_url).read()))
                largura_original, altura_original = img.size
                imagem = CTkImage(img, size=((largura_original * 148 / altura_original), (148)))
            self.canvas.place_forget()
            self.clipImg.configure(image=imagem)
            self.clipName.configure(text=pl.title)
            self.clipAuthor.configure(text=pl.owner)
            self.canvas.config(cursor='arrow')
            
    def loading(self):
        if self.status1 == 'growing':
            self.raio1 += 1
            if self.raio1 == 31:
                self.status1 = 'decreasing'
                self.status2 = 'growing'
        if self.status1 == 'decreasing':
            self.raio1 -= 1
            if self.raio1 == 20:
                self.status1 = 'static'
        if self.status2 == 'growing':
            self.raio2 += 1
            if self.raio2 == 31:
                self.status2 = 'decreasing'
                self.status3 = 'growing' 
        if self.status2 == 'decreasing':
            self.raio2 -= 1
            if self.raio2 == 20:
                self.status2 ='static'
        if self.status3 == 'growing':
            self.raio3 += 1
            if self.raio3 == 31:
                self.status3 = 'decreasing'
        if self.status3 == 'decreasing':
            self.raio3 -= 1
            if self.raio3 == 20:
                self.status3 ='static'
        if self.status1 == 'static' and self.status2 == 'static' and self.status3 == 'static':
            self.status1 = 'growing'
        self.canvas.delete(ALL)
        self.canvas.create_aa_circle(667,95,self.raio1, fill='#7b2cbf')
        self.canvas.create_aa_circle(737,95,self.raio2, fill='#7b2cbf')
        self.canvas.create_aa_circle(807,95,self.raio3, fill='#7b2cbf')
        self.after(15, self.loading)
    
    def execDownload(self):
        if self.clipName.cget('text') != '':
            self.message_box.configure(text='Download em andamento...')
            thread = Thread(target=lambda :musicDownload(self.URL.get(), self.type_menu.get(), self.quality_menu.get(),
                            self.extension_menu.get(), Path(self.destination_label.cget('text'))))
        else:
            return
        thread.start()

# Configurações de load
if __name__ == '__main__':
    window()
