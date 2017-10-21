#!/bin/bash

export JOB_NAME="lstm_train_$(date +%Y%m%d_%H%M%S)"

python2 trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--data_dir "ucf-10-final" \
        --split 0.66 \
        --seed 137 \
        --seq_length 10 \
        --batch_size 32 \
        --model_structure "gru" \
        --recurrent_dropout 0.0 \
        --unit_forget_bias "False"
