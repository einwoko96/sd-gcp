#!/bin/bash

export JOB_NAME="kinetics_train_$(date +%Y%m%d_%H%M%S)"
export DATA_DIR="kinetics-40"
export SEQ_LENGTH=40

python2 trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--data_dir "${DATA_DIR}" \
        --split 0.80 \
        --seed 137 \
        --seq_length ${SEQ_LENGTH} \
        --batch_size 128 \
        --model_structure "gru" \
        --recurrent_dropout 0.25 \
        --unit_forget_bias "False"
