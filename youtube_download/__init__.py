from flask import Flask
from youtube_download.keys import secret_key 
import os

templates_dir = os.path.abspath('youtube_download/pages/')
app = Flask(__name__, template_folder=templates_dir)
app.config['SECRET_KEY'] = secret_key 

from youtube_download import routes
