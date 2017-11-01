import glob, re, os, argparse, random
import numpy as np
import cPickle as pickle
from tqdm import tqdm
from subprocess import call

def rotate(l, x):
    return l[-x:] + l[:-x]

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
parser.add_argument('--export', action='store_true')
parser.add_argument('--job_name')
parser.add_argument('--cross', default=False, action='store_true')
args, unknown = parser.parse_known_args()
args = args.__dict__

classes = open(args['classes']).read().strip('\r\n').lower().split(',')
vectors_by_class = [[] for i in range(len(classes))]
vector_glob = glob.glob(os.path.join('sequences', args['data_dir'], '*.npy'))
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

if args['cross'] == False:
    train_set = []
    test_set = []
    for sublist in vectors_by_class:
        sublist.sort()
        random.shuffle(sublist)
        index = int(args['split'] * len(sublist))
        train_set.extend(sublist[:index])
        test_set.extend(sublist[index:])

    with open(args['job_name'] + '_train.pkl', 'wb') as f:
        pickle.dump(train_set, f)

    with open(args['job_name'] + '_test.pkl', 'wb') as f:
        pickle.dump(test_set, f)

    if args['export']:
        call(['gsutil', 'mv' , args['job_name'] + '_train.pkl',
            os.environ['JOB_DIR']])
        call(['gsutil', 'mv', args['job_name'] + '_test.pkl',
            os.environ['JOB_DIR']])

elif args['cross'] == True:
    num_fold = int(1/(1-args['split']))
    train_set = [[] for i in range(num_fold)]
    test_set = [[] for i  in range(num_fold)]
    for sublist in vectors_by_class:
        sublist.sort()
        random.shuffle(sublist)
        for i in range(num_fold):
            index = int(args['split'] * len(sublist))
            train_set[i].extend(sublist[:index])
            test_set[i].extend(sublist[index:])
            sublist = rotate(sublist, index)
    
    for i in range(num_fold):
        print str(len(train_set[i])) + ' ' + str(len(test_set[i]))
        print len([x for x in test_set[i] if x in test_set[(i + 1) % num_fold]])
        with open(args['job_name'] + str(i) + '_train.pkl', 'wb') as f:
            pickle.dump(train_set[i], f)

        with open(args['job_name'] + str(i) + '_test.pkl', 'wb') as f:
            pickle.dump(test_set[i], f)

        call(['gsutil', 'mv' , args['job_name'] + str(i) + '_train.pkl',
            os.environ['JOB_DIR']])
        call(['gsutil', 'mv', args['job_name'] + str(i) + '_test.pkl',
            os.environ['JOB_DIR']])
