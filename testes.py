import pytube
import os
from PIL import Image
import customtkinter
import requests
from io import BytesIO
from urllib import request

yt = pytube.YouTube('https://www.youtube.com/watch?v=3fHl9bxVT58')
vid = yt.streams
thumb = yt.thumbnail_url
root = customtkinter.CTk()


response = request.urlopen(thumb)
imagem_bytes = BytesIO(response.read())
img = Image.open(imagem_bytes)
largura_original, altura_original = img.size
print(largura_original, ' ', altura_original)
imagem = customtkinter.CTkImage(img, size=((largura_original), (altura_original)))
label = customtkinter.CTkLabel(master=root, image=imagem, text='')
label.pack()

root.mainloop()
