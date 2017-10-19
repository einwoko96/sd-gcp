import numpy as np
import os
import glob
import re
import pandas as pd
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
        
    y = np.vstack(y)
    df = pd.DataFrame(data=y,index=col1)
    df.to_csv(output_filename,header=class_names)
    return y



    