from customtkinter import *
from tkinter import filedialog
from PIL import Image
from threading import Thread
from pathlib import Path
from moviepy.editor import *
from urllib import request
from io import BytesIO
import pytube

class App(CTk):
    def __init__(self):
        super().__init__()
        # Configurações da Janela
        self.title('Purple Flash')
        self._set_appearance_mode('dark')
        self.geometry(f"1200x600+{int(self.winfo_screenwidth()/2-600)}+{int(self.winfo_screenheight()/2-300)}")
        self.resizable(width=False, height=False)
        try:
            self.iconbitmap('img/icon.ico')
        except Exception as e:
            print(f"Error setting icon: {e}")

        # Pegar o diretorio padrão da pasta downloads do pc do usuário
        downloads_directory = Path.home() / "Downloads"
        if downloads_directory.is_dir() is False:
            downloads_directory = 'Selecione uma pasta para download'
        
        # Configurações dos Widgets
        self.logo = CTkLabel(master=self, text='', image=CTkImage(Image.open('img/icone.png'), size=(300, 300)))
        self.logo.place(y=40, x=400, anchor='n')
        self.purple_text = CTkLabel(master=self, text='PURPLE', font=('Arial', 103), text_color='#7b2cbf')
        self.purple_text.place(y=70, x=710, anchor='n')
        self.flash_text = CTkLabel(master=self, text='FLASH', font=('Arial', 130), text_color='#7b2cbf')
        self.flash_text.place(y=170, x=710, anchor='n')
        self.URL = CTkEntry(master=self, placeholder_text='Link da playlist, vídeo ou música', border_color='#7b2cbf',
                        placeholder_text_color='#7b2cbf', font=('Roboto', 18), corner_radius=12, width=800)
        self.URL.place(x=170, y=390)
        self.serch_button = CTkButton(master=self, text='', fg_color='#7b2cbf', hover_color='#5a189a',
                                      image=CTkImage(Image.open("img/search.png"), size=(20, 20)), 
                                      corner_radius=12, width=50, command=self.validUrl)
        self.serch_button.place(x=1000, y=390, anchor='n')

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
                                corner_radius=10, width=120, anchor='center', values=['Áud/Víd', 'Áudio 🔊', 'Vídeo 📺'],
                                command=self.formatSelection)
        self.type_menu.place(x=390, y=450, anchor='nw')
        self.directory_button = CTkButton(master=self, text='Diretório', fg_color='#7b2cbf', hover_color='#5a189a', 
                                font=('Roboto', 20), corner_radius=12, width=120, anchor='center', command=self.flashSelection,
                                image=CTkImage(Image.open("img/folder.png"), size=(25, 25)), compound="right")
        self.directory_button.place(x=390, y=488, anchor='nw')
        self.destination_label = CTkLabel(master=self, text=downloads_directory, text_color='#7b2cbf', font=('Roboto', 20))
        self.destination_label.place(x=535, y=488, anchor='nw')
        self.download_button = CTkButton(master=self, text='Download', fg_color='#7b2cbf', font=('Roboto', 20), 
                                hover_color='#5a189a', corner_radius=12, width=170)
        self.download_button.place(x=600, y=530, anchor='n')
    
    def validUrl(self):
        self.serch_button.configure(state='disabled')
        # Tratamento de erros
        url = self.URL.get()
        if url == "":
            self.serch_button.configure(state='normal')
            self.message_box.configure(text='')
            return
        if url.count('youtube.com/') != 1 and url.count("youtu.be/") != 1:
            self.serch_button.configure(state='normal')
            self.message_box.configure(text="URL inválida!")
            return
        
        # Vídeo isolado
        if url.find('list') == -1:
            try:
                pytube.YouTube(url).streams
            except Exception as e:
                self.serch_button.configure(state='normal')
                self.message_box.configure(text=f'Ocorreu um erro! {e}')
                return
        # Playlist
        else:
            try:
                pl = pytube.Playlist(url)
                pl.videos[0].streams
            except Exception as e:
                self.serch_button.configure(state='normal')
                self.message_box.configure(text=f'Ocorreu um erro! {e}')
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

    def formatSelection(self, value):
        if value == 'Áud/Víd':
            formatos = ['mp4', 'mov', 'wkv', 'm4v', 'webm']
            vformato = StringVar()
            vformato.set(formatos[0])
        elif value == 'Áudio 🔊':
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
    

app = App()
app.mainloop()
