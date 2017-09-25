"""
Train our RNN on bottlecap or prediction files generated from our CNN.
"""
import numpy as np
import pandas as pd
import tensorflow as tf
import tables
import time
import csv
import sys
import argparse
import random
from tqdm import tqdm
from tensorflow.python.lib.io import file_io
from datetime import datetime
from keras.layers import Dense, Flatten, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from keras.utils import np_utils

def train(seq_length, job_dir, job_type='local'):

    # Set variables
    nb_epoch = 1000
    batch_size = 32
    timestamp = time.time()
    model_name = "trained-" + str(timestamp) + ".hdf5"
    early_stopper = EarlyStopping(patience=10)

    # Open files from cloud or locally for data file and training set
    if job_type == 'cloud':
        #checkpointer = ModelCheckpoint(filepath='gs://lstm-training/checkpoints/{epoch:03d}-{val_loss:.3f}.hdf5',
        #        verbose=1, save_best_only=True)
        tb = TensorBoard(log_dir=job_dir + '/logs/tb')
        #csv_logger = CSVLogger('gs://lstm-training/logs/csv' + str(timestamp) + '.log')
        callbacks = [early_stopper, tb]
        df = file_io.FileIO(job_dir + '/data_file.csv', 'r')
    else:
        checkpointer = ModelCheckpoint(filepath=job_dir \
                + '/checkpoints/{epoch:03d}-{val_loss:.3f}.hdf5',
                verbose=1, save_best_only=True)
        tb = TensorBoard(log_dir=job_dir + '/logs/tb')
        csv_logger = CSVLogger(job_dir + '/logs/csv' + str(timestamp) + '.log')
        callbacks = [checkpointer, tb, early_stopper, csv_logger]
        df = open(job_dir + '/data_file.csv','r')

    data_info = list(csv.reader(df))
    classes = get_classes(data_info)
    training_list, testing_list = separate_classes(data_info)
    steps_per_epoch = (len(data_info) * 0.7) // batch_size

    if job_type == 'cloud':
        training_gen = sequence_generator_cl(training_list,
            classes,
            batch_size,
            seq_length)
        validation_gen = sequence_generator_cl(testing_list,
            classes,
            batch_size,
            seq_length)
    elif job_type == 'local':
        training_gen = sequence_generator_l(training_list,
            classes,
            batch_size,
            job_dir,
            seq_length)
        validation_gen = sequence_generator_l(testing_list,
            classes,
            batch_size,
            job_dir,
            seq_length)


    print str(len(classes)) + " classes, " + str(len(data_info)) \
            + " vectors listed"
    print "Building lstm of seq_length " + str(seq_length)

    rm = build_lstm(len(classes), int(seq_length))

    print "Estimated model memory usage: " \
            + str(get_model_memory_usage(batch_size, rm))
    print "Starting fit_generator."

    hist = rm.fit_generator(
            generator=training_gen,
            steps_per_epoch=steps_per_epoch,
            epochs=nb_epoch,
            verbose=1,
            callbacks=callbacks,
            validation_data=validation_gen,
            validation_steps=10)

    #score = rm.evaluate(X_test, y_test, verbose=1)
    rm.save(model_name)
    
    if job_type == 'cloud':
        with file_io.FileIO(model_name, mode='r') as in_f:
            with file_io.FileIO('gs://lstm-training/models/' + model_name, mode = 'w+') as out_f:
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

def separate_classes(data):
    train, test = [], []
    for item in data:
        if item[0] == 'train':
            train.append(item[2])
        elif item[0] == 'test':
            test.append(item[2])
    return train, test

def sequence_generator_cl(set_list, classes, batch_size, job_dir, seq_length):
    while True:
        X, y = [], []
        for _ in range(batch_size):
            sample = random.choice(set_list)
            name = file_io.FileIO(job_dir + sample + '-' \
                    + seq_length + '-features.txt', 'r')
            vector = pd.read_csv(name, sep=" ", header=None)
            X.append(vector.values)
            y.append(get_class_one_hot(classes, sample.split('_')[1]))

        yield np.array(X), np.array(y)

def sequence_generator_l(set_list, classes, batch_size, job_dir, seq_length):
    while True:
        X, y = [], []
        for _ in range(batch_size):
            sample = random.choice(set_list)
            name = job_dir + '/sequences/' + sample + '-' \
                    + seq_length + '-features.txt'
            vector = pd.read_csv(name, sep=" ", header=None)
            X.append(vector.values)
            y.append(get_class_one_hot(classes, sample.split('_')[1]))

        yield np.array(X), np.array(y)

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

# From https://stackoverflow.com/questions/43137288/how-to-determine-needed-memory-of-keras-model
def get_model_memory_usage(batch_size, model):
    from keras import backend as K

    shapes_mem_count = 0
    for l in model.layers:
        single_layer_mem = 1
        for s in l.output_shape:
            if s is None:
                continue
            single_layer_mem *= s
        shapes_mem_count += single_layer_mem

    trainable_count = int(np.sum([K.count_params(p) for p in set(model.trainable_weights)]))
    non_trainable_count = int(np.sum([K.count_params(p) for p in set(model.non_trainable_weights)]))

    total_memory = 4*batch_size*(shapes_mem_count + trainable_count + non_trainable_count)
    gbytes = round(total_memory / (1024 ** 3), 3)
    return gbytes

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Run a training job for the lstm')
    parser.add_argument('--job_type',
            help='cloud or local job')
    parser.add_argument('--job_dir',
            help='local or cloud location to get resources and write outputs',
            required=True)
    parser.add_argument('--seq_length',
            help='length of a sequence in frames',
            required=True)
    args = parser.parse_args().__dict__

    job_type = args.pop('job_type')
    job_dir = args.pop('job_dir')
    seq_length = args.pop('seq_length')

    print "Starting " + job_type + " job. Directory is " + job_dir

    train(seq_length, job_dir=job_dir, job_type=job_type)
