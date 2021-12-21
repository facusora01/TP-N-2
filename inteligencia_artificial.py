import cv2
import numpy as np
import os

ROJO_HSV: list = [[0, 50, 70], [9, 255, 255]]
AMARILLO_HSV: list = [[20, 100, 100], [30, 255, 255]]
AZUL_HSV: list = [[90, 50, 70], [128, 255, 255]]
VERDE_HSV: list = [[36, 50, 70], [89, 255, 255]]
NEGRO_HSV: list = [[0, 0, 0], [180, 255, 30]]
MINIMO_PREDICCION: int = 0.3

def cargar_red() -> tuple:
	"""
	PRE: no recibe ningun parametro pero requiere los archivos yolov3.weights, yolov3.cfg y coco.names
	POST: carga la red de YOLO y la devuelve en una tupla junto con las clases de objetos y los nombres de capas
	"""
	red: cv2.dnn_Net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
	clases: list = []
	with open("coco.names", "r") as f:
		clases: list = [linea.strip() for linea in f.readlines()]
	nombres_capas: tuple = red.getLayerNames()
	capas: list = [nombres_capas[i-1] for i in red.getUnconnectedOutLayers()]
	return red, clases, capas

def cargar_imagen(ruta_imagen: str) -> tuple:
	"""
	PRE: recibe como parametro la ruta de la imagen
	POST: lee la imagen y la redimensiona, luego la devuelve en una tupla junto con su altura y su peso
	"""
	imagen: np.ndarray = cv2.imread(ruta_imagen)
	imagen: np.ndarray = cv2.resize(imagen, None, fx=0.4, fy=0.4)
	altura, peso, canales = imagen.shape
	return imagen, altura, peso

def detectar_objetos(imagen: np.ndarray, red: cv2.dnn_Net, capas: list) -> tuple:
	"""
	PRE: recibe como parametro la imagen, la red y las capas
	POST: devuelve los datos de los objetos detectados en la imagen (coordenadas x e y del centro del 
	objeto, su altura y peso, la puntuacion que hay de cada clase de los objetos en el archivo coco.names)
	"""
	blob: np.ndarray = cv2.dnn.blobFromImage(imagen, scalefactor=0.00392, size=(320, 320), mean=(0, 0, 0), swapRB=True, crop=False)
	red.setInput(blob)
	datos_objetos: tuple = red.forward(capas)
	return datos_objetos

def dimensiones(datos_objetos: tuple, altura: int, peso: int) -> tuple:
	"""
	PRE: recibe como parametros los datos del objeto previamente mencionados, la altura y el peso
	POST: devuelve tres listas; una con las medidas de las cuadriculas recuadrando los objetos, otra con 
	las puntuaciones mas altas entre todas las clases de objetos y la ultima con los indices de esas clases
	"""
	cuadriculas: list = []
	prediccion_objetos: list = []
	indices_clases: list = []
	
	for datos in datos_objetos:
		for detectar in datos:
			puntajes: np.ndarray = detectar[5:]
			indice_clase: np.int64 = np.argmax(puntajes)
			prediccion: np.float32 = puntajes[indice_clase]
			if prediccion > MINIMO_PREDICCION:
				centro_x: int = int(detectar[0] * peso)
				centro_y: int = int(detectar[1] * altura)
				w: int = int(detectar[2] * peso)
				h: int = int(detectar[3] * altura)
				x: int = int(centro_x - w/2)
				y: int = int(centro_y - h / 2)
				cuadriculas.append([x, y, w, h])
				prediccion_objetos.append(float(prediccion))
				indices_clases.append(indice_clase)
	return cuadriculas, prediccion_objetos, indices_clases

def etiquetar(cuadriculas: list, prediccion_objetos: list, indices_clases: list, clases: list) -> str:
	"""
	PRE: recibe como parametros las cuadriculas, las predicciones, los indices y las clases del objeto
	POST: devuelve el nombre del objeto detectado
	"""
	indices: np.ndarray = cv2.dnn.NMSBoxes(cuadriculas, prediccion_objetos, 0.5, 0.4)
	for i in range(len(cuadriculas)):
		if i in indices:
			etiqueta: str = str(clases[indices_clases[i]])
	return etiqueta

def detectar_imagen(ruta_imagen: str) -> str:
	"""
	PRE: recibe como parametro la ruta de la imagen
	POST: devuelve unicamente el nombre del objeto
	"""
	red, clases, capas = cargar_red()
	imagen, altura, peso = cargar_imagen(ruta_imagen)
	datos_objetos = detectar_objetos(imagen, red, capas)
	cuadriculas, prediccion_objetos, indices_clases = dimensiones(datos_objetos, altura, peso)
	etiqueta: str = etiquetar(cuadriculas, prediccion_objetos, indices_clases, clases)
	return etiqueta

def colores(ruta_imagen: str, menor_array: list, mayor_array: list) -> bool:
	"""
	PRE: recibe la ruta de la imagen y los valores HSV de un color
	POST: devuelve un booleano que analiza si en la imagen predomina el color dado por parametro o no
	"""
	imagen: np.ndarray = cv2.imread(ruta_imagen)
	imagen_HSV: np.ndarray = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
	abajo: np.ndarray = np.array(menor_array)
	arriba: np.ndarray = np.array(mayor_array)
	mascara: np.ndarray = cv2.inRange(imagen_HSV, abajo, arriba)
	img_resultado: np.ndarray = cv2.bitwise_and(imagen, imagen, mask=mascara)
	cantidad: float = np.sum(img_resultado) / np.sum(imagen_HSV)

	return cantidad > 0.001

def color_predominante(ruta_imagen: str, objeto: str, dicc_colores_botellas: dict, dicc_colores_vasos: dict) -> None:
	"""
	PRE: recibe como parametro la ruta de la imagen, el objeto previamente detectado, un diccionario
	de botellas y otro de vasos
	POST: no devuelve nada, solo modifica los diccionarios dependiendo del color predominante en la imagen
	"""
	lista_colores: list = [ROJO_HSV, AMARILLO_HSV, AZUL_HSV, VERDE_HSV, NEGRO_HSV]
	lista_booleanos: list = []
	for color in lista_colores:
		booleano: bool = colores(ruta_imagen, color[0], color[1])
		lista_booleanos.append(booleano)
	
	if objeto == "cup":
		if lista_booleanos[2] == True:
			dicc_colores_vasos["Azul"] += 1
		elif lista_booleanos[4] == True:
			dicc_colores_vasos["Negro"] += 1
	if objeto == "bottle":
		if lista_booleanos[0] == True:
			dicc_colores_botellas["Rojo"] += 1
		elif lista_booleanos[1] == True:
			dicc_colores_botellas["Amarillo"] += 1
		elif lista_booleanos[2] == True:
			dicc_colores_botellas["Azul"] += 1
		elif lista_booleanos[3] == True:
			dicc_colores_botellas["Verde"] += 1
		elif lista_booleanos[4] == True:
			dicc_colores_botellas["Negro"] += 1

def objetos() -> dict:
	"""
	PRE: no recibe ningun parametro
	POST: devuelve un diccionario con los dos objetos como claves
	"""
	dicc_objetos: dict = {}
	dicc_colores_botellas: dict = {"Amarillo": 0, "Rojo": 0, "Azul": 0, "Negro": 0, "Verde": 0}
	dicc_colores_vasos: dict = {"Negro": 0, "Azul": 0}
	ruta: str = os.getcwd() + "\\Lote0001"
	nombre_imagenes: list = os.listdir(ruta)
	for imagen in nombre_imagenes:
		ruta_imagen: str = os.path.join(ruta, imagen)
		objeto: str = detectar_imagen(ruta_imagen)
		if objeto != "bottle" and objeto != "cup":
			print("PROCESO DETENIDO, se reanuda en 1 minuto")
		color_predominante(ruta_imagen, objeto, dicc_colores_botellas, dicc_colores_vasos)
		if objeto == "bottle":
			dicc_objetos["Botellas"] = dicc_colores_botellas
		elif objeto == "cup":
			dicc_objetos["Vasos"] = dicc_colores_vasos

	return dicc_objetos


def cantidad_botellas(dicc_objetos: dict) -> None:
	"""
	PRE: recibe un diccionario con los objetos por parametro
	POST: modifica el archivo de texto botellas.txt pero no devuelve nada
	"""
	valores: dict = dicc_objetos.get("Botellas")
	with open("botellas.txt", "w") as botellas:
		for valor in valores:
			botellas.write(f"{valor} {valores[valor]}")
			botellas.write("\n")
    
def cantidad_vasos(dicc_objetos: dict) -> None:
	"""
	PRE: recibe un diccionario con los objetos por parametro
	POST: modifica el archivo de texto vasos.txt pero no devuelve nada
	"""
	valores: dict = dicc_objetos.get("Vasos")
	with open("vasos.txt", "w") as vasos:
		for valor in valores:
			vasos.write(f"{valor} {valores[valor]}")
			vasos.write("\n")

def main() -> None:
	"""
	PRE: no recibe ningun parametro
	POST: no devuelve nada, solo llama a las funciones
	"""
	dicc_objetos: dict = objetos()
	cantidad_botellas(dicc_objetos)
	cantidad_vasos(dicc_objetos)
