# -*- coding: utf-8 -*-
import os
import sys
import json
import base64
import config
import logging
import storage
import urllib
import urllib2
import requests
from flask import current_app, Flask, render_template, request
from google.appengine.api import images
from google.appengine.ext import blobstore
# from urlgrabber.keepalive import HTTPHandler

app = Flask(__name__)
app.config.from_object(config)

logging.basicConfig(level=logging.INFO)

def upload_video_file(stream, filename, content_type):
    if not stream:
        return None

    bucket_filepath = storage.upload_file(
        stream,
        filename,
        content_type
    )

    logging.info(
        "Uploaded file %s as %s.", filename, bucket_filepath)

    bucket = bucket_filepath[bucket_filepath.find("/")+1:bucket_filepath.rfind("/")]
    filename = bucket_filepath[bucket_filepath.rfind("/")+1:]

    file_url = "https://" + "sd-lstm.appspot.com" + ".storage.googleapis.com/" + filename
    return file_url

def fetch_predictions(vid_url, f):
    predictions = {}
    username = 'dev'
    password = 'dogclock'
    server_url = current_app.config['PREDICTION_SERVICE_URL']
    values = { 'username': username, 'password': password, 'data': vid_url, 'file_name': f}
    data = json.dumps(values)
    logging.info('URL: %s', vid_url)

    req = requests.post(server_url, data=data, headers={'Content-Type': 'application/json'}, timeout=180)
    predictions = req.json()

    logging.info('Prediction Type 1: %s', type(predictions))
    try:
        predictions = predictions['predictions']
        logging.info('Prediction Type 2: %s', type(predictions))
        
    except Exception:
        logging.info('DIDNT WORK')

    return predictions

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/video.html')
def video():
    return render_template('video.html')

@app.route('/video', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        vid = request.files.get('video')

        vid_stream = vid.read()
        filename = vid.filename
        content_type = vid.content_type

        temp = filename[:filename.rfind(".")]
        temp = temp.replace(".", "-")
        filename = temp + filename[filename.rfind("."):]

        video_url = upload_video_file(vid_stream, filename, content_type)

        predictions = fetch_predictions(vid_url=video_url, f=filename)

        try:
            top1 = predictions["label1"]
            top2 = predictions["label2"]
            top3 = predictions["label3"]
            top4 = predictions["label4"]
            top5 = predictions["label5"]

            prob1 = predictions["prob1"]
            prob2 = predictions["prob2"]
            prob3 = predictions["prob3"]
            prob4 = predictions["prob4"]
            prob5 = predictions["prob5"]

            return render_template('video.html', video_url=video_url, file_name=filename, 
                one=top1, two=top2, three=top3, four=top4, five=top5,
                p_one=prob1, p_two=prob2, p_three=prob3, p_four=prob4, p_five=prob5)

        except Exception:
            return render_template('video.html', video_url=video_url)

@app.errorhandler(500)
def server_error(e):
    logging.error('An error occurred during a request. %s', e)
    err = "An error occurred during a request." + str(e)
    return err, 500 # 'An internal error occurred.', 500
