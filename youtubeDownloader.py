

import time

import threading
import os
import pickle
from moviepy.editor import AudioFileClip
from pytube import YouTube ,Playlist


def progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    with open("te.bin", 'wb') as fichier:
        print("path progress : " , os.getcwd())
        pickle.dump([round(pct_completed, 2), round(stream.filesize/ (1024 * 1024)  , 2) ], fichier)


def downloadPlaylist(link, type):
    clips = Playlist(link)
    for clip in clips.video_urls :
        print(clip)
        downloadVideoAudio(clip, type)
        print("1down")
def downloadVideoAudio(link, type):
    try:
        os.chdir('YTDownloads')
    except  FileNotFoundError:
        pass

    with open('te.bin', 'w'):
        print("create path : ", os.getcwd())

    clip = YouTube(link,on_progress_callback=progress)
    DownlaodClip(clip, type)


def DownlaodClip(clip ,type):

    if type == 'Mp4':
        video_clip = clip.streams.get_highest_resolution()
        video_clip.download("./YTDownloads", filename_prefix="OYTDownload_")
    else:
        audio_stream = clip.streams.filter(only_audio=True).first()
        download_directory = os.path.join(os.getcwd(), 'YTDownloads')
        audio_path = audio_stream.download()
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(os.path.join(os.getcwd(), f"OYTDownload_{clip.title}.mp3"))
        audio_clip.close()
        os.remove(audio_path)
    time.sleep(5)
    os.remove('te.bin')


def charger_valeur(nom_fichier):
    while True :
        time.sleep(7)
        try:
            os.chdir('YTDownloads')
        except  FileNotFoundError:
            pass

        try:
            with open(nom_fichier, 'rb') as fichier:
                print("mnin anakhd donnee : ", os.getcwd())

                valeur = pickle.load(fichier)
            print("Valeur chargée depuis le fichier binaire:", valeur)

        except FileNotFoundError:
            print("mnin anakhd donnee mnin manl9ahomch : ", os.getcwd())
            print("no data ")
        except EOFError :
            print("file vide")






if __name__ == '__main__':
    # link="https://www.youtube.com/watch?v=JkCLL1CzNZk&ab_channel=ElzeroWebSchool"
    print("test")

    playlist = "https://www.youtube.com/playlist?list=PLTEenozo5AuE2Bx9BylCKycSu-PtDbFml"
    #
    # threading.Thread(target=charger_valeur , daemon=True ,args=('te.bin',)).start()
    # # threading.Thread(target=downloadVideoAudio  ,args=(link,'Mp4')).start()
    # downloadPlaylist(playlist, 'Mp3')
