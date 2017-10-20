# -*- coding: utf-8 -*-
import os
import sys
tastemaker = os.path.dirname(os.getcwd())
sys.path.append(tastemaker)

from flask import Flask, render_template, send_file, request
app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return render_template('video.html')


@app.route('/infer', methods=['POST'])
def infer():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'pic' not in request.files:
            return "Request does not contain a file.", 400
        file = request.files['pic']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "Empty filename.", 400
        
@app.route('/upload.jpg')
def uploaded_jpg():
    return send_file('./upload.jpg', mimetype='image/jpeg')

@app.route('/style.css')
def style():
    return send_file('./style.css', mimetype='text/css')

if __name__ == '__main__':
    app.run()