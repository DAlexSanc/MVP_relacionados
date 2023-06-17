import cv2
from skimage.metrics import structural_similarity
import numpy as np
from picamera2 import Picamera2
from datetime import datetime
import time
import os 
import atexit
import sys
from configparser import ConfigParser
config = ConfigParser()
config.read("/media/diego/USB/PyQt_Apps/IRISConfig.ini")



def on_Quit():
	picam2.stop()
	picam2.close()
	os.system('python3 /media/diego/USB/PyQt_Apps/Base_Window.py')
	cv2.destroyAllWindows()
	print("ByeBye")

def grayscale(image):
	# Convierte la imagen a grises 
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	return image_gray 
	
def lower_resolution(image): 
	# Baja la resolucion de la imagen para simplificar
	image_LR = cv2.resize(image, dsize=(320,180), interpolation = cv2.INTER_AREA)
	return image_LR 
	
def base_preparing(image):
	# Prepara la imagen base para no hacerlo de paso a paso 
	base_gray = grayscale(image)  
	base_LR = lower_resolution(base_gray) 
	return base_LR
	
#def boot(): 
#Esta funcion existe para al integrar con la GUI aqui lea la imagen base y el porcentaje maximo de error 

def SSIM(img1, img2, img3):
	#Concentrado de todo el proceso de inspeccion 
	global testing, minsim, loct, pref 
	alpha = .25 
	trns = img3.copy()
	(score, diff) = structural_similarity(img1, img2, full=True)
	diff = (diff * 255).astype("uint8")
	# Threshold the difference and produce a mask 
	# Count the number of pixels currently on to determine similarity 
	thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	thresh_FR = cv2.resize(thresh, dsize=(1920,1080), interpolation = cv2.INTER_LINEAR)
	contours = cv2.findContours(thresh_FR, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[0] if len(contours) == 2 else contours[1]
	if score < minsim:         #Aqui se hace la comparacion de el porcentaje minimo de similitud 
		color = (0,0,255) 
		if testing == 1:
			dte = datetime.now()
			still_cfg = picam2.create_still_configuration(main={"size": (1920, 1080)})
			pic_name = loct+"/"+"Failed_"+pref+"_"+str(dte.day)+str(dte.month)+str(dte.year)+"_"+str(dte.hour)+str(dte.minute)+".jpg"
			cv2.imwrite(pic_name, img3)  #Solo queda pendiente reemplazar el nombre por la fecha hora y projecto 
			testing = 0 
	elif score >= minsim:
		color =(255,255,255)

	for c in contours:
		area = cv2.contourArea(c)
		if area > 40:
			x,y,w,h = cv2.boundingRect(c)
			cv2.drawContours(trns, [c], 0, (0,0,255), -1)
			weighted = cv2.addWeighted(img3, 1-alpha, trns, alpha, 0) 
			cv2.putText(weighted, ("{:.2f}%".format(score * 100)), (1740,40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2 )
	return (weighted) # Esta imagen es la que nos interesaria mostrar ya en la GUI 
	
	
if __name__ == "__main__":
	testing = 0 
	minsim = 0
	loct = ""
	pref = ""
	picam2 = Picamera2()
	config_data = config["DEFAULT"]
	hmirr = config_data["hmirror"]
	vmirr = config_data["vmirror"]
	picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
	picam2_pConfig["transform"] = libcamera.Transform(hflip=vmirr, vflip=hmirr) ##Variables volteadas a proposito 
    picam2.configure(picam2_pConfig)
	picam2.start()
	atexit.register(on_Quit)
	minsim = float(config_data["minimumsim"])/100
	pref = config_data["projectname"]    ##Aqui Recuperamos los datos del ini para poder hacer la comparacion 
	loct = config_data["storagepath"]

	cntt = float(config_data["contrast"])/10
	strn = float(config_data["saturation"])/10
	shrp = float(config_data["sharpness"])/10
	brns = float(config_data["brightness"])/10

	picam2.set_controls({"Brightness": brns})               
	picam2.set_controls({"Sharpness": shrp})                
	picam2.set_controls({"Contrast": cntt})
	picam2.set_controls({"Saturation": strn})   

	while True:                      ## En realidad de aqui en adelante solo estamos comprobando que funcione 
		base_img = cv2.imread('/media/diego/USB/PyQt_Apps/Base.jpg')
		base_ppd = base_preparing(base_img)	
		im = picam2.capture_array()
		frame_gray = grayscale(im)
		frame_LR = lower_resolution(frame_gray)		
		final_img = SSIM(base_ppd, frame_LR, im)  
		#Finally show the complete image 
		cv2.imshow('Inspection',final_img)
		if cv2.waitKey(1) & 0xFF == ord(' '):
			testing = 1 
		if cv2.waitKey(1) & 0xFF == (27):
			sys.exit()
