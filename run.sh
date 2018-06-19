#!/bin/bash
git pull
python3 replace-tags.py
python3 augment-tags.py
python3 update-maps.py
