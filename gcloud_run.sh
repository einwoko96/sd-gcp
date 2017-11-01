#!/bin/bash

set -e

# These values should remain the same
export BUCKET_NAME=lstm-training
export JOB_DIR=gs://${BUCKET_NAME}
export OUTPUT_PATH=gs://${BUCKET_NAME}/${JOB_NAME}
export REGION=us-east1
export JOB_NAME="ts4_fold4"
#$(date +%Y%m%d_%H%M%S)"
DATA_DIR="kinetics-40"
CLASS_LIST="class_list_${DATA_DIR}.csv"
SPLIT=0.80
SEED=137
SEQ_LENGTH=40
BATCH_SIZE=128
REC_DROPOUT='0.00'

#python separate_classes.py \
#	--seed 137 \
#	--split "${SPLIT}" \
#	--data_dir "${DATA_DIR}" \
#	--seq_length "${SEQ_LENGTH}" \
#	--classes "${CLASS_LIST}" \
#	--job_name "${JOB_NAME}" \
#	--export

gcloud ml-engine jobs submit training "${JOB_NAME}" \
	--job-dir "gs://${BUCKET_NAME}" \
	--runtime-version 1.2 \
	--module-name trainer.train \
	--package-path ./trainer \
	--region "${REGION}" \
	--config=trainer/cloudml-gpu.yaml \
	-- \
	--job_type "cloud" \
	--job_dir "${JOB_DIR}" \
	--job_name "${JOB_NAME}" \
	--data_dir "${DATA_DIR}" \
	--seq_length "${SEQ_LENGTH}" \
	--batch_size "${BATCH_SIZE}" \
	--model_structure "gru" \
	--recurrent_dropout "${REC_DROPOUT}" \
	--unit_forget_bias "False"
