import cv2
import time
from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)},lores={"format": 'YUV420', "size": (320, 240)}))
picam2.start()

while True:
    im = picam2.capture_array()
    
    cv2.imshow("Camera", im)

