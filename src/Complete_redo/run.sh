#!/bin/bash

# Use webcam
#python detect_cards.py --config=yolocards_test.cfg --model=yolocards_28000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --rgb

# Use ip camera
python3 detect_cards.py --config=yolocards_test.cfg --model=/home/stormholt/Desktop/yolocards_90000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --input=http://192.168.0.10:8080/video --rgb

