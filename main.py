# Set your Cloudinary credentials
# ==============================
import pytube
from urllib.parse import quote
from flask import Flask, request, render_template
from flask_cors import CORS
from pathlib import Path

# Import the Cloudinary libraries
# ==============================
import cloudinary.api
import cloudinary.uploader
import cloudinary

# Import to format the JSON responses
# ==============================
import json

# Set configuration parameter: return "https" URLs by setting secure=true
# ==============================
config = cloudinary.config(secure=True)

# Backend
app = Flask(__name__)
CORS(app)

@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/upload-music', methods=["POST"])
def index():
    fichero = ""

    def segundos_a_segundos_minutos_y_horas(segundos):
        horas = int(segundos / 60 / 60)
        segundos -= horas*60*60
        minutos = int(segundos/60)
        segundos -= minutos*60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

    link = request.get_json(force=True)['url']
    yt = pytube.YouTube(link)
    print("\nDownloading...")
    print("Title: " + yt.title)
    fichero = f'{yt.title}.mp4'
    print("Author: " + yt.author)
    print("Duration: " + str(segundos_a_segundos_minutos_y_horas(yt.length)))

    yt_streams = yt.streams
    stream = yt_streams.first()
    stream.download(filename=fichero)
    print("Downloaded")

    file_path = fichero
    file_name = Path(file_path).stem

    # Upload the image and get its URL
    # ==============================

    # Upload the image.
    # Set the asset's public ID and allow overwriting the asset with new versions
    cloudinary.uploader.upload(fichero, resource_type='video', public_id=file_name,
                            unique_filename=True, overwrite=True, folder="music-mta/")

    # Log the image URL to the console.
    # Copy this URL in a browser tab to generate the image on the fly.
    print("\n****Upload an audio****")
    print(
        f'Delivery URL: https://res.cloudinary.com/del5cxt4n/video/upload/v1666749891/music-mta/{quote(file_path)}\n')

    response_data = {'url_direct': f'https://res.cloudinary.com/del5cxt4n/video/upload/v1666749891/music-mta/{quote(file_path)}'}
    return response_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

