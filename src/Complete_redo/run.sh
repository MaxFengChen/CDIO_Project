#!/bin/bash

# Use webcam
#python detect_cards.py --config=yolocards_test.cfg --model=yolocards_28000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --rgb

# Use ip camera (High res needed for accuracy)
# 1216
# This is the one that we use
python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=1216 --height=1216 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb


# 1600
#python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=1600 --height=1600 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb
# 2000
#python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=2048 --height=2048 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb
# 3200
#python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=3200 --height=3200 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb

# Low res for "high FPS" testing
# 800
#python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=800 --height=800 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb
# 320
#python3 detect_cards.py --config=yolocards_test.cfg --model=yolocards_90000.weights --classes=cards.names --width=320 --height=320 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb

