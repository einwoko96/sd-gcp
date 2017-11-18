import io
import os
import sys
import json
import logging
import matplotlib
import subprocess
import numpy as np
matplotlib.use('Agg')
from wordcloud import WordCloud
from multiprocessing import Pool
from werkzeug.datastructures import MultiDict

def pred():
    print("Starting")
    wordcloud = WordCloud(width = 1000, height = 500, min_font_size=None, 
                relative_scaling=0.65, background_color='white')
    classes = ["Apply Eye Makeup","Apply Lipstick","Archery","Baby Crawling","Balance Beam","Band Marching","Baseball Pitch","Basketball Shooting","Basketball Dunk","Bench Press","Biking","Billiards Shot","Blow Dry Hair","Blowing Candles","Body Weight Squats","Bowling","Boxing Punching Bag","Boxing Speed Bag","Breaststroke","Brushing Teeth","Clean and Jerk","Cliff Diving","Cricket Bowling","Cricket Shot","Cutting In Kitchen","Diving","Drumming","Fencing","Field Hockey Penalty","Floor Gymnastics","Frisbee Catch","Front Crawl","Golf Swing","Haircut","Hammer Throw","Hammering","Handstand Pushups","Handstand Walking","Head Massage","High Jump","Horse Race","Horse Riding","Hula Hoop","Ice Dancing","Javelin Throw","Juggling Balls","Jump Rope","Jumping Jack","Kayaking","Knitting","Long Jump","Lunges","Military Parade","Mixing Batter","Mopping Floor","Nun chucks","Parallel Bars","Pizza Tossing","Playing Guitar","Playing Piano","Playing Tabla","Playing Violin","Playing Cello","Playing Daf","Playing Dhol","Playing Flute","Playing Sitar","Pole Vault","Pommel Horse","Pull Ups","Punch","Push Ups","Rafting","Rock Climbing Indoor","Rope Climbing","Rowing","Salsa Spins","Shaving Beard","Shotput","Skate Boarding","Skiing","Skijet","Sky Diving","Soccer Juggling","Soccer Penalty","Still Rings","Sumo Wrestling","Surfing","Swing","Table Tennis Shot","Tai Chi","Tennis Swing","Throw Discus","Trampoline Jumping","Typing","Uneven Bars","Volleyball Spiking","Walking with a dog","Wall Pushups","Writing On Board","Yo Yo"]
    frequencies = dict()
    count = 0
    for c in classes:
        if (len(c) % 2 == 0) and count < 5:
            frequencies[c] = int(len(c) * (10**(count+11)))
            count += 1
        # else:
        #     frequencies[c] = int(len(c))
        # print(frequencies[c])
    wordcloud.generate_from_frequencies(frequencies)
    wordcloud.to_file('wordcloud.png')
    print("Saving")
    
pred()
