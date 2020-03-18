import requests     # pip3 install requests
import cv2 as cv    # pip3 install opencv-python 
import numpy as np

# Install this app on your Android phone: https://play.google.com/store/apps/details?id=com.pas.webcam&hl=en
# Change the url below to the IP adress shown in the app
url = "http://10.0.0.77:8080/shot.jpg"

while True:
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    img = cv.imdecode(img_arr, -1)

    cv.imshow("Yeet yeet beat my meat", img)

    if cv.waitKey(1) == 27:
        break