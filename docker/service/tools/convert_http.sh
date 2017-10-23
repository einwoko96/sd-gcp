#!/bin/bash
$(ffmpeg -i $1.mp4 -vcodec copy -acodec copy $2.avi)
