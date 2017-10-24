#!/bin/bash

export JOB_NAME="ts3_025_$(date +%Y%m%d_%H%M%S)"
export BUCKET_NAME=lstm-training
export JOB_DIR=gs://${BUCKET_NAME}
export OUTPUT_PATH=gs://${BUCKET_NAME}/${JOB_NAME}
export REGION=us-east1

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
	--data_dir "kinetics-40" \
	--split 0.80 \
	--seed 137 \
	--seq_length 40 \
	--batch_size 128 \
	--model_structure "gru" \
	--recurrent_dropout 0.25 \
	--unit_forget_bias "False"
