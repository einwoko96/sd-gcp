#!/usr/bin python
# -*- coding: utf-8 -*-

import re
import os
import glob
import subprocess
from datetime import datetime, timedelta
from string import capwords


FRAMES_PER_VIDEO = "40"         # set to download 40 frames for one video in each class
FRAMERATE_PROPERTY = "fps="          # frames per second(s)

#LogFile = open("dl_logging_%s.txt" % datetime.strftime(dt, "%m%d%y"), 'a')
#LogFile.write("START: %s\n" % datetime.strftime(dt, "%m%d%y-%H:%M:%S"))
def getLength(input_video):
    duration = subprocess.check_output(['ffprobe', '-i', input_video, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
    return duration

def get_nb_frames_for_video(video):
    vid_frame_fmt = re.sub(r'\.\w{3}', '*.jpg', video)
    generated_frames = glob.glob(vid_frame_fmt)
    return len(generated_frames)

def extract_frames():
    """
    SHOULD BE RUN FROM ONE LEVEL ABOVE '/train/<class_name>/<video_files> and /test/<class_name>/<video_files>'
    outputs to '/frames/train/<image files> and /frames/test/<image files>'
    extrames FRAMES_PER_VIDEO from each class video
    """
    # extract frames from training videos
    class_dirs = glob.glob('./train/*/')
    for class_dir in class_dirs:
        class_name = os.path.basename(os.path.normpath(class_dir))
        dest = './frames/train/' + class_name + '/'
        if not os.path.exists(dest):
            os.makedirs(dest)
        video_files = glob.glob(class_dir + '*.avi')
        for index, video_file in enumerate(video_files):
            duration = getLength(video_file)
            frame_dest_name = dest + 'video' + str(index) + 'frame' + '-%03d.jpg'
            try:
		# EXTRACTING FRAMES HERE
                ret = subprocess.call(["ffmpeg", "-i", video_file, "-filter:v", FRAMERATE_PROPERTY + str(float(FRAMES_PER_VIDEO)/float(duration)), "-vframes", FRAMES_PER_VIDEO, frame_dest_name])
                if ret != 0:
                    LogFile.write("Failed to extract frames from %s \n" % video_file)
            except Exception as e:
                LogFile.write("Failed to extract frames from %s: \n %s \n" % (video_file, e))
                print(e)
        
    #extract frames from testing videos
    class_dirs = glob.glob('./test/*/')
    for class_dir in class_dirs:
        class_name = os.path.basename(os.path.normpath(class_dir))
        dest = './frames/test/' + class_name + '/'
        if not os.path.exists(dest):
            os.makedirs(dest)
        video_files = glob.glob(class_dir + '*.avi')
        for index, video_file in enumerate(video_files):
            duration = getLength(video_file)
            frame_dest_name = dest + 'video' + str(index) + 'frame' + '-%03d.jpg'
            try:
		# EXTRACTING FRAMES HERE
                ret = subprocess.call(["ffmpeg", "-i", video_file, "-filter:v", FRAMERATE_PROPERTY + str(float(FRAMES_PER_VIDEO)/float(duration)), "-vframes", FRAMES_PER_VIDEO, frame_dest_name])
                if ret != 0:
                    LogFile.write("Failed to extract frames from %s \n" % video_file)
            except Exception as e:
                LogFile.write("Failed to extract frames from %s: \n %s \n" % (video_file, e))
                print(e)
    
    """
    vid_class = re.sub(r'\s+', '', capwords(vid_class))
    class_files = glob.glob('./ytdl/*/' + vid_class + '/' '*.avi')
    for video in class_files:
        x, data_folder, train_or_test, classname, filename = video.split('/')
        filename_no_ext = re.sub(r'\.\w{3}', '', filename)

        src = video
        dest_folder = re.split('\d{1,3}.avi', video)[0]
        dest = dest_folder + filename_no_ext + '-%03d.jpg'
        try:
		# EXTRACTING FRAMES HERE
            ret = subprocess.call(["ffmpeg", "-i", src, "-filter:v", FRAME_RATE, "-vframes", FRAMES_PER_VIDEO, dest])
            if ret == 0:
                nb_frames = get_nb_frames_for_video(video)
                DataFile.write("%s, %s, %s, %s \n" % (train_or_test, classname, filename_no_ext, nb_frames))
            else:
                LogFile.write("Failed to extract frames from %s \n" % video)
        except Exception as e:
            LogFile.write("Failed to extract frames from %s: \n %s \n" % (video, e))
            print(e)
    """			
def main():
    """
    run extract_frames to extract frames to /frames/train and /frames/test
    defaults: MAX_VIDEOS_PER_CLASS = 1200, FRAMES_PER_VIDEO = 40, FRAME_RATE = 4
    """
    extract_frames()

if __name__ == '__main__':
    main()
