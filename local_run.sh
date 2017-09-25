#!/bin/bash

python trainer/train.py \
	--job_type local \
	--job_dir $(pwd) \
	--seq_length 40
