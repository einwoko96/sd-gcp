#!/bin/bash

export JOB_NAME="kinetics_train_$(date +%Y%m%d_%H%M%S)"
DATA_DIR="kinetics-40"
SPLIT=0.80
SEED=137
SEQ_LENGTH=40

python separate_classes.py \
	--seed "${SEED}" \
	--split "${SPLIT}" \
	--data_dir "${DATA_DIR}" \
	--seq_length "${SEQ_LENGTH}"

python trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--data_dir "${DATA_DIR}" \
        --seq_length "${SEQ_LENGTH}" \
        --batch_size 128 \
        --model_structure "gru" \
        --recurrent_dropout 0.25 \
        --unit_forget_bias "False"
