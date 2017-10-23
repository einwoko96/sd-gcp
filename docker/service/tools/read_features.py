"""Simple script to verify pickled dataset"""

import cPickle as pickle
import pandas as pd
import sys

with open(sys.argv[1], "rb") as f:
    while True:
        try:
            pd.read_csv(f.load()[1])
            num_read += 1
        except EOFError:
            break

print "Read " + str(num_read) + " objects from " + sys.argv[1]
