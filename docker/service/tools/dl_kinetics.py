#!/usr/bin python
# -*- coding: utf-8 -*-

import re
import os
import glob
import numpy as np
import pandas as pd
import youtube_dl
import subprocess
from datetime import datetime, timedelta
from string import capwords

full_class_list = ['abseiling', 'air drumming', 'answering questions', 'applauding', 'applying cream', 'archery',
                   'arm wrestling', 'arranging flowers', 'assembling computer', 'auctioning', 'baby waking up',
                   'baking cookies', 'balloon blowing', 'bandaging', 'barbequing', 'bartending', 'beatboxing',
                   'bee keeping', 'belly dancing', 'bench pressing', 'bending back', 'bending metal',
                   'biking through snow', 'blasting sand', 'blowing glass', 'blowing leaves', 'blowing nose',
                   'blowing out candles', 'bobsledding', 'bookbinding', 'bouncing on trampoline', 'bowling',
                   'braiding hair', 'breading or breadcrumbing', 'breakdancing', 'brush painting', 'brushing hair',
                   'brushing teeth', 'building cabinet', 'building shed', 'bungee jumping', 'busking',
                   'canoeing or kayaking', 'capoeira', 'carrying baby', 'cartwheeling', 'carving pumpkin',
                   'catching fish', 'catching or throwing baseball', 'catching or throwing frisbee',
                   'catching or throwing softball', 'celebrating', 'changing oil', 'changing wheel', 'checking tires',
                   'cheerleading', 'chopping wood', 'clapping', 'clay pottery making', 'clean and jerk',
                   'cleaning floor', 'cleaning gutters', 'cleaning pool', 'cleaning shoes', 'cleaning toilet',
                   'cleaning windows', 'climbing a rope', 'climbing ladder', 'climbing tree', 'contact juggling',
                   'cooking chicken', 'cooking egg', 'cooking on campfire', 'cooking sausages', 'counting money',
                   'country line dancing', 'cracking neck', 'crawling baby', 'crossing river', 'crying', 'curling hair',
                   'cutting nails', 'cutting pineapple', 'cutting watermelon', 'dancing ballet', 'dancing charleston',
                   'dancing gangnam style', 'dancing macarena', 'deadlifting', 'decorating the christmas tree',
                   'digging', 'dining', 'disc golfing', 'diving cliff', 'dodgeball', 'doing aerobics', 'doing laundry',
                   'doing nails', 'drawing', 'dribbling basketball', 'drinking', 'drinking beer', 'drinking shots',
                   'driving car', 'driving tractor', 'drop kicking', 'drumming fingers', 'dunking basketball',
                   'dying hair', 'eating burger', 'eating cake', 'eating carrots', 'eating chips', 'eating doughnuts',
                   'eating hotdog', 'eating ice cream', 'eating spaghetti', 'eating watermelon', 'egg hunting',
                   'exercising arm', 'exercising with an exercise ball', 'extinguishing fire', 'faceplanting',
                   'feeding birds', 'feeding fish', 'feeding goats', 'filling eyebrows', 'finger snapping',
                   'fixing hair', 'flipping pancake', 'flying kite', 'folding clothes', 'folding napkins',
                   'folding paper', 'front raises', 'frying vegetables', 'garbage collecting', 'gargling',
                   'getting a haircut', 'getting a tattoo', 'giving or receiving award', 'golf chipping',
                   'golf driving', 'golf putting', 'grinding meat', 'grooming dog', 'grooming horse',
                   'gymnastics tumbling', 'hammer throw', 'headbanging', 'headbutting', 'high jump', 'high kick',
                   'hitting baseball', 'hockey stop', 'holding snake', 'hopscotch', 'hoverboarding', 'hugging',
                   'hula hooping', 'hurdling', 'hurling', 'ice climbing', 'ice fishing', 'ice skating', 'ironing',
                   'javelin throw', 'jetskiing', 'jogging', 'juggling balls', 'juggling fire', 'juggling soccer ball',
                   'jumping into pool', 'jumpstyle dancing', 'kicking field goal', 'kicking soccer ball', 'kissing',
                   'kitesurfing', 'knitting', 'krumping', 'laughing', 'laying bricks', 'long jump', 'lunge',
                   'making a cake', 'making a sandwich', 'making bed', 'making jewelry', 'making pizza',
                   'making snowman', 'making sushi', 'making tea', 'marching', 'massaging back', 'massaging feet',
                   'massaging legs', 'massaging person', 'milking cow', 'mopping floor', 'motorcycling',
                   'moving furniture', 'mowing lawn', 'news anchoring', 'opening bottle', 'opening present',
                   'paragliding', 'parasailing', 'parkour', 'passing American football', 'passing American football',
                   'peeling apples', 'peeling potatoes', 'petting animal', 'petting cat', 'picking fruit',
                   'planting trees', 'plastering', 'playing accordion', 'playing badminton', 'playing bagpipes',
                   'playing basketball', 'playing bass guitar', 'playing cards', 'playing cello', 'playing chess',
                   'playing clarinet', 'playing controller', 'playing cricket', 'playing cymbals', 'playing didgeridoo',
                   'playing drums', 'playing flute', 'playing guitar', 'playing harmonica', 'playing harp',
                   'playing ice hockey', 'playing keyboard', 'playing kickball', 'playing monopoly', 'playing organ',
                   'playing paintball', 'playing piano', 'playing poker', 'playing recorder', 'playing saxophone',
                   'playing squash or racquetball', 'playing tennis', 'playing trombone', 'playing trumpet',
                   'playing ukulele', 'playing violin', 'playing volleyball', 'playing xylophone', 'pole vault',
                   'presenting weather forecast', 'pull ups', 'pumping fist', 'pumping gas', 'punching bag',
                   'punching person', 'push up', 'pushing car', 'pushing cart', 'pushing wheelchair', 'reading book',
                   'reading newspaper', 'recording music', 'riding a bike', 'riding camel', 'riding elephant',
                   'riding mechanical bull', 'riding mountain bike', 'riding mule', 'riding or walking with horse',
                   'riding scooter', 'riding unicycle', 'ripping paper', 'robot dancing', 'rock climbing',
                   'rock scissors paper', 'roller skating', 'running on treadmill', 'sailing', 'salsa dancing',
                   'sanding floor', 'scrambling eggs', 'scuba diving', 'setting table', 'shaking hands', 'shaking head',
                   'sharpening knives', 'sharpening pencil', 'shaving head', 'shaving legs', 'shearing sheep',
                   'shining shoes', 'shooting basketball', 'shooting goal', 'shot put', 'shoveling snow',
                   'shredding paper', 'shuffling cards', 'side kick', 'sign language interpreting', 'singing', 'situp',
                   'skateboarding', 'ski jumping', 'skiing', 'skiing crosscountry', 'skiing slalom', 'skipping rope',
                   'skydiving', 'slacklining', 'slapping', 'sled dog racing', 'smoking', 'smoking hookah',
                   'snatch weight lifting', 'sneezing', 'sniffing', 'snorkeling', 'snowboarding', 'snowkiting',
                   'snowmobiling', 'somersaulting', 'spinning poi', 'spray painting', 'spraying', 'springboard diving',
                   'squat', 'sticking tongue out', 'stomping grapes', 'stretching arm', 'stretching leg',
                   'strumming guitar', 'surfing crowd', 'surfing water', 'sweeping floor', 'swimming backstroke',
                   'swimming breast stroke', 'swimming butterfly stroke', 'swing dancing', 'swinging legs',
                   'swinging on something', 'sword fighting', 'tai chi', 'taking a shower', 'tango dancing',
                   'tap dancing', 'tapping guitar', 'tapping pen', 'tasting beer', 'tasting food', 'testifying',
                   'texting', 'throwing axe', 'throwing ball', 'throwing discus', 'tickling', 'tobogganing',
                   'tossing coin', 'tossing salad', 'training dog', 'trapezing', 'trimming or shaving beard',
                   'trimming trees', 'triple jump', 'tying bow tie', 'tying knot', 'tying tie', 'unboxing',
                   'unloading truck', 'using computer', 'using remote controller', 'using segway', 'vault',
                   'waiting in line', 'walking the dog', 'washing dishes', 'washing feet', 'washing hair',
                   'washing hands', 'water skiing', 'water sliding', 'watering plants', 'waxing back', 'waxing chest',
                   'waxing eyebrows', 'waxing legs', 'weaving basket', 'welding', 'whistling', 'windsurfing',
                   'wrapping present', 'wrestling', 'writing', 'yawning', 'yoga', 'zumba']
ucf_class_list = ["ApplyEyeMakeup", "ApplyLipstick", "Archery", "BabyCrawling", "BalanceBeam", "BandMarching",
                  "BaseballPitch", "Basketball", "BasketballDunk", "BenchPress", "Biking", "Billiards", "BlowDryHair",
                  "BlowingCandles", "BodyWeightSquats", "Bowling", "BoxingPunchingBag", "BoxingSpeedBag",
                  "BreastStroke", "BrushingTeeth", "CleanAndJerk", "CliffDiving", "CricketBowling", "CricketShot",
                  "CuttingInKitchen", "Diving", "Drumming", "Fencing", "FieldHockeyPenalty", "FloorGymnastics",
                  "FrisbeeCatch", "FrontCrawl", "GolfSwing", "Haircut", "Hammering", "HammerThrow", "HandstandPushups",
                  "HandstandWalking", "HeadMassage", "HighJump", "HorseRace", "HorseRiding", "HulaHoop", "IceDancing",
                  "JavelinThrow", "JugglingBalls", "JumpingJack", "JumpRope", "Kayaking", "Knitting", "LongJump",
                  "Lunges", "MilitaryParade", "Mixing", "MoppingFloor", "Nunchucks", "ParallelBars", "PizzaTossing",
                  "PlayingCello", "PlayingDaf", "PlayingDhol", "PlayingFlute", "PlayingGuitar", "PlayingPiano",
                  "PlayingSitar", "PlayingTabla", "PlayingViolin", "PoleVault", "PommelHorse", "PullUps", "Punch",
                  "PushUps", "Rafting", "RockClimbingIndoor", "RopeClimbing", "Rowing", "SalsaSpin", "ShavingBeard",
                  "Shotput", "SkateBoarding", "Skiing", "Skijet", "SkyDiving", "SoccerJuggling", "SoccerPenalty",
                  "StillRings", "SumoWrestling", "Surfing", "Swing", "TableTennisShot", "TaiChi", "TennisSwing",
                  "ThrowDiscus", "TrampolineJumping", "Typing", "UnevenBars", "VolleyballSpiking", "WalkingWithDog",
                  "WallPushups", "WritingOnBoard", "YoYo"]

CLASSES_TO_DOWNLOAD = [
   #  'filling eyebrows',
   #  'finger snapping',
   #  'folding clothes',
   #  'folding napkins',
   #  'folding paper',
   #  'frying vegetables',
   #  'laughing',
   # 'lunge',
    'making a cake',
    'making a sandwich',
    'making bed',
    'moving furniture',
    'opening bottle',
    'opening present',
    'petting cat',
    'playing cards',
]

MAX_VIDEOS_PER_CLASS = 1200       # limits number of videos to download per class
VIDEO_DURATION = "00:00:10"     # length (seconds) of video downloaded
FRAMES_PER_VIDEO = "40"          # set to download 40 frames for one video in each class
FRAME_RATE = "fps=4/1"          # frames per second(s)

params = {
    'format': 'bestvideo[height<=480]',
    'verbose': 'false'}
ydl = youtube_dl.YoutubeDL(params)  # single instance of ydl class
dt = datetime.now()
Kinetics = pd.read_csv('kinetics_val.csv', nrows=None)

DataFile = open("data_file_%s.csv" % datetime.strftime(dt, "%m%d%y"), 'a')
LogFile = open("dl_logging_%s.txt" % datetime.strftime(dt, "%m%d%y"), 'a')
DataFile.write("START: %s\n" % datetime.strftime(dt, "%m%d%y-%H:%M:%S"))
LogFile.write("START: %s\n" % datetime.strftime(dt, "%m%d%y-%H:%M:%S"))


def get_full_class_list():
    """
    don't run, all classes in full_class_list[] at top of file
    """
    class_list = []
    class_file = open('dl_classInd.txt')
    try:
        class_list = [re.split('\d+\W+((\w*\s+)*)\W+', entry)[1] for entry in class_file]
    except Exception as e:
        LogFile.write("Error getting full_class_list: %s\n" % e)
    class_file.close()
    return class_list


def get_vid_class_info(vid_class):
    """
    :param vid_class: activity class as string
    :return: list of tuples [(vid_id, vidStart)]
    """
    vid_class_info = []
    try:
        vid_id_list = Kinetics.youtube_id.iloc[np.where(Kinetics['label'] == vid_class)].values.tolist()
        vid_start_list = Kinetics.time_start.iloc[np.where(Kinetics['label'] == vid_class)].values.tolist()
        vid_start_list = [str(timedelta(seconds=t)) for t in vid_start_list]
        vid_class_info = list(zip(vid_id_list, vid_start_list))
    except Exception as e:
        LogFile.write("%s\n" % e)
    return vid_class_info


def download_class_frames(vid_class, vid_class_info):
    """
    downloads video frames from specified class
    :param vid_class: activity class as string
    :param vid_class_info: list of tuples [(vid_id, vidStart)] --> get_vid_class_info
    """
    vid_frame_list = []
    for id, start in vid_class_info:
        vid_name = "%s_%s.avi" % (re.sub(r'\s+', '_', vid_class), id)
        if id == '#NAME?':
            continue
        if is_extracted(vid_name):
            LogFile.write("Frames already extracted for %s_%s\n" % (vid_class, id))
            continue
        vid_url = 'http://youtube.com/watch?v=' + id
        try:
            vid_info = ydl.extract_info(vid_url, download=False)  # GET FULL PATH TO YOUTUBE VIDEO
            url = vid_info['url']
            vid_frame_name = "%s_%s-%%04d.jpg" % (re.sub(r'\s+', '_', vid_class), id)
            ret = subprocess.call(["ffmpeg", "-ss", start, "-i", url, "-t", VIDEO_DURATION, "-filter:v", FRAME_RATE, "-vframes", FRAMES_PER_VIDEO, vid_frame_name])  # DOWNLOAD FRAMES
            if ret == 0:
                DataFile.write("train, %s, %s, %s\n" % (vid_class, id, get_nb_frames_for_video(vid_name)))
                LogFile.write("pass, %s, %s\n" % (vid_class, id))
            else:
                LogFile.write("fail, %s, %s\n" % (vid_class, id))
        except Exception as e:
            LogFile.write("fail, %s, %s\n" % (vid_class, id))
    return vid_frame_list


def move_class_frames(vid_class, vid_frame_list):
    vid_frame_files = glob.glob("%s*.jpg" % re.sub(r'\s+', '_', vid_class))
    vid_class = re.sub(r'\s+', '', capwords(vid_class))
    data_dir = os.getcwd()
    vid_dest = "%s/train/%s" % (data_dir, vid_class)
    vid_frame_files_dest = [("%s/%s" % (vid_dest, re.sub(r'\s+', '', vid))) for vid in vid_frame_files]

    if vid_frame_list:
        vid_frame_list_dest = [("%s/%s" % (vid_dest, re.sub(r'\s+', '', vid))) for vid in vid_frame_list]
    if not os.path.exists(vid_dest):
        try:
            os.makedirs(vid_dest)
            LogFile.write("Created folder for %s\n" % vid_dest)
        except Exception as e:
            LogFile.write("Error creating %s: %s\n" % (vid_dest, e))
    [os.rename(v_frame, v_frame_dest) for v_frame, v_frame_dest in list(zip(vid_frame_files, vid_frame_files_dest))]
    if vid_frame_list:
        [os.rename(v_frame, v_frame_dest) for v_frame, v_frame_dest in list(zip(vid_frame_list, vid_frame_list_dest))]


def get_nb_frames_for_video(video):
    vid_frame_fmt = re.sub(r'\.\w{3}', '*.jpg', video)
    generated_frames = glob.glob(vid_frame_fmt)
    return len(generated_frames)


def is_extracted(video):
    vid_frame = re.sub(r'\.\w{3}', '-\d{3}.jpg', video)
    return bool(os.path.exists(vid_frame))


def download_class_videos(vid_class, vid_class_info):
    """
    download MAX_VIDEOS_PER_CLASS videos for specified class
    :param vid_class: activity class as string
    :param vid_class_info: list of tuples [(vid_id, vidStart)] --> get_vid_class_info
    """
    vid_list = []
    index = 0
    for id, start in vid_class_info:
        if id == '#NAME?':
            continue  # SKIP if no valid youtube_id
        vid_url = 'http://youtube.com/watch?v=' + id
        try:
            vid_info = ydl.extract_info(vid_url, download=False)
            url = vid_info['url']
            # vid_name = re.sub(r'\s+', '_', vid_class) + id + ".avi"
            vid_name = re.sub(r'\s+', '_', vid_class) + "_" + index + ".avi"
            ret = subprocess.call(["ffmpeg", "-i",  url, "-ss", start, "-t", VIDEO_DURATION, "-c:v", "libx264",  vid_name])  # DOWNLOAD VIDEOS
            if ret == 0:
                LogFile.write("pass, %s, %s\n" % (vid_class, id))
                vid_list.append(vid_name)
            else:
                LogFile.write("fail, %s, %s\n" % (vid_class, id))
        except Exception as e:
            LogFile.write("fail, %s, %s\n" % (vid_class, id))
        index = index + 1
    return vid_list


def download_class_videos_v2(class_name, vid_class_info):
    vid_list = []
    video_ind = 0
    for video_id, time_start in vid_class_info:
        url = 'http://www.youtube.com/watch?v=' + video_id
        output_filename = re.sub(r'\s+', '_', class_name) + '_' + str(video_ind) + '.%(ext)s'
        converted_file =  re.sub(r'\s+', '_', class_name) + '_' + str(video_ind) + '.avi'
        if os.path.exists(converted_file):
            video_ind = video_ind + 1
            continue
        fmt = 'bestvideo[height<=480]'
        params = {'outtmpl': output_filename, 'format': fmt}
        ydl = youtube_dl.YoutubeDL(params)
        try:
            info = ydl.extract_info(url)
            LogFile.write("pass, %s, %s\n" % (class_name, video_id))
        except Exception:
            print('Failed to download video, skipping')
            LogFile.write("fail, %s, %s\n" % (class_name, video_id))
            video_ind = video_ind + 1
            continue
        source = re.sub(r'\s+', '_', class_name) + '_' + str(video_ind) + '.' + info['ext']
        vid_list.append(source)
        dest =  re.sub(r'\s+', '_', class_name) + '_' + str(video_ind) + '.avi'
        cmd_str = 'ffmpeg -y -ss ' + time_start + ' -i ' + source + ' -t 10 -vcodec copy ' + dest
        subprocess.check_output(cmd_str, shell=True)
        video_ind = video_ind + 1
    # REMOVE
    mp4_files = glob.glob("%s*.mp4" % re.sub(r'\s+', '_', class_name))
    webm_files = glob.glob("%s*.webm" % re.sub(r'\s+', '_', class_name))
    [os.remove(vid) for vid in mp4_files]
    [os.remove(vid) for vid in webm_files]


def move_class_videos(vid_class):
    vid_files = glob.glob("%s*.avi" % re.sub(r'\s+', '_', vid_class))
    vid_class = re.sub(r'\s+', '', capwords(vid_class))
    data_dir = os.getcwd()
    vid_dest ="%s/ytdl/%s" % (data_dir, vid_class)
    vid_files_dest = [("%s/%s" % (vid_dest, re.sub(r'\s+', '', vid))) for vid in vid_files]

    if not os.path.exists(vid_dest):
        try:
            os.makedirs(vid_dest)
            LogFile.write("Created folder for %s\n" % vid_dest)
        except Exception as e:
            LogFile.write("Error creating %s: %s\n" % (vid_dest, e))
    [os.rename(vid_f, vid_f_dest) for vid_f, vid_f_dest in list(zip(vid_files, vid_files_dest))]


def extract_frames(vid_class):
    """
    SHOULD BE RUN FROM ONE LEVEL ABOVE 'ytdl/train/<class_name>/<video_file>'
    :param vid_class: video class as 'filling eyebrows' OR 'FillingEyebrows'
    extrames FRAMES_PER_VIDEO from each class video
    """
    vid_class = re.sub(r'\s+', '', capwords(vid_class))
    class_files = glob.glob('./ytdl/*/' + vid_class + '/' '*.avi')
    for video in class_files:
        if is_extracted(video):
            continue
        x, data_folder, train_or_test, classname, filename = video.split('/')
        filename_no_ext = re.sub(r'\.\w{3}', '', filename)

        src = video
        dest_folder = re.split('\d{1,3}.avi', video)[0]
        dest = dest_folder + filename_no_ext + '-%03d.jpg'
        try:
            ret = subprocess.call(["ffmpeg", "-i", src, "-filter:v", FRAME_RATE, "-vframes", FRAMES_PER_VIDEO, dest])
            if ret == 0:
                nb_frames = get_nb_frames_for_video(video)
                DataFile.write("%s, %s, %s, %s \n" % (train_or_test, classname, filename_no_ext, nb_frames))
            else:
                LogFile.write("Failed to extract frames from %s \n" % video)
        except Exception as e:
            LogFile.write("Failed to extract frames from %s: \n %s \n" % (video, e))
            print(e)


def main():
    """
    1. run get_vid_class_info() to return list of [(vid_id, vidStarttime)] for specified class
    2. run download_class_videos_v2() to download videos from specified kinetics video class to the /ytdl/ directory
    3. run extract_frames to extract frames to /<vid class>/
       defaults: MAX_VIDEOS_PER_CLASS = 1200, FRAMES_PER_VIDEO = 40, FRAME_RATE = 4
    4. see 'data.csv' for Data file to input when TRAINING
    5. check 'dl_logging_*.txt' in working directory to view pass/ fail video IDs
    """
    for vid_class in CLASSES_TO_DOWNLOAD:
        LogFile.write("Downloading class: %s\n" % vid_class)
        class_info = get_vid_class_info(vid_class)
        try:
            if MAX_VIDEOS_PER_CLASS < len(class_info):
                vid_index = list(np.random.choice(len(class_info), MAX_VIDEOS_PER_CLASS))
                class_info = [class_info[v] for v in vid_index]
            else:
                pass
            download_class_videos_v2(vid_class, class_info)
            move_class_videos(vid_class)
            # extract_frames(vid_class)
        except ValueError as v:
            LogFile.write("Error downloading %s class:\n%s\n" % (vid_class, v))
    LogFile.close()
    DataFile.close()


if __name__ == '__main__':
    main()
