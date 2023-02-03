from flask import Flask, render_template, request, send_file

import youtube_dl
import os
import sys

app = Flask(__name__)

TYPE = 'mp3'

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result", methods= ['POST', 'GET'])
def result():
    global TYPE
    output = request.form.to_dict()
    URL = output["URL"]
    TYPE = output["type"]

    if URL and TYPE:
        if TYPE == 'mp3':
            YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{os.getcwd()}/media.mp3'
            }

        elif TYPE == 'mp4':
            YDL_OPTIONS = {
            'format': 'mp4',
            'outtmpl': f'{os.getcwd()}/media.mp4'
            }

        if os.path.isfile(f"{os.getcwd()}/media.{TYPE}"):
            os.remove(f"{os.getcwd()}/media.{TYPE}")

        if os.path.isfile(f"{os.getcwd()}/media.{TYPE}.part"):
            os.remove(f"{os.getcwd()}/media.{TYPE}.part")

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info_dict = ydl.extract_info(URL, download=False)
            video_title = info_dict.get('title', None)
            try:
                ydl.download([URL])
            except:
                return render_template("index.html", message="Error trying to download video, please try other")

        return render_template("index.html", URL=URL, TYPE=TYPE, video_title=video_title, message="Downloaded {{video_title}} in type {{TYPE}}")


    return render_template("index.html", URL=URL, TYPE=TYPE, message="")

@app.route('/download')
def download_file():
    filename = 'media.' + TYPE
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug= True, port=5001)
