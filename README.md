# 62410 CDIO-Projekt F20 - Solitaire solver

![Image of solitaire_ascii](https://raw.githubusercontent.com/MaxTheScrub/CDIO_Project/master/src/Complete_redo/solitaire_ascii.png)


Group 7:                                    
Henrik Peter Warncke s184801                
Max Feng Chen Bjørnsen s184811              
Jeppe Møller Bak s164871                    
Adam Aron Edelsten s173057                 
Tobias Lauge Borgstrøm s184810              
Tobias Ladefoged Jensen s184815             
Markus Repnak Jacobsen s184808              
Ajs Ritsmer Stormholt s174517               

Naming convention: https://www.python.org/dev/peps/pep-0008/                       
Class names: PascalCase                         
Function names: snake_case                       
Variables: camelCase
Objects: camelCase                        
Constants: SCREAMING_SNAKE_CASE 

The finished code is in the **src/complete_redo** folder

To run the code, first install python 3, clone the repository, install the python requirements and download the weights file:
```bash
git clone https://github.com/MaxTheScrub/CDIO_Project.git
cd CDIO_Project/src/Complete_redo/
pip3 install -r requirements.txt
wget https://github.com/MaxTheScrub/CDIO_Project/releases/download/90000/yolocards_90000.weights
```

In order to run the code, modify the **run.sh** file according to your input source:
```bash
#!/bin/bash

# Use webcam
#python3 detect_cards.py 1216

# Use webcam (fast for setup)
#python3 detect_cards.py 320 http://192.168.31.97:8080/video

# Use IP camera
python3 detect_cards.py 1216 http://192.168.31.97:8080/video

# Use IP camera (fast for setup)
#python3 detect_cards.py 320 http://192.168.31.97:8080/video
```
Where the IP-address is a video source such as an IP-camera. We have used the following app: https://play.google.com/store/apps/details?id=com.pas.webcam&hl=da

Running the app on a local network will show the IP-address for the video-stream. This IP-address  needs to be put into the **run.sh** commands. Alternatively, a webcam can be used, as long as its resolution is 1080p since that is the resolution that our program is made to run at. If a higher or lower resolution is wanted, the constants: **RESOLUTION_X** and **RESOLUTION_Y** can be modified in **classes.py**, this has not been tested and is not guaranteed to work.

A game of solitaire is played by first running one of the "fast for setup" commands from **run.sh** and laying a game of solitaire properly in the given piles. When the game is ready to be played, simply modify **run.sh** again to run with one of the higher resolution commands.
```bash
bash run.sh
```
Simply follow the advice that is written on the screen and illustrated with the yellow highlighting. The terminal shows a text-based solitaire game based on what is detected on the screen and also shows errors in detection. A high performance processor is needed to run the game at a usable FPS. An AMD 3700X (8 core processor) runs the code at 0.6 FPS.

Video demonstration of running a complete game of solitaire (with a random deck):

[![](http://img.youtube.com/vi/_YRsYZZIzUQ/0.jpg)](http://www.youtube.com/watch?v=_YRsYZZIzUQ "Link to video")
