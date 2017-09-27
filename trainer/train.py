"""
Train our RNN on bottlecap or prediction files generated from our CNN.
"""
import numpy as np
import pandas as pd
import tensorflow as tf
import cPickle as pickle
import time, csv, sys, argparse, random, os, glob
from tensorflow.python.lib.io import file_io
from subprocess import call
from keras.layers import Dense, Flatten, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential, load_model
from keras.optimizers import Adam
import keras.callbacks
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, CSVLogger
from keras.utils import np_utils

class CloudCheckpoint(keras.callbacks.Callback):
    def __init__(self, checkpoint_path, output_path, log_path):
        self.checkpoint_path = checkpoint_path
        self.log_path = log_path
        self.output_path = output_path
        self.saved = []

    def on_epoch_begin(self, epoch, logs={}):
        local = [a.split(self.checkpoint_path)[1].lstrip('/') for a in
                glob.glob(os.path.join(self.checkpoint_path, '*.hdf5'))]
        unsaved = [a for a in local if a not in self.saved]
        for item in unsaved:
            with file_io.FileIO(os.path.join(self.checkpoint_path, item),
                    mode='r') as input_f:
                with file_io.FileIO(os.path.join(self.output_path,
                    'checkpoints', item),
                        mode='w+') as output_f:
                    output_f.write(input_f.read())
            self.saved.append(item)

    def on_epoch_end(self, epoch, logs={}):
        local = [a.split(self.log_path)[1].lstrip('/') for a in
                glob.glob(os.path.join(self.log_path, '*.csv'))]
        unsaved = [a for a in local if a not in self.saved]
        for item in unsaved:
            with file_io.FileIO(os.path.join(self.log_path, item),
                    mode='r') as input_f:
                with file_io.FileIO(os.path.join(self.output_path,
                    'logs', item),
                        mode='w+') as output_f:
                    output_f.write(input_f.read())
            self.saved.append(item)

def train(seq_length, job_dir, job_type='local',
        batch_size=32, output_path=''):

    # Set variables
    nb_epoch = 1000
    timestamp = time.time()
    model_name = "trained-" + str(timestamp) + ".hdf5"
    early_stopper = EarlyStopping(patience=10)

    # Open files from cloud or locally for data file and training set
    if job_type == 'cloud':
        call(['gsutil', '-m', 'cp', '-r',
            'gs://lstm-training/sequences/40', '/tmp'])
        checkpoint_path = os.path.join('/tmp', 'checkpoints')
        log_path = os.path.join('/tmp', 'csv')
        try:
            os.mkdir(os.path.join(checkpoint_path))
        except OSError:
            pass
        checkpointer = ModelCheckpoint(
                filepath=os.path.join(checkpoint_path,
                '{epoch:03d}-{val_loss:.3f}.hdf5'),
                verbose=1, save_best_only=True)
        saver = CloudCheckpoint(checkpoint_path, output_path, log_path)
        tb = TensorBoard(log_dir=os.path.join(output_path, 'tb'))
        logger = CSVLogger(os.path.join('/tmp', 'csv',
            str(timestamp) + '.log'))
        callbacks = [early_stopper, tb, checkpointer, logger, saver]
        df = file_io.FileIO(os.path.join(job_dir,
            'data_file_' + seq_length + '.csv'), 'r')
    else:
        job_dir_output  = os.path.join(job_dir, os.environ['JOB_NAME'])
        os.mkdir(job_dir_output)
        os.mkdir(os.path.join(job_dir_output, 'tb'))
        os.mkdir(os.path.join(job_dir_output, 'csv'))
        os.mkdir(os.path.join(job_dir_output, 'checkpoints'))
        checkpointer = ModelCheckpoint(filepath=os.path.join(job_dir_output,
                'checkpoints',
                '{epoch:03d}-{val_loss:.3f}.hdf5'),
                verbose=1,
                save_best_only=True)
        tb = TensorBoard(log_dir=os.path.join(job_dir_output, 'tb'))
        csv_log_name = os.path.join(job_dir_output,
                'csv', str(timestamp) + '.log')
        csv_logger = CSVLogger(csv_log_name)
        callbacks = [checkpointer, tb, early_stopper, csv_logger]
        df = open(os.path.join(job_dir,
            'data_file_' + seq_length + '.csv'),'r')

    data_info = list(csv.reader(df))
    classes = get_classes(data_info)
    training_list, testing_list = separate_classes(data_info)
    steps_per_epoch = (len(data_info) * 0.7) // batch_size

    print "Dataset split:"
    print str(len(training_list)) + " training"
    print str(len(testing_list)) + " testing"

    if job_type == 'cloud':
        training_gen = sequence_generator_cl(training_list,
            classes,
            batch_size,
            job_dir,
            seq_length)
        validation_gen = sequence_generator_cl(testing_list,
            classes,
            batch_size,
            job_dir,
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
    print "Building lstm..."

    rm = build_lstm(len(classes), int(seq_length))

    print "Estimated model memory usage: " \
            + str(get_model_memory_usage(batch_size, rm))
    print "Starting up fit_generator..."

    hist = rm.fit_generator(
            generator=training_gen,
            steps_per_epoch=steps_per_epoch,
            epochs=nb_epoch,
            verbose=1,
            callbacks=callbacks,
            validation_data=validation_gen,
            validation_steps=10)

    
    if job_type == 'cloud':
        model_path = os.path.join('/tmp/', model_name)
        rm.save(model_path)
        call(['gsutil', 'cp', model_path, output_path])
    elif job_type == 'local':
        rm.save(os.path.join(job_dir_output, model_name))

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
            name = os.path.join('/tmp/40',
                sample + '-' + seq_length + '-features.pkl')
            vector = pd.read_pickle(name, compression='gzip')
            X.append(vector.values)
            y.append(get_class_one_hot(classes, sample.split('_')[1]))

        yield np.array(X), np.array(y)

def sequence_generator_l(set_list, classes, batch_size, job_dir, seq_length):
    while True:
        X, y = [], []
        for _ in range(batch_size):
            sample = random.choice(set_list)
            name = job_dir + '/sequences/' + seq_length + '/' \
                    + sample + '-' \
                    + seq_length + '-features.pkl'
            vector = pd.read_pickle(name, compression='gzip')
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
    parser.add_argument('--batch_size',
            default=32,
            help='batch size per step')
    parser.add_argument('--output_path',
            default='',
            help='cloud output directory based on job name')
    args, unknown = parser.parse_known_args()
    args = args.__dict__

    job_type = args.pop('job_type')
    job_dir = args.pop('job_dir')
    seq_length = args.pop('seq_length')
    batch_size = int(args.pop('batch_size'))
    output_path = args.pop('output_path')

    print "Starting with parameters:"
    print "job_type: " + job_type
    print "job_dir: " + job_dir
    print "output_path: " + output_path
    print "seq_length: " + seq_length
    print "batch_size: " + str(batch_size)

    train(seq_length, job_dir=job_dir, job_type=job_type, 
            batch_size=batch_size, output_path=output_path)
