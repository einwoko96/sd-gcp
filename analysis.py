import numpy as np
import os
import glob
import re
import pandas as pd
import argparse
from keras.models import load_model
from tqdm import tqdm

#model_filename = '/home/dgj/sd-gcp/models/1506557978.57.hdf5'
#feature_dir = '/home/dgj/sd-gcp/sequences/ucf-40-final/hold'
#output_filename = '/home/dgj/Desktop/analysis.csv'

def analysis(model_filename, feature_dir, output_filename):
    feature_filenames = glob.glob(feature_dir + os.sep + '*.npy')
    basenames = [os.path.basename(f) for f in feature_filenames]
    file_classes = [re.search('[A-z]{1,}',s).group(0) for s in basenames]
    class_names = np.sort(np.unique(file_classes))
    
    sample = np.load(feature_filenames[0])
    size = np.shape(sample)
    del sample
    
    model = load_model(model_filename)
    
    col1 = ['']*len(feature_filenames)
    count = 0
    y = []
    for i_class_name, class_name in enumerate(tqdm(class_names)):
        files = glob.glob(feature_dir + os.sep + class_name + '*.npy')
        X = np.zeros([len(files), size[0], size[1]])    
        col1[count:count+len(files)] = np.repeat(class_name,len(files))
        for i_file, f in enumerate(files):
            feature = np.load(f)
    #        for some reason some of the feature vectors only had 30 frames!!!!
            if not np.shape(feature)[0] == size[0]:
                X[i_file,:,:] = np.zeros([size[0],size[1]])
            else:
                X[i_file,:,:] = feature 
        y.append(model.predict(X))
        count = count+len(files)
    y_list = y    
    y = np.vstack(y)
    df = pd.DataFrame(data=y,index=col1)
    df.to_csv(output_filename,header=class_names)
    return y_list, class_names

def read_predictions_csv(csvfile):
    df = pd.read_csv(csvfile,header=None)
    class_names = np.array(df.iloc[0,1:])
    true_classes = np.array(df.iloc[1:,0])
    predictions = np.array(df.iloc[1:,1:]).astype(float)
    del df
    y_list = [[]]*len(class_names)
    for i_class_name, class_name in enumerate(class_names):
        match = np.where(true_classes == class_names[i_class_name])[0]
        y_list[i_class_name] = predictions[match,:]
    return y_list, class_names
            
def topk_accuracy(y_list,k):
    
    topk_list = np.zeros([len(y_list)])
    
    for i_y, y in enumerate(y_list):
        predicted_classes = np.argsort(y,1)[:,-k:]
        n_correct = float(np.sum(predicted_classes == i_y))
        topk_list[i_y] = n_correct/float(len(y))
    
    n_samples = np.array([np.shape(y_list[i])[0] for i in range(len(y_list))])
    weight = n_samples/float(np.sum(n_samples))
    topk = np.dot(weight,topk_list)
    return topk, topk_list
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Generate inferences on the holdout' +
            'set and measure accuracy')
    parser.add_argument('--model',
            required=True,
            help='path to the hdf5 model to be tested')
    parser.add_argument('--holdout',
            required=True,
            help='path to data to run inferences on')
    args, unknown = parser.parse_known_args()
    args = args.__dict__

    p, c = analysis(args['model'], args['holdout'],
            os.path.join(os.path.dirname(args['model']), 'predictions.csv'))

    t1, l1 = topk_accuracy(p, 1)
    t5, l5 = topk_accuracy(p, 5)

    print ("Model: " + args['model'])
    print ("Top 1 accuracy: " + str(t1))
    print ("Top 5 accuracy: " + str(t5))

        


    
