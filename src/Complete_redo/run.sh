#!/bin/bash

# Use webcam
#python3 detect_cards.py 1216

# Use webcam (fast for setup)
#python3 detect_cards.py 320 http://192.168.31.97:8080/video

# Use IP camera
python3 detect_cards.py 1216 http://192.168.31.97:8080/video

# Use IP camera (fast for setup)
#python3 detect_cards.py 320 http://192.168.31.97:8080/video

