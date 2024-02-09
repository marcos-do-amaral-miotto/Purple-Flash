import pytube
import os

def musicDownload():
    destination = r'C:\Users\marcos_miotto\Desktop'
    yt = pytube.YouTube('https://www.youtube.com/watch?v=YDDz1Er2IXA&list=RDMMYDDz1Er2IXA&start_radio=1')
    vid = yt.streams.filter(type='video', file_extension='mp4')
    print(yt.streams.filter(type='video', file_extension='mp4', progressive=True).get_highest_resolution())
    # for i in vid:
    #     print(i)
musicDownload()
# .download(output_path=destination)