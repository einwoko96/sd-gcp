"""Simple script to verify pickled dataset"""
import pickle

def read_features(filename):
    num_read = 0
    all_content = [];
    with open(filename, "rb") as f:
        while True:
            try:
                content = pickle.load(f)
#                print(content[0])
                num_read += 1
                all_content.append(content)
            except EOFError:
                break
    
    print ("Read " + str(num_read) + " objects")
    b, c = [e[0] for e in all_content], [e[1] for e in all_content]
    return b,c

def read_features_easy(filename):
    import numpy as np
    filenames, features = read_features(filename)
    ind = np.argsort(filenames)
    filenames = [filenames[i] for i in ind]
    features = [features[i] for i in ind]
    names = []
    data_ind = []
    num_frames = np.shape(features[0])[0]

    for file_ind, filename in enumerate(filenames):
        name = filename[2:(len(filename)-8)]
        if len(np.where(np.array(names) == name)[0]):
            data_ind[-1].append(file_ind)
        else:
            names.append(name)
            data_ind.append([])
    data = []
    for name_ind, name in enumerate(names):
        class_features = [features[i] for i in data_ind[name_ind]]
        X = np.zeros([len(class_features),num_frames,2048])
        for ind, val in enumerate(class_features):
            X[ind] = val
        data.append(X)
    out = {'data':data, 'names':names, 'num_frames':num_frames}
    return(out) 