#!/bin/bash

apt-get update && apt-get install -y ffmpeg
pip install xlrd coloredlogs
python3 --version
python3 -u extract-data.py