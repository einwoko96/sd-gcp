#!/bin/bash

export JOB_NAME="lstm_train_$(date +%Y%m%d_%H%M%S)"

python2 trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--data_dir ucf-5-npy \
	--seq_length 5 \
	--seed 137 \
	--split 0.66 \
	--model_structure gru \
	--batch_size 32 \
	--dropout 0.5 \
	--recurrent_dropout 0.0 \
	--unit_forget_bias False
