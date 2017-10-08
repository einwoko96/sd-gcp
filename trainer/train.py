"""
Train our RNN on bottlecap or prediction files generated from our CNN.
"""
import numpy as np
import pandas as pd
import tensorflow as tf
import cPickle as pickle
import time, csv, sys, argparse, random, os, glob
from tensorflow.python.lib.io import file_io
from subprocess import call, Popen
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

    def on_epoch_begin(self, epoch, logs={}):
        Popen(['gsutil', '-m', 'mv',
            os.path.join(checkpoint_path, epoch + '*.hdf5'),
            os.path.join(output_path, 'checkpoints')],
            stdin=None, stdout=None,
            stderr=None, close_fds=True)

    def on_epoch_end(self, epoch, logs={}):
        Popen(['gsutil', 'cp', os.path.join(log_path, '*.log'),
            os.path.join(output_path, 'logs')],
            stdin=None, stdout=None,
            stderr=None, close_fds=True)

class Trainer():
    def __init__(self, **kwargs):
        self.job_type = kwargs['job_type']
        self.seq_length = kwargs['seq_length']
        self.batch_size = kwargs['batch_size']
        self.job_dir = kwargs['job_dir']
        if kwargs['job_type'] == 'cloud':
            self.data_dir = os.path.join('/tmp/', 'sequences',
                    kwargs['data_dir'])
            self.output_path = kwargs['output_path']
        else:
            self.data_dir = os.path.join(kwargs['job_dir'],
                    'sequences', kwargs['data_dir'])
            self.output_path = os.path.join(self.job_dir,
                os.environ['JOB_NAME'])
        self.classes = []
        self.train_set = []
        self.test_set = []

    def train(self):

        nb_epoch = 1000
        timestamp = time.time()
        model_name = "trained-" + str(timestamp) + ".hdf5"
        early_stopper = EarlyStopping(patience=10)

        # Open files from cloud or locally for data file and training set
        if self.job_type == 'cloud':
            # copies the whole dataset to /tmp
            call(['gsutil', '-m', 'cp', '-r',
                os.path.join(self.job_dir, 'sequences', self.data_dir),
                '/tmp'])
            checkpoint_path = os.path.join('/tmp', 'checkpoints')
            log_path = os.path.join('/tmp', 'logs')
            try:
                os.mkdir(checkpoint_path)
                os.mkdir(log_path)
            except OSError:
                pass
            checkpointer = ModelCheckpoint(
                    filepath=os.path.join(checkpoint_path,
                    '{epoch:03d}-{val_loss:.3f}.hdf5'),
                    verbose=1, save_best_only=True)
            saver = CloudCheckpoint(checkpoint_path, self.output_path, log_path)
            tb = TensorBoard(log_dir=os.path.join(output_path, 'tb'))
            logger = CSVLogger(os.path.join(log_path,
                'lstm_train_' + str(timestamp) + '.log'))
            callbacks = [early_stopper, tb, checkpointer, logger, saver]
            df = file_io.FileIO(os.path.join(job_dir,
                'class_list_' + self.data_dir + '.csv'), 'r')
        else:
            os.mkdir(self.output_path)
            os.mkdir(os.path.join(self.output_path, 'tb'))
            os.mkdir(os.path.join(self.output_path, 'csv'))
            os.mkdir(os.path.join(self.output_path, 'checkpoints'))
            checkpointer = ModelCheckpoint(
                    filepath=os.path.join(self.output_path,
                    'checkpoints',
                    '{epoch:03d}-{val_loss:.3f}.hdf5'),
                    verbose=1,
                    save_best_only=True)
            tb = TensorBoard(log_dir=os.path.join(self.output_path, 'tb'))
            csv_log_name = os.path.join(self.output_path,
                    'csv', str(timestamp) + '.log')
            csv_logger = CSVLogger(csv_log_name)
            callbacks = [checkpointer, tb, early_stopper, csv_logger]
            df = open(os.path.join(self.job_dir,
                'class_list_' + os.path.basename(self.data_dir) + '.csv'),'r')

        self.classes = df.read().strip('\r\n').lower().split(',')
        self.separate_classes()
        steps_per_epoch = (len(self.classes) * 0.7) // self.batch_size

        print str(len(self.classes)) + " classes listed."
        print str(len(self.train_set)) + " marked as training."
        print str(len(self.test_set)) + " marked as testing."

        training_gen = self.sequence_generator(self.train_set)
        validation_gen = self.sequence_generator(self.test_set)

        print "Building lstm..."

        rm = self.build_lstm()

        print "Starting up fit_generator..."

        hist = rm.fit_generator(
                generator=training_gen,
                steps_per_epoch=steps_per_epoch,
                epochs=nb_epoch,
                verbose=1,
                callbacks=callbacks,
                validation_data=validation_gen,
                validation_steps=10)

    
        if self.job_type == 'cloud':
            model_path = os.path.join('/tmp', model_name)
            rm.save(model_path)
            call(['gsutil', 'cp', model_path, self.output_path])
        elif self.job_type == 'local':
            rm.save(os.path.join(self.output_path, model_name))

    def get_class_one_hot(self, class_str):
        label_encoded = self.classes.index(class_str.lower())
        label_hot = np_utils.to_categorical(label_encoded, len(self.classes))
        label_hot = label_hot[0]
        return label_hot

    def separate_classes(self):
        for item in glob.glob(os.path.join(self.data_dir, '*.pkl')):
            if 'train' in item:
                self.train_set.append(os.path.basename(item))
            elif 'test' in item:
                self.test_set.append(os.path.basename(item))

    def sequence_generator(self, set_list):
        while True:
            X, y = [], []
            for _ in range(self.batch_size):
                sample = random.choice(set_list)
                name = os.path.join(self.data_dir, sample)
                vector = pd.read_pickle(name, compression='gzip')
                X.append(vector.values)
                y.append(self.get_class_one_hot(sample.split('_')[1]))

            yield np.array(X), np.array(y)

    def build_lstm(self):
        model = Sequential()
        model.add(LSTM(2048,
            return_sequences=True,
            input_shape=(self.seq_length, 2048),
            dropout=0.5))
        model.add(Flatten())
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.classes), activation='softmax'))
        model.summary()
        optimizer = Adam(lr=1e-6)
        model.compile(loss='categorical_crossentropy',
                optimizer=optimizer,
                metrics=['accuracy','top_k_categorical_accuracy'])
        return model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Run a training job for the lstm')
    parser.add_argument('--job_type',
            help='cloud or local job')
    parser.add_argument('--job_dir',
            help='local or cloud location to get resources and write outputs',
            required=True)
    parser.add_argument('--seq_length',
            type=int,
            help='length of a sequence in frames',
            required=True)
    parser.add_argument('--batch_size',
            default=32,
            type=int,
            help='batch size per step')
    parser.add_argument('--output_path',
            default='',
            help='cloud output directory based on job name')
    parser.add_argument('--data_dir',
            help='dataset location in directory in `job_dir`/sequences')
    args, unknown = parser.parse_known_args()
    args = args.__dict__

    print "Starting with parameters:"
    print args

    t = Trainer(**args)
    t.train()
