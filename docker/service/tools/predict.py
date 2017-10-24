from keras.models import load_model
from keras.applications.inception_v3 import decode_predictions
import numpy as np
import requests
import os
import sys
import subprocess
import extractor_py3 as ep3

def main():
    # X = np.loadtxt('sequences-003classes-005frames/v_ApplyEyeMakeup_g01_c01-5-features.txt')
    cmd = "./tools/convert.sh " + sys.argv[1]
    subprocess.call(cmd, shell=True)
    # sys.sleep(3)
    ep3.extract_features(sys.argv[1])
    feature_path = sys.argv[1] + "-features.txt"
    X = np.loadtxt(feature_path)
    test = np.zeros([1,np.shape(X)[0], np.shape(X)[1]])
    test[0,:,:] = X

    preds = model.predict(test)
    top5 = decode_predictions(preds,top=5)[0]
    predictions = [{'label': label, 'description': description, 'probability': probability * 100.0}
                    for label,description, probability in top5]
    return predictions

def predict(X):
    file_id = '0BxnNE6IbgiIJUTNtUVpiNjFIeVU'
    destination = 'tools/lstm-features.062-1.015.hdf5'
    if os.path.isfile(destination):
        print('Found model: ',destination)
    else: 
        print('Downloading ' + destination + '...')
        download_file_from_google_drive(file_id, destination)
    print('loading model...')
    model = load_model(destination)
    print('generating prediction...')
    prediction = model.predict(X)
    print(prediction)
    classes = ["Apply Eye Makeup","Apply Lipstick","Archery","Baby Crawling","Balance Beam","Band Marching","Baseball Pitch","Basketball Shooting","Basketball Dunk","Bench Press","Biking","Billiards Shot","Blow Dry Hair","Blowing Candles","Body Weight Squats","Bowling","Boxing Punching Bag","Boxing Speed Bag","Breaststroke","Brushing Teeth","Clean and Jerk","Cliff Diving","Cricket Bowling","Cricket Shot","Cutting In Kitchen","Diving","Drumming","Fencing","Field Hockey Penalty","Floor Gymnastics","Frisbee Catch","Front Crawl","Golf Swing","Haircut","Hammer Throw","Hammering","Handstand Pushups","Handstand Walking","Head Massage","High Jump","Horse Race","Horse Riding","Hula Hoop","Ice Dancing","Javelin Throw","Juggling Balls","Jump Rope","Jumping Jack","Kayaking","Knitting","Long Jump","Lunges","Military Parade","Mixing Batter","Mopping Floor","Nun chucks","Parallel Bars","Pizza Tossing","Playing Guitar","Playing Piano","Playing Tabla","Playing Violin","Playing Cello","Playing Daf","Playing Dhol","Playing Flute","Playing Sitar","Pole Vault","Pommel Horse","Pull Ups","Punch","Push Ups","Rafting","Rock Climbing Indoor","Rope Climbing","Rowing","Salsa Spins","Shaving Beard","Shotput","Skate Boarding","Skiing","Skijet","Sky Diving","Soccer Juggling","Soccer Penalty","Still Rings","Sumo Wrestling","Surfing","Swing","Table Tennis Shot","Tai Chi","Tennis Swing","Throw Discus","Trampoline Jumping","Typing","Uneven Bars","Volleyball Spiking","Walking with a dog","Wall Pushups","Writing On Board","Yo Yo"]
    print("Max probability: ", max(prediction[0]))
    print("Argmax: ", np.argmax(prediction[0]))
    print("Class: ", classes[np.argmax(prediction[0])])
    return prediction
    
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                
if __name__ == "__main__":
    main()
