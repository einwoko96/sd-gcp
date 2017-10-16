def main():
    classes_to_download = [
    'clapping',
    'celebrating'
    ]
    clean_up(classes_to_download)
    
    
def clean_up(classes):
    import os
    import glob
    import re
    from tqdm import tqdm
    for class_ind, class_name in enumerate(tqdm(classes)):
        completed_files = 'ytdl' + os.sep + class_name + os.sep + '*.avi'
        for video_ind, video_filename in enumerate(glob.glob(completed_files)):
            fileroot = os.path.splitext(video_filename)[0]
            mp4file = fileroot + '.mp4'
            if os.path.exists(mp4file):
                os.remove(mp4file)
        source = 'ytdl' + os.sep + class_name
        if os.path.exists(source):
            dest = 'ytdl' + os.sep + re.sub(' ','',(re.sub('_',' ',class_name).title()))
            os.rename(source,dest)
    
if __name__ == "__main__":
    main()