"""
Train our RNN on bottlecap or prediction files generated from our CNN.
"""
import numpy as np
import pandas as pd
import tensorflow as tf
import cPickle as pickle
import time
import csv
import sys
import os.path
from tqdm import tqdm
from tensorflow.python.lib.io import file_io
from datetime import datetime
from keras.layers import Dense, Flatten, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from keras.utils import np_utils

abs_path = "/home/freeman/Documents/sd-gcp/"

def train(seq_length, job_type='local'):

    # Set variables
    nb_epoch = 1000
    batch_size = 12
    timestamp = time.time()
    model_name = "trained-" + str(timestamp) + ".hdf5"


    # Open files from cloud or locally for data file and training set
    if job_type == 'cloud':
        checkpointer = ModelCheckpoint(filepath='gs://lstm-training/checkpoints/{epoch:03d}-{val_loss:.3f}.hdf5',
                verbose=1, save_best_only=True)
        tb = TensorBoard(log_dir='gs://lstm-training/logs/tb')
        csv_logger = CSVLogger('gs://lstm-training/logs/csv' + str(timestamp) + '.log')
        df = file_io.FileIO('gs://lstm-training/data_file.csv', 'r')
        train_p = file_io.FileIO('gs://lstm-training/training.pickle', 'r')
        validation_p = file_io.FileIO('gs://lstm-training/validation.pickle', 'r')
        batch_size = 32
    else:
        checkpointer = ModelCheckpoint(filepath=abs_path + 'checkpoints/{epoch:03d}-{val_loss:.3f}.hdf5',
                verbose=1, save_best_only=True)
        tb = TensorBoard(log_dir=abs_path + 'logs/tb')
        csv_logger = CSVLogger('logs/csv' + str(timestamp) + '.log')
        df = open(abs_path + 'data_file.csv','r')
        train_p = open(abs_path + 'training.pickle', 'rb')
        validation_p = open(abs_path + 'validation.pickle', 'rb')
        batch_size = 12

    early_stopper = EarlyStopping(patience=10)
    data_info = list(csv.reader(df))
    classes = get_classes(data_info)

    print "Using batch size " + str(batch_size)
    print str(len(classes)) + " classes, " + str(len(data_info)) + " vectors listed"
    print "Unpickling and loading data into memory"

    # Load data from pickle into memory
    X = []
    y = []
    X_test = []
    y_test = []
    num_test = 0
    num_train = 0
    prog = tqdm(total=len(data_info))

    while True:
        try:
            vector = pickle.load(train_p)
            X.append(vector[1].values)
            y.append(get_class_one_hot(classes, vector[0].split('_')[1]))
            num_train += 1
        except EOFError:
            break
        prog.update()

    while True:
        try:
            vector = pickle.load(validation_p)
            X_test.append(vector[1].values)
            y_test.append(get_class_one_hot(classes, vector[0].split('_')[1]))
            num_test += 1
        except EOFError:
            break
        prog.update()

    prog.close()


    print str(num_train) + " actual vectors unpickled in train set"
    print str(num_test) + " actual vectors unpickled in test set"
    print "Building lstm of seq_length " + str(seq_length)

    rm = build_lstm(len(classes), seq_length)

    print "Beginning model fit."

    history = rm.fit(np.array(X), np.array(y),
        batch_size=batch_size,
        validation_data=(np.array(X_test), np.array(y_test)),
        verbose=1,
        callbacks=[checkpointer, tb, early_stopper, csv_logger],
        epochs=nb_epoch)

    score = rm.evaluate(X_test, y_test, verbose=1)
    rm.save(model_name)
    
    if job_type == 'cloud':
        with file_io.FileIO('model_name', mode='r') as in_f:
            with file_io.FileIO('gs://sd-training/' + model_name, mode = 'w+') as out_f:
                out_f.write(in_f.read())

def get_class_one_hot(classes, class_str):
    label_encoded = classes.index(class_str.lower())
    label_hot = np_utils.to_categorical(label_encoded, len(classes))
    label_hot = label_hot[0]
    return label_hot

def get_classes(data):
    classes = []
    for item in data:
        if item[1].lower() not in classes:
            classes.append(item[1].lower())
    classes = sorted(classes)
    return classes

def build_lstm(nb_classes, seq_length):
    model = Sequential()
    model.add(LSTM(2048,
        return_sequences=True,
        input_shape=(seq_length, 2048),
        dropout=0.5))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes, activation='softmax'))
    model.summary()
    optimizer = Adam(lr=1e-6)
    model.compile(loss='categorical_crossentropy',
                    optimizer=optimizer,
                    metrics=['accuracy','top_k_categorical_accuracy'])
    return model

if __name__ == '__main__':
    seq_length = 40
    job_type = sys.argv[1]
    print "Starting " + job_type + " job."
    train(seq_length, job_type=job_type)
