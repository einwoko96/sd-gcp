from flask import Flask, current_app, request, jsonify
import io
import sys
import json
import base64
import logging
import subprocess
import numpy as np
sys.path.insert(0, 'tools')
import extractor_py3 as ep3
from predict import predict
import urllib
from multiprocessing import Pool
import requests
from keras.models import load_model
from predict import download_file_from_google_drive
import os
from werkzeug.datastructures import MultiDict

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def pred():
    data = ""
    found = False
    try:
        data = request.get_json()['data']
    except Exception:
        return jsonify(status_code='400', msg='Bad Request'), 400

    # data = "https://sd-lstm.appspot.com.storage.googleapis.com/terrain_w1anmt8er__PM-2017-10-23-000514.mp4"
    # data = "tools/juggling.MOV"
    current_app.logger.info('Data: %s', data)

    if 'http' in data:
        cmd = "./tools/convert_http.sh " + data + " tools/" + data[data.rfind("/")+1:data.rfind(".")]
    else:
        cmd = "./tools/convert.sh " + data + " " + data[:data.rfind(".")]

    data = "tools/" + data[data.rfind("/")+1:data.rfind(".")]
    print("CMD: " + cmd)
    subprocess.check_output(cmd, shell=True)
    data = ep3.extract_features(data)
    # feature_path = data + "-features.txt"
    X = np.loadtxt(data)
    test = np.zeros([1,np.shape(X)[0], np.shape(X)[1]])
    test[0,:,:] = X
    if not 'trained_lstm_model' in globals():
        init_model()
    preds = trained_lstm_model.predict(test)
    classes = ["Apply Eye Makeup","Apply Lipstick","Archery","Baby Crawling","Balance Beam","Band Marching","Baseball Pitch","Basketball Shooting","Basketball Dunk","Bench Press","Biking","Billiards Shot","Blow Dry Hair","Blowing Candles","Body Weight Squats","Bowling","Boxing Punching Bag","Boxing Speed Bag","Breaststroke","Brushing Teeth","Clean and Jerk","Cliff Diving","Cricket Bowling","Cricket Shot","Cutting In Kitchen","Diving","Drumming","Fencing","Field Hockey Penalty","Floor Gymnastics","Frisbee Catch","Front Crawl","Golf Swing","Haircut","Hammer Throw","Hammering","Handstand Pushups","Handstand Walking","Head Massage","High Jump","Horse Race","Horse Riding","Hula Hoop","Ice Dancing","Javelin Throw","Juggling Balls","Jump Rope","Jumping Jack","Kayaking","Knitting","Long Jump","Lunges","Military Parade","Mixing Batter","Mopping Floor","Nun chucks","Parallel Bars","Pizza Tossing","Playing Guitar","Playing Piano","Playing Tabla","Playing Violin","Playing Cello","Playing Daf","Playing Dhol","Playing Flute","Playing Sitar","Pole Vault","Pommel Horse","Pull Ups","Punch","Push Ups","Rafting","Rock Climbing Indoor","Rope Climbing","Rowing","Salsa Spins","Shaving Beard","Shotput","Skate Boarding","Skiing","Skijet","Sky Diving","Soccer Juggling","Soccer Penalty","Still Rings","Sumo Wrestling","Surfing","Swing","Table Tennis Shot","Tai Chi","Tennis Swing","Throw Discus","Trampoline Jumping","Typing","Uneven Bars","Volleyball Spiking","Walking with a dog","Wall Pushups","Writing On Board","Yo Yo"]

    top1 = classes[np.argmax(preds[0])]
    preds[0][np.argmax(preds[0])] = -1

    top2 = classes[np.argmax(preds[0])]
    preds[0][np.argmax(preds[0])] = -1

    top3 = classes[np.argmax(preds[0])]
    preds[0][np.argmax(preds[0])] = -1

    top4 = classes[np.argmax(preds[0])]
    preds[0][np.argmax(preds[0])] = -1

    top5 = classes[np.argmax(preds[0])]
    preds[0][np.argmax(preds[0])] = -1

    predictions = {'label1': top1, 'label2': top2, 'label3': top3, 'label4': top4, 'label5': top5}
    current_app.logger.info('Predictions: %s', predictions)

    return jsonify(predictions=predictions)

def init_model():
    global trained_lstm_model
    file_id = '0BxnNE6IbgiIJUTNtUVpiNjFIeVU'
    destination = 'tools/lstm-features.062-1.015.hdf5'
    if os.path.isfile(destination):
        print('Found model: ',destination)
    else: 
        print('Downloading ' + destination + '...')
        download_file_from_google_drive(file_id, destination)
    print('loading model...')
    trained_lstm_model = load_model(destination)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
#    init_model()
