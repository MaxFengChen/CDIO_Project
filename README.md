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
Where the IP-address is a video source such as an IP-camera.

A game of solitaire is played by first running one of the "fast for setup" commands from **run.sh** and laying a game of solitaire properly in the given piles. When the game is ready to be played, simply modify **run.sh** again to run with one of the higher resolution commands.
```bash
bash run.sh
```
Simply follow the advice that is written on the screen and illustrated with the yellow highlighting.

![Image of solitaire game](https://raw.githubusercontent.com/MaxTheScrub/CDIO_Project/master/src/Complete_redo/CV%20Solitaire%20solver%20-%20Gruppe%207_screenshot_24.06.2020.png)
