#!/bin/bash
export FLASK_APP=./backend/back.py
source $conda activate ocelapp
flask run -h 0.0.0.0 -p 5002