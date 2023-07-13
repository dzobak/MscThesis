#!/bin/bash
export FLASK_APP=./back.py
# source $conda activate ocelapp
flask run -h 0.0.0.0 -p 5002