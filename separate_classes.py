import glob, re, os, argparse, random
import numpy as np
import cPickle as pickle
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--classes',
        required=True,
        help='csv listing of classes')
parser.add_argument('--seed',
        type=int,
        required=True,
        help='random seed with which to generate the split')
parser.add_argument('--split', type=float)
parser.add_argument('--data_dir')
parser.add_argument('--seq_length', type=int)
args, unknown = parser.parse_known_args()
args = args.__dict__

train_set = []
test_set = []

classes = open(args['classes']).read().strip('\r\n').lower().split(',')

vectors_by_class = [[] for i in range(len(classes))]
vector_glob = glob.glob(os.path.join(args['data_dir'], '*.npy'))
random.seed(args['seed'])
for item in tqdm(vector_glob):
    if np.load(item).shape != (args['seq_length'], 2048):
        continue
    item_name = os.path.basename(item)
    item_class = re.split("^(.*?)(_|[0-9])", item_name)[1]
    for label in classes:
        if label.lower() == item_class.lower():
            vectors_by_class[classes.index(label)].append(
                    item_name)

for sublist in vectors_by_class:
    sublist.sort()
    random.shuffle(sublist)
    index = int(args['split'] * len(sublist))
    train_set.extend(sublist[:index])
    test_set.extend(sublist[index:])

with open(os.path.basename(args['data_dir]') + '_train.pkl', 'wb') as f:
    pickle.dump(train_set, f)

with open(os.path.basename(args['data_dir']) + '_test.pkl', 'wb') as f:
    pickle.dump(test_set, f)
    #call(gsutil mv f gs://lstm-training
