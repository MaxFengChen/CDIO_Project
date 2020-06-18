#!/bin/bash

# Use webcam
#python detect_cards.py --config=yolocards_test.cfg --model=yolocards_28000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --rgb

# Use ip camera
python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --input=http://192.168.0.101:8080/video --rgb

# Use picture 
#python detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --input=/home/stormholt/Documents/CDIO/CDIO_Project/src/Complete/testpic1.jpg --rgb
