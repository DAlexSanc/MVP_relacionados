from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QMainWindow, QFileDialog, )
from PyQt5.QtGui import QPixmap
import cv2 # OpenCV
import qimage2ndarray # for a memory leak,see gist
import sys # for exiting
from picamera2 import Picamera2

# Minimal implementation...



def displayFrame():
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = qimage2ndarray.array2qimage(frame)
    label.setPixmap(QPixmap.fromImage(image))

app = QApplication([])
window = QWidget()

# Picam2 
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()


# timer for getting frames

timer = QtCore.QTimer()
timer.timeout.connect(displayFrame)
timer.start(60)
label = QLabel('No Camera Feed')
button = QPushButton("Quiter")
button.clicked.connect(sys.exit) # quiter button 
layout = QVBoxLayout()
layout.addWidget(button)
layout.addWidget(label)
window.setLayout(layout)
window.show()
app.exec_()

# See also: https://gist.github.com/bsdnoobz/8464000
