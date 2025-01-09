#!/bin/bash

set -e
PWD=$(pwd)

# Download index file
if [ ! -f "$PWD/input/index_file.json" ]; then
  curl -X GET https://antm-pt-prod-dataz-nogbd-nophi-us-east1.s3.amazonaws.com/anthem/2025-01-01_anthem_index.json.gz -o $PWD/input/index_file.json.gz
  gzip -d $PWD/input/index_file.json.gz 
fi

# Setup python Virtual Env
if [ ! -d "$PWD/venv" ]; then
  python3 -m venv ./venv 
  pip install --upgrade pip 
  pip install -r requirements.txt 
  source ./venv/bin/activate
else
  source ./venv/bin/activate
fi
