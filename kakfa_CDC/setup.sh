#!/bin/bash

virtualenv -p /usr/bin/python venv
source venv/bin/activate
pip install -r requirements.txt
