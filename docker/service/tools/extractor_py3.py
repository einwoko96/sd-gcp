"""
Short script to download feature vector for a single AVI video file
Change VIDEO_PATH or pass command line argument
"""

import os
import re
import sys
import glob
import subprocess
import numpy as np
from extractor import Extractor

# need Extractor.py (five-video-classification-methods, tensorflow, keras, h5py)
# set video path and sequence length

SEQ_LENGTH = 40
# VIDEO_PATH = "/home/jovita/SeniorDesign2017/tools/train/Archery/archery-lPLLbPsMDU.avi"
# VIDEO_PATH = "gunalan.avi"
VIDEO_PATH_SAMPLE = "https://fpdl.vimeocdn.com/vimeo-prod-skyfire-std-us/01/792/3/78961286/203684545.mp4?token=1505994750-0x2b1d99a82b3fd9415f0e0e578d37cecfd8d5a5dd&download=1&filename=Sample+Videos+%2852%29+-+Copy.mp4.mp4"
FRAMES_PER_VIDEO = "5"
FRAME_RATE = "fps=1/1"          # frames per second(s)
START_TIME = "00:00:00"

def extracted(video):
    vid_frame = re.sub(r'\.\w{3}', '-0001.jpg', video)
    return bool(os.path.exists(vid_frame))


def get_frames(video):
    if not video:
        video = VIDEO_PATH
    if extracted(video):
        return
    if 'http' in video:
        current_dir = os.getcwd()
        frame_output_path = current_dir + '/samples-%04d.jpg'
    else:
        frame_output_path = re.sub(r'\.\w{3}', '-%04d.jpg', video)
        
    try:
        # "-ss", START_TIME, "-filter:v", FRAME_RATE,
        ret = subprocess.call(["ffmpeg", "-i", video, "-vframes", FRAMES_PER_VIDEO, frame_output_path])
    except Exception:
        pass


def extract_features(name):
    VIDEO_PATH = name + ".avi"
    Model = Extractor()
    current_dir = os.getcwd()
    print("Vid name: ", name)
    vid_name = VIDEO_PATH.split('/')
    vid_name= vid_name[len(vid_name) - 1]
    seq_path = re.sub(r'\.\w{3}', '-features.txt', VIDEO_PATH)

    if not os.path.isfile(seq_path):
        get_frames(VIDEO_PATH)
        vid_frame_fmt = re.sub(r'\.\w{3}', '*.jpg', VIDEO_PATH)
        frames = glob.glob(vid_frame_fmt)
        if len(frames) > SEQ_LENGTH:
            # downsample number of frames to SEQ_LENGTH
            skip = len(frames)
            new_frames = [frames[i] for i in range(0, len(frames), skip)]
        sequence = []
        for frame in frames:
            features = Model.extract(frame)
            sequence.append(features)

        np.savetxt(seq_path, sequence)
        print("Sequence file saved to %s" % seq_path)
    else:
        print("Feature vector text file already exists for %s" % VIDEO_PATH)
    return seq_path


if __name__ == '__main__':
    try:
        VIDEO_PATH = sys.argv[1]
    except IndexError:
        print("Using default VIDEO_PATH, no command line input")
    extract_features()

