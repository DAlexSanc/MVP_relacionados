#!/usr/bin/python3

import time

import numpy as np

from picamera2 import Picamera2, Preview

import datetime

import time

import cv2

from skimage.metrics import structural_similarity

picam2 = Picamera2()

bandera = False    #esta nos va a ayudar a determinara que etapa del programa vamos 
lsize = (640, 360) # Variable que dicta la resoucion de todo lo lores (HD/3)
                   # En caso de perder muchos fps la hacemos mas chica en multiplos de 1920x1080p

def grayscale(image):
	# Convierte la imagen a grises 
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
	return image_gray 
	
def lower_resolution(image): 
	# Baja la resolucion de la imagen para simplificar
	image_LR = cv2.resize(image, dsize=(lsize), interpolation = cv2.INTER_AREA)
	return image_LR 
	
def base_preparing(image):
	# Prepara la imagen base para no hacerlo de paso a paso 
	base_gray = grayscale(image)  
	base_LR = lower_resolution(base_gray) 
	base_Y = base_LR[:,:,0]
	return base_LR

def SSIM(img1, img2):
	mask = np.zeros((lsize[1], lsize[0], 4), dtype = np.uint8) ##Numpy maneja X y Y volteados, ergo el 240, 320
	(score, diff) = structural_similarity(img1, img2, full=True)
	diff = (diff * 255).astype("uint8")
	# Threshold the difference and produce a mask 
	# Count the number of pixels currently on to determine similarity 
	thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[0] if len(contours) == 2 else contours[1]

	for c in contours:
		area = cv2.contourArea(c)
		if area > 40:
			cv2.drawContours(mask, [c], 0, (255,0,0, 120), -1)
			cv2.resize(mask, dsize=(1920, 1080), interpolation = cv2.INTER_LINEAR)
	return (mask, score) # Esta imagen es la que nos interesaria mostrar ya en la GUI 


preview_config = picam2.create_preview_configuration(main = {"size": (1920, 1080), "format": "XRGB8888"}, lores={"size": (lsize), "format": "YUV420"}, raw=picam2.sensor_modes[2])
picam2.configure(preview_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
##### Aqui en ambas instancias cuando declaramos una configuracion,
##### estamos declarando el sensor mode para preservar FoV
##### que es basicamente la vista de la camara, y usamos el 2 
##### ya que es el modo nativo a 1080p (Puede cambiar al 1 en la version final, pero eso esta por verse)

##### Adicionalmente, como vas a poder ver, ya no usamos la imagen 1080p para comparar
##### Usamos el "Lores" que es la imagen que sale paralela a la HD, pero en una resolucion menor 
##### Y al ser YUV en lugar de RGB ya basicamente es escala de grises  

while bandera == False:
	print("First while")
	time.sleep(5)
	print("Slept")
	cfg = picam2.create_still_configuration(main={"size": (1920,1080)}, raw=picam2.sensor_modes[2])
	picam2.switch_mode_and_capture_file(cfg, "test.jpg")
	base = cv2.imread("test.jpg")
	base_ppd = base_preparing(base)
	print("Changing")
	bandera = True
	
while bandera == True:
	print("New Process")
	array = picam2.capture_array("lores")
	grey = array[:lsize[1] ,:lsize[0]]  ## Aqui suceden dos cosas raras, lo primero, el :X es porque 
	base_Y = base_ppd[:,:,0]  ## la imagen lores se duplica de formas extranas, pero al decirle  
	mask, score_F = SSIM(base_Y, grey) # que corte la imagen en el pixel X, deja de suceder el doblete
	picam2.set_overlay(mask)  ## la otra, como YUV es una matriz, tratamos la otra imagen como una matriz 
	print (score_F)           ## dejando solo el canal de grises. 
	
	
	
