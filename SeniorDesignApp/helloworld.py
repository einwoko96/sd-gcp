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


@app.route('/video', methods=['POST'])
def infer():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'vid' not in request.files:
            return "Request does not contain a file.", 400
        files = request.files['vid']
        # if user does not select file, browser also
        # submit a empty part without filename
        if files.filename == '':
            return "Empty filename.", 400
        if files:
            files.save(os.path.join(files.filename))
#            answer = run_inference_on_image()
            predicted_categories, top5_labels, top5_proba = image_to_category('upload.jpg')
            print(predicted_categories)
            print(top5_labels)
            print(top5_proba)
            return render_template('video.html', categories=predicted_categories, dish=top5_labels[0], prob=top5_proba[0])

@app.route('/upload.jpg')
def uploaded_jpg():
    return send_file('./upload.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run()