#!/bin/bash

export JOB_NAME="train_$(date +%Y%m%d_%H%M%S)"
export DATA_DIR="ucf-40-final"
export SEQ_LENGTH=40

python2 trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--data_dir "${DATA_DIR}" \
        --split 0.80 \
        --seed 137 \
        --seq_length ${SEQ_LENGTH} \
        --batch_size 32 \
        --model_structure "gru" \
        --recurrent_dropout 0.25 \
        --unit_forget_bias "False"
