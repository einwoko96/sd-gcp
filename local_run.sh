#!/bin/bash

export JOB_NAME="lstm_train_$(date +%Y%m%d_%H%M%S)"

python2 trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--model_structure gru \
	--data_dir ucf-5-npy \
	--seq_length 5 \
	--batch_size 32 \
	--dropout 0.5 \
	--recurrent_dropout 0.0 \
	--unit_forget_bias False
