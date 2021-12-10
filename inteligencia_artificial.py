import cv2
import numpy as np
import os

def load_yolo():
	net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
	classes: list = []
	with open("coco.names", "r") as f:
		classes = [line.strip() for line in f.readlines()]
	layers_names = net.getLayerNames()
	output_layers = [layers_names[i-1] for i in net.getUnconnectedOutLayers()]
	colors = np.random.uniform(0, 255, size=(len(classes), 3))
	return net, classes, colors, output_layers

def load_image(img_path):
	img = cv2.imread(img_path)
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width, channels

def detect_objects(img, net, outputLayers):			
	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return blob, outputs

def draw_labels(boxes, confs, colors, class_ids, classes, img): 
	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
	font = cv2.FONT_HERSHEY_PLAIN
	for i in range(len(boxes)):
		if i in indexes:
			x, y, w, h = boxes[i]
			label = str(classes[class_ids[i]])
			color = colors[i]
	return label

def get_box_dimensions(outputs, height, width):
	boxes: list = []
	confs: list = []
	class_ids: list = []
	for output in outputs:
		for detect in output:
			scores = detect[5:]
			class_id = np.argmax(scores)
			conf = scores[class_id]
			if conf > 0.3:
				center_x = int(detect[0] * width)
				center_y = int(detect[1] * height)
				w = int(detect[2] * width)
				h = int(detect[3] * height)
				x = int(center_x - w/2)
				y = int(center_y - h / 2)
				boxes.append([x, y, w, h])
				confs.append(float(conf))
				class_ids.append(class_id)
	return boxes, confs, class_ids

def image_detect(img_path): 
	model, classes, colors, output_layers = load_yolo()
	image, height, width, channels = load_image(img_path)
	blob, outputs = detect_objects(image, model, output_layers)
	boxes, confs, class_ids = get_box_dimensions(outputs, height, width)
	label: str = draw_labels(boxes, confs, colors, class_ids, classes, image)
	return label
	# key = 0
	# while key != 27:                        # esto no se para que es pero anda bien sin ponerlo, si no se queda colgada la terminal
	# 	key = cv2.waitKey(1)


def color_rojo(path_imagen) -> bool:
	img = cv2.imread(path_imagen)
	img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([0, 50, 70])
	upper = np.array([9, 255, 255])
	mask = cv2.inRange(img_HSV, lower, upper)
	img_result = cv2.bitwise_and(img, img, mask=mask)
	cantidad_rojo: float = np.sum(img_result) / np.sum(img_HSV)
	
	if cantidad_rojo > 0.001:
		return True
	else:
		return False

def color_amarillo(path_imagen) -> bool:
	img = cv2.imread(path_imagen)
	img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([20, 100, 100])
	upper = np.array([30, 255, 255])
	mask = cv2.inRange(img_HSV, lower, upper)
	img_result = cv2.bitwise_and(img, img, mask=mask)
	cantidad_amarillo: float = np.sum(img_result) / np.sum(img_HSV)

	if cantidad_amarillo > 0.001:
		return True
	else:
		return False

def color_azul(path_imagen) -> bool:
	img = cv2.imread(path_imagen)
	img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([90, 50, 70])
	upper = np.array([128, 255, 255])
	mask = cv2.inRange(img_HSV, lower, upper)
	img_result = cv2.bitwise_and(img, img, mask=mask)
	cantidad_azul: float = np.sum(img_result) / np.sum(img_HSV)

	if cantidad_azul > 0.001:
		return True
	else:
		return False

def color_verde(path_imagen) -> bool:
	img = cv2.imread(path_imagen)
	img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([36, 50, 70])
	upper = np.array([89, 255, 255])
	mask = cv2.inRange(img_HSV, lower, upper)
	img_result = cv2.bitwise_and(img, img, mask=mask)
	cantidad_verde: float = np.sum(img_result) / np.sum(img_HSV)

	if cantidad_verde > 0.001:
		return True
	else:
		return False

def color_negro(path_imagen) -> bool:
	img = cv2.imread(path_imagen)
	img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array([0, 0, 0])
	upper = np.array([180, 255, 30])
	mask = cv2.inRange(img_HSV, lower, upper)
	img_result = cv2.bitwise_and(img, img, mask=mask)
	cantidad_negro: float = np.sum(img_result) / np.sum(img_HSV)

	if cantidad_negro > 0.001:
		return True
	else:
		return False

def color_predominante(path_imagen, objeto, dicc_colores_botellas, dicc_colores_vasos):
	if (color_amarillo(path_imagen) == True) and (objeto == "bottle"):
		dicc_colores_botellas["Amarillo"] += 1
	elif (color_rojo(path_imagen) == True) and (objeto == "bottle"):
		dicc_colores_botellas["Rojo"] += 1
	elif (color_azul(path_imagen)) == True:
		if objeto == "bottle":			
			dicc_colores_botellas["Azul"] += 1
		elif objeto == "cup":
			dicc_colores_vasos["Azul"] += 1
	elif (color_negro(path_imagen) == True):
		if objeto == "bottle":			
			dicc_colores_botellas["Negro"] += 1
		elif objeto == "cup":
			dicc_colores_vasos["Negro"] += 1
	elif (color_verde(path_imagen) == True) and (objeto == "bottle"):
		dicc_colores_botellas["Verde"] += 1
	else:
		return "None"

def main():
	dicc_objetos: dict = {}
	dicc_colores_botellas: dict = {"Amarillo": 0, "Rojo": 0, "Azul": 0, "Negro": 0, "Verde": 0}
	dicc_colores_vasos: dict = {"Negro": 0, "Azul": 0} # hago un contador de los colores de vasos y botellas
	path: str = os.getcwd() + "\\Lote0001"
	nombre_imagenes: list = os.listdir(path)
	for imagen in nombre_imagenes:
		path_imagen: str = path + "\\" + imagen
		objeto: str = image_detect(path_imagen)	
		if objeto != "bottle" and objeto != "cup":
			print("PROCESO DETENIDO, se reanuda en 1 minuto")
		color: str = color_predominante(path_imagen, objeto, dicc_colores_botellas, dicc_colores_vasos)
		if objeto == "bottle":
			dicc_objetos["Botellas"] = dicc_colores_botellas
		elif objeto == "cup":
			dicc_objetos["Vasos"] = dicc_colores_vasos

	# print(dicc_objetos)

main()
