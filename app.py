import time
from flask import Flask, jsonify, render_template, request, redirect, url_for
import threading
import os
import pickle
from moviepy.editor import AudioFileClip
from pytube import YouTube , Playlist
import facFunction
from flask_mail import Mail, Message
from dotenv import load_dotenv 

load_dotenv()
COUNTER = 0
app = Flask(__name__, template_folder="templates")
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "othmandone@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv('MY_SECRET_KEY')
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)

TYPE=('Mp3','Mp4')
def progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    pct_completed = bytes_downloaded / total_size * 100
    with open("te.bin", 'wb') as fichier:
        pickle.dump([round(pct_completed, 2), round(stream.filesize/ (1024 * 1024)  , 2) ], fichier)


def downloadPlaylist(link, type):
    global COUNTER
    COUNTER = 0
    clips = Playlist(link)
    for clip in clips.video_urls :
        downloadVideoAudio(clip, type)
        COUNTER += 1


def downloadVideoAudio(link, type):
    with open('te.bin', 'w'):
        pass
    clip = YouTube(link,on_progress_callback=progress)
    DownlaodClip(clip, type)


def DownlaodClip(clip ,type):
    if type == 'Mp4':
        video_clip = clip.streams.get_highest_resolution()
        video_clip.download(filename_prefix="OYTDownload_")
    else:
        audio_stream = clip.streams.filter(only_audio=True).first()
        audio_path = audio_stream.download()
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(os.path.join(os.getcwd(), f"OYTDownload_{clip.title}.mp3"))
        audio_clip.close()
        os.remove(audio_path)
    time.sleep(5)
    os.remove('te.bin')
    
    

    

@app.route('/', methods=['POST' , 'GET'] )
def index():
    if 'YTDownloads' not in os.getcwd():
        os.chdir('YTDownloads')
    if request.method == 'GET':
        return  render_template("index.html")
    elif request.method == 'POST' :
        url = request.form.get('url')
        typeDownload = request.form.get('typeDownload')
        fullNameContactUs  = request.form.get('fullNameContactUs')
        emailContactUs  = request.form.get('emailContactUs')
        textContactUs  = request.form.get('textContactUs')
        if url and typeDownload in TYPE:
            return  redirect(url_for('loading',url=url , typeDownload=typeDownload) )
        elif fullNameContactUs and  emailContactUs and textContactUs :
            fullNameContactUs = request.form.get('fullNameContactUs')
            emailContactUs = request.form.get('emailContactUs')
            textContactUs = request.form.get('textContactUs')
            if len(textContactUs.strip()) != 0 :
                msg = Message(fullNameContactUs,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[emailContactUs])
                msg.body = textContactUs
                mail.send(msg)
                return redirect(url_for('mailSent'))
            else :
                return "<h1>The message email is Empty </h1>"

        else :
            return "<h1> Internal Error Occurs , Try to Reload the back to the Home Page </h1>"

@app.route('/mailSent', methods=['POST','GET'])
def mailSent():
    return "good"


@app.route('/loading', methods=[ 'POST','GET'])
def loading():
    url = request.args.get('url')
    typeDownload = request.args.get('typeDownload')
    clip = YouTube(url)
    thread = threading.Thread(target=downloadVideoAudio, daemon=True ,  args=(url, typeDownload))
    thread.start()
    # if thread.is_alive():
    #     print("Thread is running")
    # else:
    #     print("Thread is not running")
    return render_template("loading.html" , author=clip.author  ,videoTitle=clip.title  , duration= facFunction.elemnt_length(clip.length)  , thumbnail_url=clip.thumbnail_url , publish_date=clip.publish_date.date() )

@app.route('/get_progress', methods=['GET'])
def get_number():
    try:
        with open('te.bin', 'rb') as fichier:
            value = pickle.load(fichier)
            return jsonify({'number': float(value[0]), 'filesize': float(value[1])})
    except FileNotFoundError:
        return jsonify({'number': 100.0})
    except EOFError:
        return jsonify({'number': 0.0, 'filesize': 0.0})
    except ValueError:
        return jsonify({'error': 'Invalid data in file'})


@app.route('/switch' , methods=['POST' , 'GET'] )
def switch():
    if request.method == 'GET' :
        return render_template("playlist.html")
    elif request.method == 'POST' :
        url = request.form.get('url')
        typeDownload = request.form.get('typeDownload')
        if url and typeDownload in TYPE:
            return  redirect(url_for('loadingp',url=url , typeDownload=typeDownload) )
        else :
            return "hack2"

@app.route('/loadingp', methods=[ 'POST','GET'])
def loadingp():
    url = request.args.get('url')
    typeDownload = request.args.get('typeDownload')
    clip = Playlist(url)
    thread = threading.Thread(target=downloadPlaylist, daemon=True ,  args=(url, typeDownload))
    thread.start()
    # if thread.is_alive():
    #     print("Thread is running")
    # else:
    #     print("Thread is not running")
    thum=clip.sidebar_info[0]['playlistSidebarPrimaryInfoRenderer']["thumbnailRenderer"]["playlistVideoThumbnailRenderer"]["thumbnail"]["thumbnails"][0]['url']
    return render_template("loadingp.html" , author=clip.owner  ,videoTitle=clip.title  , length= clip.length   , thumbnail_url=thum  )

@app.route('/get_progress_p', methods=['GET'])
def get_number_p():
    return jsonify({'counter' : COUNTER})




if __name__ == '__main__':
    app.run(host='0.0.0.0' ,debug=True, port=9999)
