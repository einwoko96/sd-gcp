from keras.models import load_model
import numpy as np
import requests
import os


def main():
    # X = np.loadtxt('sequences-003classes-005frames/v_ApplyEyeMakeup_g01_c01-5-features.txt')
    X = np.loadtxt('tools/gunalan-features.txt')
    test = np.zeros([1,np.shape(X)[0], np.shape(X)[1]])
    test[0,:,:] = X
    predict(test)

def predict(X):
    file_id = '0BxnNE6IbgiIJUTNtUVpiNjFIeVU'
    destination = 'lstm-features.062-1.015.hdf5'
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
    print("Max probability: ", max(prediction[0]))
    print("Argmax: ", np.argmax(prediction[0]))
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
