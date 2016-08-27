import os
import sys

basedir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, basedir + '/../')

from flaskr import flaskr
from utils import logging
