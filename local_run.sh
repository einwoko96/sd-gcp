#!/bin/bash

export JOB_NAME="train_$(date +%Y%m%d_%H%M%S)"
export DATA_DIR="ucf-10-final"
export SEQ_LENGTH=10

python2 trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--data_dir "${DATA_DIR}" \
        --split 0.66 \
        --seed 137 \
        --seq_length ${SEQ_LENGTH} \
        --batch_size 32 \
        --model_structure "gru" \
        --recurrent_dropout 0.0 \
        --unit_forget_bias "False"
