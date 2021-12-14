import cv2
import numpy as np
import os

def cargar_red() -> tuple:
	net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
	classes: list = []
	with open("coco.names", "r") as f:
		classes = [line.strip() for line in f.readlines()]
	layers_names = net.getLayerNames()
	output_layers = [layers_names[i-1] for i in net.getUnconnectedOutLayers()]
	return net, classes, output_layers

def cargar_imagen(img_path) -> tuple:
	img = cv2.imread(img_path)
	img = cv2.resize(img, None, fx=0.4, fy=0.4)
	height, width, channels = img.shape
	return img, height, width

def detectar_objetos(img, net, outputLayers) -> tuple:			
	blob = cv2.dnn.blobFromImage(img, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	net.setInput(blob)
	outputs = net.forward(outputLayers)
	return outputs

def etiqueta(boxes, confs, class_ids, classes) -> str:
	indexes = cv2.dnn.NMSBoxes(boxes, confs, 0.5, 0.4)
	for i in range(len(boxes)):
		if i in indexes:
			label = str(classes[class_ids[i]])
	return label

def dimensiones(outputs, height, width) -> tuple:
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

def image_detect(img_path) -> str:
	model, classes, output_layers = cargar_red()
	image, height, width = cargar_imagen(img_path)
	outputs = detectar_objetos(image, model, output_layers)
	boxes, confs, class_ids = dimensiones(outputs, height, width)
	label: str = etiqueta(boxes, confs, class_ids, classes)
	return label

def colores(path_imagen, lower_array, upper_array) -> bool:
	img = cv2.imread(path_imagen)
	img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower = np.array(lower_array)
	upper = np.array(upper_array)
	mask = cv2.inRange(img_HSV, lower, upper)
	img_result = cv2.bitwise_and(img, img, mask=mask)
	cantidad: float = np.sum(img_result) / np.sum(img_HSV)

	if cantidad > 0.001:
		return True
	else:
		return False

def color_predominante(path_imagen, objeto, dicc_colores_botellas, dicc_colores_vasos) -> None:
	rojo: bool = colores(path_imagen, [0, 50, 70], [9, 255, 255])
	amarillo: bool = colores(path_imagen, [20, 100, 100], [30, 255, 255])
	azul: bool = colores(path_imagen, [90, 50, 70], [128, 255, 255])
	verde: bool = colores(path_imagen, [36, 50, 70], [89, 255, 255])
	negro: bool = colores(path_imagen, [0, 0, 0], [180, 255, 30])
	lista_colores: list = [rojo, amarillo, azul, verde, negro]
	for color in range(len(lista_colores)):
		if lista_colores[color] == True:
			if color == 0 and (objeto == "bottle"):
				dicc_colores_botellas["Rojo"] += 1
			elif color == 1 and (objeto == "bottle"):
				dicc_colores_botellas["Amarillo"] += 1
			elif color == 2:
				if objeto == "bottle":
					dicc_colores_botellas["Azul"] += 1
				elif objeto == "cup":
					dicc_colores_vasos["Azul"] += 1
			elif color == 3 and (objeto == "bottle"):
				dicc_colores_botellas["Verde"] += 1
			elif color == 4:
				if objeto == "bottle":
					dicc_colores_botellas["Negro"] += 1
				elif objeto == "cup":
					dicc_colores_vasos["Negro"] += 1

def main() -> dict:
	dicc_objetos: dict = {}
	dicc_colores_botellas: dict = {"Amarillo": 0, "Rojo": 0, "Azul": 0, "Negro": 0, "Verde": 0}
	dicc_colores_vasos: dict = {"Negro": 0, "Azul": 0}
	path: str = os.getcwd() + "\\Lote0001"
	nombre_imagenes: list = os.listdir(path)
	for imagen in nombre_imagenes:
		path_imagen: str = path + "\\" + imagen
		objeto: str = image_detect(path_imagen)
		if objeto != "bottle" and objeto != "cup":
			print("PROCESO DETENIDO, se reanuda en 1 minuto")
		color_predominante(path_imagen, objeto, dicc_colores_botellas, dicc_colores_vasos)
		if objeto == "bottle":
			dicc_objetos["Botellas"] = dicc_colores_botellas
		elif objeto == "cup":
			dicc_objetos["Vasos"] = dicc_colores_vasos

	return dicc_objetos
