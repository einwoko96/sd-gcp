"""Simple script to demonstrate pickling dataframe feature vectors"""

import pandas as pd
import numpy as np
import multiprocessing as mp
import glob, argparse, os
from tqdm import tqdm

def txt_to_pickle(items):
    global output_path, queue
    for item in items:
        v = pd.read_csv(item, sep=" ", header=None)
        out_name = os.path.join(output_path, item.split('.txt')[0] + '.pkl')
        f = open(out_name, 'wb')
        v.to_pickle(f, compression='gzip')
        queue.put_nowait(1)

p = argparse.ArgumentParser()
p.add_argument('--dir',
        help='path to sequences directory',
        required=True)

args = p.parse_args().__dict__
src_dir = args.pop('dir')

vector_list = glob.glob(os.path.join(src_dir, '*.txt'))
for _ in range(0, len(vector_list) % 4):
    vector_list.append(None)
split_list = np.reshape(np.array(vector_list), (4, len(vector_list)/4))
thread_inputs = np.ndarray.tolist(split_list)
thread_inputs[3] = filter(None, thread_inputs[3])

output_path = os.path.join(src_dir, 'output')
try:
    os.mkdir(output_path)
except OSError:
    pass

queue = mp.Queue()
for i in range(0,4):
    p = mp.Process(target=txt_to_pickle, args=(thread_inputs[i],))
    p.start()

prog = tqdm(total=len(vector_list))
while mp.active_children > 0:
    queue.get()
    prog.update(1)
