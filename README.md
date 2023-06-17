# MVP_relacionados
De aqui podras cosechar codigo para la aplicacion y la documentacion de Raspicam2. 

Dentro de la carpeta de Picam2 esta todo lo relacionado a la parte de vision, desde un par de ejemplos de como sacar la imagen de la camara y entregarla a Opencv, hasta a montarla en PyQt. 
La version final de mi aplicacion de inspeccion es el archivo que dice SSIM2App, ese lee el config para determinar los parametros de la camara y solo esta haciendo la comparacion de la imagen. 
El Base_Window es lo que yo desarrolle, si hay algo de codigo que te sirva cosechalo, si no pues, con que te sirva para entender que es lo que estamos buscando usar es suficiente, lo unico que considero yo que vale la pena mencionar es que dentro de esos codigos los directorios estan a mi raspberry asi que eliminalos, o ajustalos a donde lo pongas, solo reemplaza "diego" por el tuyo. 

Debido a que la camara no puede usarse en dos procesos a la vez pienso yo que la solucion mas sencilla seria tener dos versiones de la aplicacion que se alternen cuando esta usandose la inspeccion, pero tienes completa libertad de hacerlo como quieras en tanto funcione y no perdamos calidad en la imagen. 
