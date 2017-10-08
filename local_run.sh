#!/bin/bash

export JOB_NAME="lstm_train_$(date +%Y%m%d_%H%M%S)"

python2 trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--seq_length 40 \
	--batch_size 32 \
