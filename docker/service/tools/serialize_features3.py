"""Python 3 version of serialize_features.py"""
import pickle
import pandas as pd
import glob, os, argparse
from tqdm import tqdm
import csv

#p = argparse.ArgumentParser()
#
#p.add_argument('-d',
#        help='path to sequences directory',
#        required=True)
#
#args = p.parse_args()
#a = args.__dict__

src_dir = '/home/dev/five-video-classification-methods/data/sequences'

train_out = open('training.pickle', 'wb')
val_out = open('validation.pickle', 'wb')

num_test = 0
num_train = 0

videos = pd.read_csv('/home/dev/five-video-classification-methods/data/data_file.csv',names=['split','label','filename','n_frames'])

for ind, filename in enumerate(tqdm(videos['filename'])):
    try:
        if videos['split'][ind] == 'test':
            features = pd.read_csv(src_dir + os.sep + filename + "-5-features.txt", sep=" ", header=None)
            pickle.dump((filename, features), val_out, 1)
            num_test += 1
        elif videos['split'][ind]:
            features = pd.read_csv(src_dir + os.sep + filename + "-5-features.txt", sep=" ", header=None)
            pickle.dump((filename, features), train_out, 1)
            num_train += 1
    except FileNotFoundError:
        print('Could not find ' + src_dir + os.sep + filename + '-5-features.txt, skipping')
                

print ("Pickled " + str(num_train) + " training vectors.")
print ("Pickled " + str(num_test) + " testing vectors.")
