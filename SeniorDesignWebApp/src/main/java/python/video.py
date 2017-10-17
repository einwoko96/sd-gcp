# -*- coding: utf-8 -*-
import os
import sys
tastemaker = os.path.dirname(os.getcwd())
sys.path.append(tastemaker)
# from predict import main

from flask import Flask, render_template, send_file, request, abort, redirect
app = Flask(__name__, template_folder='.')

print("Howdy")
