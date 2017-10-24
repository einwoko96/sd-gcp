classes_to_download = [
    'clapping',
    'celebrating'
]

classes_to_download = [x.strip().replace(' ','_') for x in classes_to_download]

import pandas as pd
import numpy as np
import os
import youtube_dl
from tqdm import tqdm
import subprocess
kinetics = pd.read_csv('kinetics_val.csv')
kinetics['label'] = [ x.strip().replace(' ','_') for x in kinetics['label'] ]
labels = kinetics['label']

for class_ind, class_name in enumerate(classes_to_download):
    desired_videos_ind = np.where(labels == classes_to_download[class_ind])
    video_ids = kinetics.youtube_id.iloc[desired_videos_ind]
    for video_ind, video_id in enumerate(tqdm(video_ids)):
        url = 'http://www.youtube.com/watch?v=' + video_id
        output_filename = 'ytdl' + os.sep + 'validation' + os.sep + class_name + os.sep + str(video_ind) +'.%(ext)s'
        converted_file = 'ytdl' + os.sep + 'validation' + os.sep + class_name + os.sep + str(video_ind) + '.avi'
        if os.path.exists(converted_file):
            continue
        fmt = 'bestvideo[height<=480]'
        params = {'outtmpl': output_filename, 'format':fmt}
        ydl = youtube_dl.YoutubeDL(params)
        try:
            info = ydl.extract_info(url)
        except Exception:
            print('Failed to download video, skipping')
            continue
        source = 'ytdl' + os.sep + 'validation' + os.sep + class_name + os.sep + str(video_ind) + '.' + info['ext']
        dest = 'ytdl' + os.sep + 'validation' + os.sep  + class_name + os.sep + str(video_ind) + '.avi'
        time_start = str(kinetics['time_start'].iloc[desired_videos_ind[0][video_ind]]);
        cmd_str = 'ffmpeg -y -ss ' + time_start +' -i ' + source + ' -t 10 -vcodec copy ' + dest
        subprocess.check_output(cmd_str, shell=True)
        os.remove(source)
        
