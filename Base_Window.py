#!/usr/bin/python3

# This example is essentially the same as app_capture.py, however here
# we use the Qt signal/slot mechanism to get a callback (capture_done)
# when the capture, that is running asynchronously, is finished.

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
                             QVBoxLayout, QWidget, QMainWindow, QFileDialog, QShortcut)
from PyQt5.QtGui import QKeySequence

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput, FileOutput
from picamera2.previews.qt import QGlPicamera2
import libcamera
from skimage.metrics import structural_similarity
import numpy as np
from datetime import datetime
import cv2
import time
import sys
import SSIM2App
import atexit

#from Sett_Wind import Ui_Sett_Window
    
import os 
from configparser import ConfigParser
config = ConfigParser()


config.read("/media/diego/USB/PyQt_Apps/IRISConfig.ini")
config_data = config["DEFAULT"]



picam2 = Picamera2()
picam2_pConfig = picam2.create_preview_configuration(main={"format": 'XRGB8888',"size": (1920, 1080)})

picam2_pConfig["transform"] = libcamera.Transform(hflip=0, vflip=0)
picam2.configure(picam2_pConfig)
picam2.start()

H_toggle = False
V_toggle = False 
recording = False 
Iris_On = False 
Minsim = 00.00 
testing = 0 


class Main_Preview(): 
        def __init__(self):
                
                self.window = QWidget()
                self.layout_h = QHBoxLayout()
              
                self.layout_h.addWidget(qpicamera2, 10)
                self.window.setWindowTitle("Qt Picamera2 App")
                self.window.resize(1920, 1080)
                self.window.setLayout(self.layout_h)
                self.CRNR_btn = QPushButton(text="Settings", parent=self.window)
                self.CRNR_btn.setFixedSize(100,40)
                self.CRNR_btn.setGeometry(12, 12, 10, 10)
                self.CRNR_btn.released.connect(self.Open_Set_Wind)
                
                self.SPCE_sct = QShortcut(QKeySequence('Space'), self.window)

                self.SPCE_sct.activated.connect(self.pic_get)
                self.window.showFullScreen()
                self.window.show()
        
        def Open_Set_Wind(self): 
                self.S_Window = QtWidgets.QMainWindow()
                self.ui = Ui_Sett_Window()
                self.ui.setupUi(self.S_Window, self)
                self.S_Window.show()
                self.S_Window.raise_()
                
        def pic_get(self):
                #button.setEnabled(False)
                config_data = config["DEFAULT"]
                pref = config_data["projectname"]
                loct =config_data["storagepath"]
                dte = datetime.now()
                still_cfg = picam2.create_still_configuration(main={"size": (1920, 1080)})
                pic_name = loct+"/"+pref+"_"+str(dte.day)+str(dte.month)+str(dte.year)+"_"+str(dte.hour)+str(dte.minute)+".jpg"
                picam2.switch_mode_and_capture_file(still_cfg, pic_name, signal_function=qpicamera2.signal_done)
        
        def record_start():
                # Start video capture
                video_cfg = picam2.create_video_configuration(main={"size": (1920, 1080)})
                encoder = H264Encoder()
                output = FfmpegOutput("test_vid.mp4")
                picam2.start_encoder(encoder, output, quality=Quality.MEDIUM)

        def record_stop():
                # Stop video capture
                picam2.stop_encoder()
                
class Ui_Sett_Window(QMainWindow):
        def setupUi(self, Sett_Window, mainWindow):
                Sett_Window.setObjectName("Sett_Window")
                Sett_Window.setEnabled(True)
                Sett_Window.resize(500, 675)
                Sett_Window.setMaximumSize(QtCore.QSize(500, 800))
                Sett_Window.setAcceptDrops(False)
                Sett_Window.setAutoFillBackground(True)
                Sett_Window.setDocumentMode(True)
                Sett_Window.setTabShape(QtWidgets.QTabWidget.Rounded)
                self.centralwidget = QtWidgets.QWidget(Sett_Window)
                self.centralwidget.setObjectName("centralwidget")
                self.Major_gpb = QtWidgets.QGroupBox(self.centralwidget)
                self.Major_gpb.setGeometry(QtCore.QRect(9, 9, 481, 741))
                self.Major_gpb.setFlat(True)
                self.Major_gpb.setObjectName("Major_gpb")
                self.TABS_tab = QtWidgets.QTabWidget(self.Major_gpb)
                self.TABS_tab.setGeometry(QtCore.QRect(6, 29, 471, 481))
                self.TABS_tab.setDocumentMode(True)
                self.TABS_tab.setObjectName("TABS_tab")
                self.CAMS_tab = QtWidgets.QWidget()
                self.CAMS_tab.setObjectName("CAMS_tab")
                self.WB_L = QtWidgets.QLabel(self.CAMS_tab)
                self.WB_L.setGeometry(QtCore.QRect(10, 10, 111, 22))
                self.WB_L.setObjectName("WB_L")
                self.CNTS_L = QtWidgets.QLabel(self.CAMS_tab)
                self.CNTS_L.setGeometry(QtCore.QRect(10, 160, 91, 22))
                self.CNTS_L.setObjectName("CNTS_L")
                self.BRGT_L = QtWidgets.QLabel(self.CAMS_tab)
                self.BRGT_L.setGeometry(QtCore.QRect(10, 70, 91, 22))
                self.BRGT_L.setObjectName("BRGT_L")
                self.STRT_L = QtWidgets.QLabel(self.CAMS_tab)
                self.STRT_L.setGeometry(QtCore.QRect(10, 190, 91, 22))
                self.STRT_L.setObjectName("STRT_L")
                self.SHRP_L = QtWidgets.QLabel(self.CAMS_tab)
                self.SHRP_L.setGeometry(QtCore.QRect(10, 220, 91, 22))
                self.SHRP_L.setObjectName("SHRP_L")
                self.GAIN_L = QtWidgets.QLabel(self.CAMS_tab)
                self.GAIN_L.setGeometry(QtCore.QRect(10, 250, 41, 22))
                self.GAIN_L.setObjectName("GAIN_L")
                self.REDS_L = QtWidgets.QLabel(self.CAMS_tab)
                self.REDS_L.setGeometry(QtCore.QRect(10, 280, 41, 22))
                self.REDS_L.setObjectName("REDS_L")
                self.BLUS_L = QtWidgets.QLabel(self.CAMS_tab)
                self.BLUS_L.setGeometry(QtCore.QRect(220, 290, 91, 22))
                self.BLUS_L.setObjectName("BLUS_L")
                self.CNTT_slr = QtWidgets.QSlider(self.CAMS_tab)
                self.CNTT_slr.setGeometry(QtCore.QRect(130, 160, 271, 21))
                self.CNTT_slr.setMaximum(60)
                self.CNTT_slr.setProperty("value", 10)
                self.CNTT_slr.setOrientation(QtCore.Qt.Horizontal)
                self.CNTT_slr.setObjectName("CNTT_slr")
                self.HOMR_btn = QtWidgets.QPushButton(self.CAMS_tab)
                self.HOMR_btn.setGeometry(QtCore.QRect(10, 370, 131, 41))
                self.HOMR_btn.setAutoExclusive(False)
                self.HOMR_btn.setAutoDefault(False)
                self.HOMR_btn.setDefault(False)
                self.HOMR_btn.setFlat(False)
                self.HOMR_btn.setObjectName("HOMR_btn")
                self.RSDF_btn = QtWidgets.QPushButton(self.CAMS_tab)
                self.RSDF_btn.setGeometry(QtCore.QRect(330, 370, 131, 41))
                self.RSDF_btn.setAutoFillBackground(False)
                self.RSDF_btn.setDefault(False)
                self.RSDF_btn.setObjectName("RSDF_btn")
                self.VEMR_btn = QtWidgets.QPushButton(self.CAMS_tab)
                self.VEMR_btn.setGeometry(QtCore.QRect(170, 370, 131, 41))
                self.VEMR_btn.setObjectName("VEMR_btn")
                self.BRNS_slr = QtWidgets.QSlider(self.CAMS_tab)
                self.BRNS_slr.setGeometry(QtCore.QRect(130, 70, 271, 21))
                self.BRNS_slr.setMinimum(-10)
                self.BRNS_slr.setMaximum(10)
                self.BRNS_slr.setSingleStep(1)
                self.BRNS_slr.setProperty("value", 0)
                self.BRNS_slr.setOrientation(QtCore.Qt.Horizontal)
                self.BRNS_slr.setObjectName("BRNS_slr")
                self.STRT_slr = QtWidgets.QSlider(self.CAMS_tab)
                self.STRT_slr.setGeometry(QtCore.QRect(130, 190, 271, 21))
                self.STRT_slr.setMaximum(60)
                self.STRT_slr.setProperty("value", 10)
                self.STRT_slr.setOrientation(QtCore.Qt.Horizontal)
                self.STRT_slr.setObjectName("STRT_slr")
                self.SHPS_slr = QtWidgets.QSlider(self.CAMS_tab)
                self.SHPS_slr.setGeometry(QtCore.QRect(130, 220, 271, 21))
                self.SHPS_slr.setMaximum(160)
                self.SHPS_slr.setProperty("value", 10)
                self.SHPS_slr.setOrientation(QtCore.Qt.Horizontal)
                self.SHPS_slr.setObjectName("SHPS_slr")
                self.GAIN_slr = QtWidgets.QSlider(self.CAMS_tab)
                self.GAIN_slr.setGeometry(QtCore.QRect(130, 250, 271, 21))
                self.GAIN_slr.setMinimum(0)
                self.GAIN_slr.setMaximum(160)
                self.GAIN_slr.setProperty("value", 0)
                self.GAIN_slr.setOrientation(QtCore.Qt.Horizontal)
                self.GAIN_slr.setObjectName("GAIN_slr")
                self.REDS_spb = QtWidgets.QDoubleSpinBox(self.CAMS_tab)
                self.REDS_spb.setGeometry(QtCore.QRect(80, 285, 101, 31))
                self.REDS_spb.setMaximum(32.0)
                self.REDS_spb.setSingleStep(0.1)
                self.REDS_spb.setEnabled(False)
                self.REDS_spb.setObjectName("REDS_spb")
                self.REDS_spb.setAccelerated(True)
                self.BLUS_spb = QtWidgets.QDoubleSpinBox(self.CAMS_tab)
                self.BLUS_spb.setGeometry(QtCore.QRect(290, 285, 101, 31))
                self.BLUS_spb.setMaximum(32.0)
                self.BLUS_spb.setSingleStep(0.1)
                self.BLUS_spb.setObjectName("BLUS_spb")
                self.BLUS_spb.setAccelerated(True)
                self.BLUS_spb.setEnabled(False)
                self.WHBA_ckx = QtWidgets.QCheckBox(self.CAMS_tab)
                self.WHBA_ckx.setGeometry(QtCore.QRect(190, 10, 95, 28))
                self.WHBA_ckx.setChecked(True)
                self.WHBA_ckx.setObjectName("WHBA_ckx")
                self.WBM_L = QtWidgets.QLabel(self.CAMS_tab)
                self.WBM_L.setGeometry(QtCore.QRect(10, 40, 151, 22))
                self.WBM_L.setObjectName("WBM_L")
                self.WHBM_cbx = QtWidgets.QComboBox(self.CAMS_tab)
                self.WHBM_cbx.setGeometry(QtCore.QRect(190, 40, 121, 21))
                self.WHBM_cbx.setObjectName("WHBM_cbx")
                self.WHBM_cbx.addItems(["Auto", "Incandescent", "Tungsten", "Fluorescent", "Indoor", "Daylight", "Cloudy"])
                self.AUEX_ckx = QtWidgets.QCheckBox(self.CAMS_tab)
                self.AUEX_ckx.setGeometry(QtCore.QRect(190, 100, 95, 28))
                self.AUEX_ckx.setChecked(True)
                self.AUEX_ckx.setObjectName("AUEX_ckx")
                self.AUEX_L = QtWidgets.QLabel(self.CAMS_tab)
                self.AUEX_L.setGeometry(QtCore.QRect(10, 100, 111, 22))
                self.AUEX_L.setObjectName("AUEX_L")
                self.EXTM_L = QtWidgets.QLabel(self.CAMS_tab)
                self.EXTM_L.setGeometry(QtCore.QRect(10, 130, 111, 22))
                self.EXTM_L.setObjectName("EXTM_L")
                self.EXTM_slr = QtWidgets.QSlider(self.CAMS_tab)
                self.EXTM_slr.setEnabled(False)
                self.EXTM_slr.setGeometry(QtCore.QRect(130, 131, 271, 20))
                self.EXTM_slr.setMinimum(75)
                self.EXTM_slr.setMaximum(6000000)
                self.EXTM_slr.setPageStep(100)
                self.EXTM_slr.setOrientation(QtCore.Qt.Horizontal)
                self.EXTM_slr.setObjectName("EXTM_slr")
                self.BRNS_lbl = QtWidgets.QLabel(self.CAMS_tab)
                self.BRNS_lbl.setGeometry(QtCore.QRect(420, 70, 51, 20))
                self.BRNS_lbl.setObjectName("BRNS_lbl")
                self.EXTM_lbl = QtWidgets.QLabel(self.CAMS_tab)
                self.EXTM_lbl.setGeometry(QtCore.QRect(420, 130, 51, 20))
                self.EXTM_lbl.setObjectName("EXTM_lbl")
                self.CNTT_lbl = QtWidgets.QLabel(self.CAMS_tab)
                self.CNTT_lbl.setGeometry(QtCore.QRect(420, 160, 51, 20))
                self.CNTT_lbl.setObjectName("CNTT_lbl")
                self.STRT_lbl = QtWidgets.QLabel(self.CAMS_tab)
                self.STRT_lbl.setGeometry(QtCore.QRect(420, 190, 51, 20))
                self.STRT_lbl.setObjectName("STRT_lbl")
               
                self.SHPS_lbl = QtWidgets.QLabel(self.CAMS_tab)
                self.SHPS_lbl.setGeometry(QtCore.QRect(420, 220, 51, 20))
                self.SHPS_lbl.setObjectName("SHPS_lbl")
        
                self.GAIN_lbl = QtWidgets.QLabel(self.CAMS_tab)
                self.GAIN_lbl.setGeometry(QtCore.QRect(420, 250, 51, 20))
                self.GAIN_lbl.setObjectName("GAIN_lbl")
                self.TABS_tab.addTab(self.CAMS_tab, "")
                self.INSP_tab = QtWidgets.QWidget()
                self.INSP_tab.setObjectName("INSP_tab")
                self.REIM_L = QtWidgets.QLabel(self.INSP_tab)
                self.REIM_L.setGeometry(QtCore.QRect(10, 20, 151, 22))
                self.REIM_L.setObjectName("REIM_L")
                self.MNSM_L = QtWidgets.QLabel(self.INSP_tab)
                self.MNSM_L.setGeometry(QtCore.QRect(10, 70, 151, 22))
                self.MNSM_L.setObjectName("MNSM_L")
                self.REIM_txb = QtWidgets.QLineEdit(self.INSP_tab)
                self.REIM_txb.setGeometry(QtCore.QRect(170, 20, 121, 30))
                self.REIM_txb.setObjectName("REIM_txb")
                self.REIM_btn = QtWidgets.QPushButton(self.INSP_tab)
                self.REIM_btn.setGeometry(QtCore.QRect(320, 20, 131, 30))
                self.REIM_btn.setObjectName("REIM_btn")
                self.MNSM_spb = QtWidgets.QDoubleSpinBox(self.INSP_tab)
                self.MNSM_spb.setGeometry(QtCore.QRect(170, 60, 121, 31))
                self.MNSM_spb.setAccelerated(True)
                self.MNSM_spb.setSingleStep(.01)
                self.MNSM_spb.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
                self.MNSM_spb.setProperty("value", 99.99)
                self.MNSM_spb.setObjectName("MNSM_spb")
                self.BOOT_btn = QtWidgets.QPushButton(self.INSP_tab)
                self.BOOT_btn.setGeometry(QtCore.QRect(160, 330, 131, 30))
                self.BOOT_btn.setObjectName("BOOT_btn")
                self.STRT_L_2 = QtWidgets.QLabel(self.INSP_tab)
                self.STRT_L_2.setGeometry(QtCore.QRect(10, 330, 151, 22))
                self.STRT_L_2.setObjectName("STRT_L_2")
                self.CRSH_gpb = QtWidgets.QGroupBox(self.INSP_tab)
                self.CRSH_gpb.setGeometry(QtCore.QRect(30, 120, 401, 191))
                self.CRSH_gpb.setFlat(False)
                self.CRSH_gpb.setCheckable(False)
                self.CRSH_gpb.setObjectName("CRSH_gpb")
                self.CRH1_cbx = QtWidgets.QCheckBox(self.CRSH_gpb)
                self.CRH1_cbx.setGeometry(QtCore.QRect(10, 30, 95, 28))
                self.CRH1_cbx.setObjectName("CRH1_cbx")
                self.CRH2_cbx = QtWidgets.QCheckBox(self.CRSH_gpb)
                self.CRH2_cbx.setGeometry(QtCore.QRect(10, 70, 95, 28))
                self.CRH2_cbx.setObjectName("CRH2_cbx")
                self.CRV1_cbx = QtWidgets.QCheckBox(self.CRSH_gpb)
                self.CRV1_cbx.setGeometry(QtCore.QRect(10, 110, 95, 28))
                self.CRV1_cbx.setObjectName("CRV1_cbx")
                self.CRV2_cbx = QtWidgets.QCheckBox(self.CRSH_gpb)
                self.CRV2_cbx.setGeometry(QtCore.QRect(10, 150, 95, 28))
                self.CRV2_cbx.setObjectName("CRV2_cbx")
                self.CH1C_cbb = QtWidgets.QComboBox(self.CRSH_gpb)
                self.CH1C_cbb.setGeometry(QtCore.QRect(190, 30, 101, 30))
                self.CH1C_cbb.setObjectName("CH1C_cbb")
                self.CH1C_cbb.addItem("")
                self.CH1C_cbb.addItem("")
                self.CH1C_cbb.addItem("")
                self.CH1C_cbb.addItem("")
                self.CH1C_cbb.addItem("")
                self.CH1C_cbb.addItem("")
                self.CH1C_cbb.addItem("")
                self.CH1L_spb = QtWidgets.QSpinBox(self.CRSH_gpb)
                self.CH1L_spb.setGeometry(QtCore.QRect(320, 30, 71, 31))
                self.CH1L_spb.setAccelerated(True)
                self.CH1L_spb.setMaximum(1080)
                self.CH1L_spb.setObjectName("CH1L_spb")
                self.CH2L_spb = QtWidgets.QSpinBox(self.CRSH_gpb)
                self.CH2L_spb.setGeometry(QtCore.QRect(320, 70, 71, 31))
                self.CH2L_spb.setAccelerated(True)
                self.CH2L_spb.setMaximum(1080)
                self.CH2L_spb.setObjectName("CH2L_spb")
                self.CV1L_spb = QtWidgets.QSpinBox(self.CRSH_gpb)
                self.CV1L_spb.setGeometry(QtCore.QRect(320, 110, 71, 31))
                self.CV1L_spb.setAccelerated(True)
                self.CV1L_spb.setMaximum(1920)
                self.CV1L_spb.setObjectName("CV1L_spb")
                self.CV2L_spb = QtWidgets.QSpinBox(self.CRSH_gpb)
                self.CV2L_spb.setGeometry(QtCore.QRect(320, 150, 71, 31))
                self.CV2L_spb.setAccelerated(True)
                self.CV2L_spb.setMaximum(1920)
                self.CV2L_spb.setObjectName("CV2L_spb")
                self.CRH1_L = QtWidgets.QLabel(self.CRSH_gpb)
                self.CRH1_L.setGeometry(QtCore.QRect(90, 30, 91, 31))
                self.CRH1_L.setObjectName("CRH1_L")
                self.CRH2_L = QtWidgets.QLabel(self.CRSH_gpb)
                self.CRH2_L.setGeometry(QtCore.QRect(90, 70, 91, 31))
                self.CRH2_L.setObjectName("CRH2_L")
                self.CRV1_L = QtWidgets.QLabel(self.CRSH_gpb)
                self.CRV1_L.setGeometry(QtCore.QRect(90, 110, 91, 31))
                self.CRV1_L.setObjectName("CRV1_L")
                self.CRV2_L = QtWidgets.QLabel(self.CRSH_gpb)
                self.CRV2_L.setGeometry(QtCore.QRect(90, 150, 91, 31))
                self.CRV2_L.setObjectName("CRV2_L")
                self.CH1C_cbb_2 = QtWidgets.QComboBox(self.CRSH_gpb)
                self.CH1C_cbb_2.setGeometry(QtCore.QRect(190, 70, 101, 30))
                self.CH1C_cbb_2.setObjectName("CH1C_cbb_2")
                self.CH1C_cbb_2.addItem("")
                self.CH1C_cbb_2.addItem("")
                self.CH1C_cbb_2.addItem("")
                self.CH1C_cbb_2.addItem("")
                self.CH1C_cbb_2.addItem("")
                self.CH1C_cbb_2.addItem("")
                self.CH1C_cbb_2.addItem("")
                self.CH1C_cbb_3 = QtWidgets.QComboBox(self.CRSH_gpb)
                self.CH1C_cbb_3.setGeometry(QtCore.QRect(190, 110, 101, 30))
                self.CH1C_cbb_3.setObjectName("CH1C_cbb_3")
                self.CH1C_cbb_3.addItem("")
                self.CH1C_cbb_3.addItem("")
                self.CH1C_cbb_3.addItem("")
                self.CH1C_cbb_3.addItem("")
                self.CH1C_cbb_3.addItem("")
                self.CH1C_cbb_3.addItem("")
                self.CH1C_cbb_3.addItem("")
                self.CH1C_cbb_4 = QtWidgets.QComboBox(self.CRSH_gpb)
                self.CH1C_cbb_4.setGeometry(QtCore.QRect(190, 150, 101, 30))
                self.CH1C_cbb_4.setObjectName("CH1C_cbb_4")
                self.CH1C_cbb_4.addItem("")
                self.CH1C_cbb_4.addItem("")
                self.CH1C_cbb_4.addItem("")
                self.CH1C_cbb_4.addItem("")
                self.CH1C_cbb_4.addItem("")
                self.CH1C_cbb_4.addItem("")
                self.CH1C_cbb_4.addItem("")
                self.TABS_tab.addTab(self.INSP_tab, "")
                self.SYST_tab = QtWidgets.QWidget()
                self.SYST_tab.setObjectName("SYST_tab")
               
                self.DDAY_spb = QtWidgets.QSpinBox(self.SYST_tab)
                self.DDAY_spb.setGeometry(QtCore.QRect(150, 10, 61, 31))
                self.DDAY_spb.setMinimum(1)
                self.DDAY_spb.setMaximum(31)
                self.DDAY_spb.setObjectName("DDAY_spb")
                self.MMNT_spb = QtWidgets.QSpinBox(self.SYST_tab)
                self.MMNT_spb.setGeometry(QtCore.QRect(220, 10, 61, 31))
                self.MMNT_spb.setMinimum(1)
                self.MMNT_spb.setMaximum(12)
                self.MMNT_spb.setObjectName("Mmnt_spb")
                self.YYER_spb = QtWidgets.QSpinBox(self.SYST_tab)
                self.YYER_spb.setGeometry(QtCore.QRect(300, 10, 81, 31))
                self.YYER_spb.setMinimum(2000)
                self.YYER_spb.setMaximum(2100)
                self.YYER_spb.setObjectName("YYER_spb")
                self.HHUR_spb = QtWidgets.QSpinBox(self.SYST_tab)
                self.HHUR_spb.setGeometry(QtCore.QRect(150, 60, 61, 31))
                self.HHUR_spb.setMinimum(1)
                self.HHUR_spb.setMaximum(24)
                self.HHUR_spb.setObjectName("HHUR_spb")
                self.MINT_spb = QtWidgets.QSpinBox(self.SYST_tab)
                self.MINT_spb.setGeometry(QtCore.QRect(220, 60, 61, 31))
                self.MINT_spb.setMaximum(60)
                self.MINT_spb.setObjectName("MINT_spb")
                self.DATI_btn = QtWidgets.QPushButton(self.SYST_tab)
                self.DATI_btn.setGeometry(QtCore.QRect(320, 60, 131, 30))
                self.DATI_btn.setObjectName("DATI_btn")
               
                self.DATE_L = QtWidgets.QLabel(self.SYST_tab)
                self.DATE_L.setGeometry(QtCore.QRect(10, 10, 91, 31))
                self.DATE_L.setObjectName("DATE_L")
                self.TIME_L = QtWidgets.QLabel(self.SYST_tab)
                self.TIME_L.setGeometry(QtCore.QRect(10, 60, 91, 31))
                self.TIME_L.setObjectName("TIME_L")
                self.SHTD_btn = QtWidgets.QPushButton(self.SYST_tab)
                self.SHTD_btn.setGeometry(QtCore.QRect(10, 240, 131, 41))
                self.SHTD_btn.setObjectName("SHTD_btn")
                self.REBT_btn = QtWidgets.QPushButton(self.SYST_tab)
                self.REBT_btn.setGeometry(QtCore.QRect(320, 240, 131, 41))
                self.REBT_btn.setObjectName("REBT_btn")
                self.PJNM_L = QtWidgets.QLabel(self.SYST_tab)
                self.PJNM_L.setGeometry(QtCore.QRect(10, 110, 111, 31))
                self.PJNM_L.setObjectName("PJNM_L")
                self.PJNM_txb = QtWidgets.QLineEdit(self.SYST_tab)
                self.PJNM_txb.setGeometry(QtCore.QRect(150, 110, 141, 30))
                self.PJNM_txb.setObjectName("PJNM_txb")
                self.PJNM_btn = QtWidgets.QPushButton(self.SYST_tab)
                self.PJNM_btn.setGeometry(QtCore.QRect(320, 110, 131, 30))
                self.PJNM_btn.setObjectName("PJNM_btn")
                self.FLST_L = QtWidgets.QLabel(self.SYST_tab)
                self.FLST_L.setGeometry(QtCore.QRect(10, 160, 111, 31))
                self.FLST_L.setObjectName("FLST_L")
                self.FLST_txb = QtWidgets.QLineEdit(self.SYST_tab)
                self.FLST_txb.setGeometry(QtCore.QRect(150, 170, 141, 30))
                self.FLST_txb.setObjectName("FLST_txb")
                self.FLST_btn = QtWidgets.QPushButton(self.SYST_tab)
                self.FLST_btn.setGeometry(QtCore.QRect(320, 170, 131, 30))
                self.FLST_btn.setObjectName("FLST_btn")
                self.TABS_tab.addTab(self.SYST_tab, "")
                self.CLSE_btn = QtWidgets.QPushButton(self.Major_gpb)
                self.CLSE_btn.setGeometry(QtCore.QRect(170, 550, 140, 40))
                self.CLSE_btn.setObjectName("CLSE_btn")
                self.SNAP_btn = QtWidgets.QPushButton(self.Major_gpb)
                self.SNAP_btn.setGeometry(QtCore.QRect(10, 550, 130, 40))
                self.SNAP_btn.setObjectName("SNAP_btn")
                self.VIDC_btn = QtWidgets.QPushButton(self.Major_gpb)
                self.VIDC_btn.setGeometry(QtCore.QRect(340, 550, 130, 40))
                self.VIDC_btn.setObjectName("VIDC_btn")
                Sett_Window.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(Sett_Window)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 27))
                self.menubar.setObjectName("menubar")
                Sett_Window.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(Sett_Window)
                self.statusbar.setObjectName("statusbar")
                Sett_Window.setStatusBar(self.statusbar)

                self.retranslateUi(Sett_Window)
                self.TABS_tab.setCurrentIndex(0)
                self.CLSE_btn.released.connect(Sett_Window.deleteLater)
                QtCore.QMetaObject.connectSlotsByName(Sett_Window)
#######################Widget - retrieving ini values 
                config_data = config["DEFAULT"]
                self.BRNS_slr.setValue(int(config_data["brightness"]))
                self.SHPS_slr.setValue(int(config_data["sharpness"]))
                self.STRT_slr.setValue(int(config_data["saturation"]))
                self.CNTT_slr.setValue(int(config_data["contrast"]))
                
                self.BRNS_lbl.setNum(int(config_data["brightness"])/10)
                self.SHPS_lbl.setNum(int(config_data["sharpness"])/10)
                self.STRT_lbl.setNum(int(config_data["saturation"])/10)
                self.CNTT_lbl.setNum(int(config_data["contrast"])/10)
                
                self.PJNM_txb.setText(config_data["projectname"])
                self.REIM_txb.setText(config_data["irisimage"])
                self.FLST_txb.setText(config_data["storagepath"])
                
                self.MNSM_spb.setValue(float(config_data["minimumsim"]))
                
#######################Widget - command linking 
        
                self.REIM_btn.released.connect(self.Base_Img_Sel)
                self.FLST_btn.released.connect(self.Storage_Dir)
                self.REBT_btn.released.connect(self.Reboot)
                self.SHTD_btn.released.connect(self.Shutdown)
                self.RSDF_btn.released.connect(self.Restore_Def)
                self.PJNM_btn.released.connect(self.Project_Ren)
                
                self.HOMR_btn.released.connect(self.Horiz_Mirror)
                self.VEMR_btn.released.connect(self.Verti_Mirror)
                
                self.SNAP_btn.released.connect(self.SNAP_get)
                self.VIDC_btn.released.connect(self.VIDC_get)
                self.BOOT_btn.released.connect(self.Iris_Boot)
                self.DATI_btn.released.connect(self.Update_DateTime)

                
                self.WHBA_ckx.stateChanged.connect(self.awb_update) 
                self.AUEX_ckx.stateChanged.connect(self.AutoExpTim_chck) 
		
                self.MNSM_spb.valueChanged.connect(self.Upd_IrisP) 
                
                self.CNTT_slr.valueChanged['int'].connect(self.CNTT_Update)
                self.BRNS_slr.valueChanged['int'].connect(self.BRNS_Update)
                self.EXTM_slr.valueChanged['int'].connect(self.EXTM_Update)
                self.STRT_slr.valueChanged['int'].connect(self.STRT_Update)
                self.SHPS_slr.valueChanged['int'].connect(self.SHPS_Update)
                self.GAIN_slr.valueChanged['int'].connect(self.GAIN_lbl.setNum)
                self.REDS_spb.valueChanged.connect(self.awb_update)
                self.BLUS_spb.valueChanged.connect(self.awb_update)
                
                self.WHBM_cbx.currentIndexChanged.connect(self.awb_update)

        
        ##Functions for widgets         
        def Base_Img_Sel(self):
                Iris_base_IMG, _ = QFileDialog.getOpenFileName(self, 'Select Image', "", "All File(*);;Images(*.jpg ,*png)")
                self.REIM_txb.setText(Iris_base_IMG)
                config_data = config["DEFAULT"]
                config_data["irisimage"] = str(Iris_base_IMG)
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
                Iris_base_IMG = cv2.imread(Iris_base_IMG)
                cv2.imwrite("/media/diego/USB/PyQt_Apps/Base.jpg", Iris_base_IMG) ##Missing its specific Directory
		
        def Storage_Dir(self):
                Storage_Path = QFileDialog.getExistingDirectory(self, "Select Storage Device") ## Missing how it should only be removable drives3
                self.FLST_txb.setText(Storage_Path)	
                config_data = config["DEFAULT"]
                config_data["storagepath"] = Storage_Path
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
                

        def awb_dict(self):
                ret = {
                "AwbEnable": self.WHBA_ckx.isChecked(),
                "AwbMode": self.WHBM_cbx.currentIndex(),
                "ColourGains": [self.REDS_spb.value(), self.BLUS_spb.value()]
                }
                if self.WHBA_ckx.isChecked():
                        del ret["ColourGains"]
                return ret

        def awb_update(self):
                self.REDS_spb.setMinimum(picam2.camera_controls["ColourGains"][0] + 0.01)
                self.REDS_spb.setMaximum(picam2.camera_controls["ColourGains"][1])
                self.BLUS_spb.setMinimum(picam2.camera_controls["ColourGains"][0] + 0.01)
                self.BLUS_spb.setMaximum(picam2.camera_controls["ColourGains"][1])

                self.REDS_spb.setEnabled(not self.WHBA_ckx.isChecked())
                self.BLUS_spb.setEnabled(not self.WHBA_ckx.isChecked())
                # print(self.awb_dict)
                picam2.set_controls(self.awb_dict())
			
        def AutoExpTim_chck(self):
                checker = self.AUEX_ckx
                if self.AUEX_ckx.isChecked():
                        self.EXTM_slr.setEnabled(False)
                        picam2.set_controls({"AeEnable": True})
                else:
                        self.EXTM_slr.setEnabled(True)
                        picam2.set_controls({"AeEnable": False})
                        
        def Restore_Def(self):
                self.AUEX_ckx.setCheckState(1)
                self.WHBA_ckx.setCheckState(1)
                self.BRNS_slr.setValue(0)
                self.EXTM_slr.setValue(75)
                self.BLUS_spb.setValue(0)
                self.REDS_spb.setValue(0)
                self.GAIN_slr.setValue(0)
                self.SHPS_slr.setValue(10)
                self.STRT_slr.setValue(10)
                self.CNTT_slr.setValue(10)
			
        def Shutdown(self):
                picam2.stop()
                os.system('sudo shutdown now')
		
        def Reboot(self):
                picam2.stop()
                os.system('sudo reboot now')
                
        def Update_DateTime(self): 
                day = self.DDAY_spb.value()
                month = self.MMNT_spb.value()
                year = self.YYER_spb.value()
                hour = self.HHUR_spb.value()
                minute = self.MINT_spb.value()
                date_string = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)
                os.system("sudo date -s'"+date_string+"'")
                os.system('sudo reboot now')
	
        def Project_Ren(self):
                N_name = self.PJNM_txb.text()
                config_data = config["DEFAULT"]
                config_data["projectname"] = N_name
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
			
        def Upd_IrisP(self):
                Min_Perc = self.MNSM_spb.value()
                config_data = config["DEFAULT"]
                config_data["minimumsim"] = str(round(Min_Perc,4))
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
                        
        def CNTT_Update(self, value):
                config_data = config["DEFAULT"]
                config_data["contrast"] = str(value)
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
                picam2.set_controls({"Contrast": value/10})
                self.CNTT_lbl.setNum(value/10)
                
        def STRT_Update(self, value):
                config_data = config["DEFAULT"]
                config_data["saturation"] = str(value)
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
                picam2.set_controls({"Saturation": value/10})   
                self.STRT_lbl.setNum(value/10)
                
        def SHPS_Update(self, value):
                config_data = config["DEFAULT"]
                config_data["sharpness"] = str(value)
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
                picam2.set_controls({"Sharpness": value/10})
                self.SHPS_lbl.setNum(value/10)
        
        def BRNS_Update(self, value):
                config_data = config["DEFAULT"]
                config_data["brightness"] = str(value)
                with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                        config.write(f)
                picam2.set_controls({"Brightness": (value/10)})
                self.BRNS_lbl.setNum(value/10)
                
        def EXTM_Update(self, value):
                picam2.set_controls({"ExposureTime": value})

        def Horiz_Mirror(self):  ##Las variables estan volteadas a proposito 
                global H_toggle
                config_data = config["DEFAULT"]
                
                if not H_toggle: 
                        picam2.stop()
                        picam2_pConfig["transform"] = libcamera.Transform(vflip=1)
                        picam2.configure(picam2_pConfig)
                        config_data["hmirror"] = str(1)
                        with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                                config.write(f)

                        picam2.start()
                        H_toggle = True
                else: 
                        picam2.stop()
                        picam2_pConfig["transform"] = libcamera.Transform(vflip=0)
                        picam2.configure(picam2_pConfig)
                        config_data["hmirror"] = str(0)
                        with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                                config.write(f)

                        picam2.start()
                        H_toggle = False 
        
        def Verti_Mirror(self):
                global V_toggle
                config_data = config["DEFAULT"]
                
                if not V_toggle: 
                        picam2.stop()
                        picam2_pConfig["transform"] = libcamera.Transform(hflip=1)
                        picam2.configure(picam2_pConfig)
                        picam2.configure(picam2_pConfig)
                        config_data["vmirror"] = str(1)
                        with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                                config.write(f)

                        picam2.start()
                        V_toggle = True
                else: 
                        picam2.stop()
                        picam2_pConfig["transform"] = libcamera.Transform(hflip=0)
                        picam2.configure(picam2_pConfig)
                        picam2.configure(picam2_pConfig)
                        config_data["vmirror"] = str(0)
                        with open("/media/diego/USB/PyQt_Apps/IRISConfig.ini","w") as f: 
                                config.write(f)

                        picam2.start()
                        V_toggle = False
        
        def SNAP_get(self): 
                self.SNAP_btn.setEnabled(False)
                Main_Preview.pic_get(self)
                self.SNAP_btn.setEnabled(True)
        
        def VIDC_get(self): 
                global recording
                if not recording:
                        self.TABS_tab.setEnabled(False)
                        self.VIDC_btn.setText("Stop Video")	
                        self.SNAP_btn.setEnabled(False)
                        Main_Preview.record_start()
                        recording = True
                else:				
                        self.TABS_tab.setEnabled(True)
                        self.VIDC_btn.setText("Take Video")
                        self.SNAP_btn.setEnabled(True)
                        Main_Preview.record_stop()
                        recording = False
                        
        def Iris_Boot(self): 
                atexit.register(on_Exit)
                sys.exit()
                #app.quit()
                      
        
        def retranslateUi(self, Sett_Window):
                _translate = QtCore.QCoreApplication.translate
                Sett_Window.setWindowTitle(_translate("Sett_Window", "Settings Menu"))
                self.Major_gpb.setTitle(_translate("Sett_Window", "Settings Menu "))
                self.WB_L.setText(_translate("Sett_Window", "White Balance"))
                self.CNTS_L.setText(_translate("Sett_Window", "Contrast "))
                self.BRGT_L.setText(_translate("Sett_Window", "Brightness "))
                self.STRT_L.setText(_translate("Sett_Window", "Saturation "))
                self.SHRP_L.setText(_translate("Sett_Window", "Sharpness "))
                self.GAIN_L.setText(_translate("Sett_Window", "Gain "))
                self.REDS_L.setText(_translate("Sett_Window", "Red "))
                self.BLUS_L.setText(_translate("Sett_Window", "Blue "))
                self.HOMR_btn.setText(_translate("Sett_Window", "Horizontal Mirror"))
                self.RSDF_btn.setText(_translate("Sett_Window", "Restore Defaults"))
                self.VEMR_btn.setText(_translate("Sett_Window", "Vertical Mirror"))
                self.WHBA_ckx.setText(_translate("Sett_Window", "Auto "))
                self.WBM_L.setText(_translate("Sett_Window", "White Balance Mode"))
                #self.WHBM_cbx.setItemText(0,_translate("Sett_Window", "Auto"))
                #self.WHBM_cbx.setItemText(1,_translate("Sett_Window", "Incandescent"))
                #self.WHBM_cbx.setItemText(2,_translate("Sett_Window", "Tungsten"))
                #self.WHBM_cbx.setItemText(3,_translate("Sett_Window", "Fluorescent"))
                #self.WHBM_cbx.setItemText(4,_translate("Sett_Window", "Indoor"))
                #self.WHBM_cbx.setItemText(5,_translate("Sett_Window", "Daylight"))
                #self.WHBM_cbx.setItemText(6,_translate("Sett_Window", "Cloudy"))
                self.AUEX_ckx.setText(_translate("Sett_Window", "Auto "))
                self.AUEX_L.setText(_translate("Sett_Window", "Auto Exposure"))
                self.EXTM_L.setText(_translate("Sett_Window", "Exposure Time"))
                self.BRNS_lbl.setText(_translate("Sett_Window", "0"))
                self.EXTM_lbl.setText(_translate("Sett_Window", "75"))
                self.CNTT_lbl.setText(_translate("Sett_Window", "1"))
                self.STRT_lbl.setText(_translate("Sett_Window", "1"))
  
                self.SHPS_lbl.setText(_translate("Sett_Window", "1"))
              
                self.GAIN_lbl.setText(_translate("Sett_Window", "0"))
                self.TABS_tab.setTabText(self.TABS_tab.indexOf(self.CAMS_tab), _translate("Sett_Window", " Camera  "))
                self.REIM_L.setText(_translate("Sett_Window", "Reference Image:"))
                self.MNSM_L.setText(_translate("Sett_Window", "Minimum Similarity:"))
                self.REIM_btn.setText(_translate("Sett_Window", "Search"))
                self.MNSM_spb.setSuffix(_translate("Sett_Window", "%"))
                self.BOOT_btn.setText(_translate("Sett_Window", "Enable"))
                self.STRT_L_2.setText(_translate("Sett_Window", "Begin Inspection"))
                self.CRSH_gpb.setTitle(_translate("Sett_Window", "Crosshairs"))
                self.CRH1_cbx.setText(_translate("Sett_Window", "Show"))
                self.CRH2_cbx.setText(_translate("Sett_Window", "Show"))
                self.CRV1_cbx.setText(_translate("Sett_Window", "Show"))
                self.CRV2_cbx.setText(_translate("Sett_Window", "Show"))
                self.CH1C_cbb.setItemText(0, _translate("Sett_Window", "Red"))
                self.CH1C_cbb.setItemText(1, _translate("Sett_Window", "Blue"))
                self.CH1C_cbb.setItemText(2, _translate("Sett_Window", "Green"))
                self.CH1C_cbb.setItemText(3, _translate("Sett_Window", "Yellow"))
                self.CH1C_cbb.setItemText(4, _translate("Sett_Window", "Orange"))
                self.CH1C_cbb.setItemText(5, _translate("Sett_Window", "Purple"))
                self.CH1C_cbb.setItemText(6, _translate("Sett_Window", "Pink"))
                self.CRH1_L.setText(_translate("Sett_Window", "Horizontal"))
                self.CRH2_L.setText(_translate("Sett_Window", "Horizontal"))
                self.CRV1_L.setText(_translate("Sett_Window", "Vertical"))
                self.CRV2_L.setText(_translate("Sett_Window", "Vertical"))
                self.CH1C_cbb_2.setItemText(0, _translate("Sett_Window", "Red"))
                self.CH1C_cbb_2.setItemText(1, _translate("Sett_Window", "Blue"))
                self.CH1C_cbb_2.setItemText(2, _translate("Sett_Window", "Green"))
                self.CH1C_cbb_2.setItemText(3, _translate("Sett_Window", "Yellow"))
                self.CH1C_cbb_2.setItemText(4, _translate("Sett_Window", "Orange"))
                self.CH1C_cbb_2.setItemText(5, _translate("Sett_Window", "Purple"))
                self.CH1C_cbb_2.setItemText(6, _translate("Sett_Window", "Pink"))
                self.CH1C_cbb_3.setItemText(0, _translate("Sett_Window", "Red"))
                self.CH1C_cbb_3.setItemText(1, _translate("Sett_Window", "Blue"))
                self.CH1C_cbb_3.setItemText(2, _translate("Sett_Window", "Green"))
                self.CH1C_cbb_3.setItemText(3, _translate("Sett_Window", "Yellow"))
                self.CH1C_cbb_3.setItemText(4, _translate("Sett_Window", "Orange"))
                self.CH1C_cbb_3.setItemText(5, _translate("Sett_Window", "Purple"))
                self.CH1C_cbb_3.setItemText(6, _translate("Sett_Window", "Pink"))
                self.CH1C_cbb_4.setItemText(0, _translate("Sett_Window", "Red"))
                self.CH1C_cbb_4.setItemText(1, _translate("Sett_Window", "Blue"))
                self.CH1C_cbb_4.setItemText(2, _translate("Sett_Window", "Green"))
                self.CH1C_cbb_4.setItemText(3, _translate("Sett_Window", "Yellow"))
                self.CH1C_cbb_4.setItemText(4, _translate("Sett_Window", "Orange"))
                self.CH1C_cbb_4.setItemText(5, _translate("Sett_Window", "Purple"))
                self.CH1C_cbb_4.setItemText(6, _translate("Sett_Window", "Pink"))
                self.TABS_tab.setTabText(self.TABS_tab.indexOf(self.INSP_tab), _translate("Sett_Window", "Inspection"))
                self.DATI_btn.setText(_translate("Sett_Window", "Update D/T"))
                        
                self.DATE_L.setText(_translate("Sett_Window", "Date: "))
                self.TIME_L.setText(_translate("Sett_Window", "Time: "))
                self.SHTD_btn.setText(_translate("Sett_Window", "Shutdown"))
                self.REBT_btn.setText(_translate("Sett_Window", "Reboot"))
                self.PJNM_L.setText(_translate("Sett_Window", "Project Name: "))
                self.PJNM_btn.setText(_translate("Sett_Window", "Update"))
                self.FLST_L.setText(_translate("Sett_Window", "File Storage: "))
                self.FLST_btn.setText(_translate("Sett_Window", "Search"))
                self.TABS_tab.setTabText(self.TABS_tab.indexOf(self.SYST_tab), _translate("Sett_Window", " System "))
                self.CLSE_btn.setText(_translate("Sett_Window", "Close"))

                self.SNAP_btn.setText(_translate("Sett_Window", "Take Picture"))
                self.VIDC_btn.setText(_translate("Sett_Window", "Take Video"))
        
def capture_done(job):
        picam2.wait(job)
        #button.setEnabled(True)
def on_Exit():
        picam2.stop()
        picam2.close()
        os.system('python3 /media/diego/USB/PyQt_Apps/SSIM2App.py')
        app.quit()
        print ("ByeBye")        

app = QApplication([])

qpicamera2 = QGlPicamera2(picam2, width=1920, height=1080, keep_ar=False)
qpicamera2.done_signal.connect(capture_done)

UIWindow = Main_Preview()
app.exec()
