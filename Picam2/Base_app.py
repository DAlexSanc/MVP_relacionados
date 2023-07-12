#!/usr/bin/python3

# This example is essentially the same as app_capture.py, however here
# we use the Qt signal/slot mechanism to get a callback (capture_done)
# when the capture, that is running asynchronously, is finished.

from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget)

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput, FileOutput
from picamera2.previews.qt import QGlPicamera2


picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (1920, 1080)}))

app = QApplication([])


def on_button_clicked():
    button.setEnabled(False)
    cfg = picam2.create_still_configuration(main={"size": (1920, 1080)})
    picam2.switch_mode_and_capture_file(cfg, "test.jpg", signal_function=qpicamera2.signal_done)


def capture_done(job):
    picam2.wait(job)
    button.setEnabled(True)


qpicamera2 = QGlPicamera2(picam2, width=1920, height=1080, keep_ar=False)
window = QWidget()
qpicamera2.done_signal.connect(capture_done)


layout_h = QHBoxLayout()
layout_v = QVBoxLayout()
layout_h.addWidget(qpicamera2, 100)
#layout_h.addLayout(layout_v, 20)
window.setWindowTitle("Qt Picamera2 App")
window.resize(1920, 1080)
window.setLayout(layout_h)
button = QPushButton("Click to capture JPEG", parent = window) ##Lo importante es el parent
button.clicked.connect(on_button_clicked) 
button.setFixedSize(100,40)   
button.setGeometry(12, 12, 10, 10) ##Los parametros importantes de donde se pone el boton son los primero dos (12, 12)  


picam2.start()
window.show()
app.exec()
