#!/bin/bash

export JOB_NAME="lstm_train_$(date +%Y%m%d_%H%M%S)"
export BUCKET_NAME=lstm-training
export JOB_DIR=gs://${BUCKET_NAME}
export OUTPUT_PATH=gs://${BUCKET_NAME}/${JOB_NAME}
export REGION=us-east1

gcloud ml-engine jobs submit training ${JOB_NAME} \
	--job-dir gs://${BUCKET_NAME} \
	--runtime-version 1.0 \
	--module-name trainer.train \
	--package-path ./trainer \
	--region ${REGION} \
	--config=trainer/cloudml-gpu.yaml \
	-- \
	cloud