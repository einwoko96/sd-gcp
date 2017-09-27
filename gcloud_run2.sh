#!/bin/bash

export JOB_NAME="lstm_train_$(date +%Y%m%d_%H%M%S)"
export BUCKET_NAME=lstm-training
export JOB_DIR=gs://${BUCKET_NAME}
export OUTPUT_PATH=gs://${BUCKET_NAME}/${JOB_NAME}
export REGION=us-east1

python trainer/train.py \
	--job_type cloud \
	--job_dir ${JOB_DIR} \
	--output_path ${OUTPUT_PATH} \
	--seq_length 40 \
	--batch_size 32
