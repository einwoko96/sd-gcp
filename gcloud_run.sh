#!/bin/bash

export JOB_NAME="lstm-train-$(date +%Y%m%d_%H%M%S)"
export BUCKET_NAME=lstm-training
export JOB_DIR=gs://${BUCKET_NAME}
export REGION=us-east1-c

gcloud ml-engine jobs submit training ${JOB_NAME} \
	--job-dir gs://${BUCKET_NAME} \
	--runtime-version 1.0 \
	--package-path ./trainer \
	--region ${REGION} \
	--config=trainer/cloudml-gpu.yaml \
	-- \
	cloud
