import datetime
import time
import cv2
from skimage.metrics import structural_similarity
import numpy as np
from picamera2 import Picamera2


global testing 
testing = 0 

bandera = False #esta nos va a ayudar a determinara que etapa del programa vamos 

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
	global testing 
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

	if score < 0.85:          #Aqui se hace la comparacion de el porcentaje minimo de similitud 
		color = (0,0,255)     #El .85 sera reemplazado por el porcentaje que se indique con el GUI 
		if testing == 1:      #Esto es porque si el producto no cumple con el minimo necesitamos guardar la imagen como que fallo 
			cv2.imwrite("Failed.jpg", img3)  #Solo queda pendiente reemplazar el nombre por la fecha hora y projecto 
			testing = 0 
	else:
		color =(255,255,255)

	for c in contours:
		area = cv2.contourArea(c)
		if area > 40:
			x,y,w,h = cv2.boundingRect(c)
			cv2.drawContours(trns, [c], 0, (0,0,255), -1)
			weighted = cv2.addWeighted(img3, 1-alpha, trns, alpha, 0) 
			cv2.putText(weighted, ("{:.2f}%".format(score * 100)), (1740,40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 2 )
	return (weighted) # Esta imagen es la que nos interesaria mostrar ya en la GUI 
	
	
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()

while True:                      ## En realidad de aqui en adelante solo estamos comprobando que funcione 
	print("dentro de el ciclo")  ## Esta parte sera casi toda reemplazada o modificada para funcionar con el Gui correctamente 
	
	while bandera == False: #aqui solo estamos esperando a tomar la foto mientras vemos el video 
		im = picam2.capture_array()
		cv2.imshow("Camera", im)
		if cv2.waitKey(1) & 0xFF == ord('a'):
			cv2.imwrite('base.jpg',im)
			print("tomamos la foto")
			base_img = cv2.imread('base.jpg')
			base_ppd = base_preparing(base_img)
			bandera = True
			cv2.destroyAllWindows()
			print("cambiando de proceso")
			
	while bandera == True: #aqui se procesan los cuadros en vivo para hacer sus restas 
		print("dentro del nuevo proceso")
		im = picam2.capture_array()
		frame_gray = grayscale(im)
		frame_LR = lower_resolution(frame_gray)
		final_img = SSIM(base_ppd, frame_LR, im)  
		#Finally show the complete image 
		cv2.imshow('result',final_img)
		if cv2.waitKey(1) & 0xFF == ord(' '):
			testing = 1 
	
