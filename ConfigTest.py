from configparser import ConfigParser

config = ConfigParser()

config["DEFAULT"] = {
	"ProjectName": "IMG",
	"StoragePath": "/media/diego/USB", 
	"MinimumSim": 99.99,
	"irisimage": "", 
	"Brightness": 0,
	"Contrast": 1,
	"Saturation": 1, 
	"Sharpness":1,
	"Hmirror":0, 
	"Vmirror":0
}

with open("IRISConfig.ini","w") as f: 
	config.write(f)
