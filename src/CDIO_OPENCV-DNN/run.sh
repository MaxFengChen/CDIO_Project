#!/bin/bash
python detect_cards.py --config=yolocards_test.cfg --model=yolocards_28000.weights --classes=cards.names --width=1216 --height=1216 --scale=0.00392 --input=http://192.168.31.97:8080/video --rgb


