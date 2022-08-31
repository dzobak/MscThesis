#!/bin/bash
export FLASK_APP=./back.py
source $conda activate msc
flask run -h 0.0.0.0 -p 5002