from picamera2 import Picamera2, Preview
import time

##Ejemplo de como se crea la ventana automaticamente si usamos las herramientas que ya vienen incluidas con Picam2 

picam2 = Picamera2()
picam2.start_preview(Preview.QTGL)


preview_config = picam2.create_preview_configuration({"size":(1920,1080)})
picam2.configure(preview_config)

picam2.start()
time.sleep(10)
