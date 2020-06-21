#!/bin/bash

# Use webcam
#python detect_cards.py --config=yolocards_test.cfg --model=yolocards_28000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --rgb

# Use ip camera (High res needed for accuracy)
#python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=1216 --height=1216 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb
# Low res for "high FPS" testing
python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb

