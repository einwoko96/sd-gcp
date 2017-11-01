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
    print(f)
    data = json.dumps(values)
    # req = urllib2.Request(server_url, data, {'Content-Type': 'application/json'})
    # keepalive_handler = HTTPHandler()
    # opener = urllib2.build_opener(keepalive_handler)
    # urllib2.install_opener(opener)
    req = requests.get(server_url, data=data, headers={'Content-Type': 'application/json'}, timeout=120)
    predictions = req.json()

    # try:
    #     f = urllib2.urlopen(req)
    #     predictions = json.loads(f.read())
    # except urllib2.HTTPError as e:
    #     logging.exception(e)

    logging.info('Predictions: %s', predictions)

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
        video_url = upload_video_file(vid_stream, filename, content_type)

        predictions = fetch_predictions(vid_url=video_url, f=filename)

        try:
            top1 = predictions["label1"]

            top2 = predictions["label2"]

            top3 = predictions["label3"]

            top4 = predictions["label4"]

            top5 = predictions["label5"]

            return render_template('video.html', video_url=video_url, file_name=filename, one=top1, two=top2, three=top3, four=top4, five=top5)
        except Exception:

            return render_template('video.html', video_url=video_url)

@app.errorhandler(500)
def server_error(e):
    logging.error('An error occurred during a request.')
    return 'An internal error occurred.', 500