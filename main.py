import Ejercicio_1 as ej1
import TPAlgoritmos2 as ej5y6
import inteligencia_artificial as ia
import utils as u
from geopy import Nominatim, location
from geopy import distance
import csv
from os import close
import cv2
import numpy as np
import os
import time
from utils import csv_a_lista

PESO_BOTELLAS: int = 0.45
PESO_VASOS: int = 0.35
GEOLOCALIZADOR: Nominatim = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
COORDENADAS_DE_EMPRESA: tuple = (-34.9204529,-57.9881899)
ROJO_HSV: list = [[0, 50, 70], [9, 255, 255]]
AMARILLO_HSV: list = [[20, 100, 100], [30, 255, 255]]
AZUL_HSV: list = [[90, 50, 70], [128, 255, 255]]
VERDE_HSV: list = [[36, 50, 70], [89, 255, 255]]
NEGRO_HSV: list = [[0, 0, 0], [180, 255, 30]]
MINIMO_PREDICCION: int = 0.3


# 5 - Determinar cuáles fueron los pedidos que fueron a la ciudad de Rosario y valorizarlos. 

def pedidos_a_ciudad(ciudad: str) -> None:
    """ Determina cuáles fueron los pedidos que fueron a la ciudad indicada por parametro y los valoriza.
    PRE: Recibe el nombre de una ciudad en formato string.
    """

    DATA: list = csv_a_lista()
    PRECIO_BOTELLA_1334: int = 15
    PRECIO_BOTELLA_568: int = 8

    print(f"Los pedidos a {ciudad} fueron:")
    for fila in DATA:
        if fila != DATA[0] and fila != []:
            if fila[3] == ciudad:
                print(f"El pedido número {fila[0]} de la fecha {fila[1]} con {fila[7]} unidades del articulo numero {fila[5]} de color {fila[6]}.")
                if fila[5] == "1334":
                    precio_pedido = int(fila[7]) * PRECIO_BOTELLA_1334
                elif fila[5] == "568":
                    precio_pedido = int(fila[7]) * PRECIO_BOTELLA_568
                porcentajeDescuento: int = int(fila[8])
                descuento: float = precio_pedido * (porcentajeDescuento / 100)
                print(f"Costo: ${precio_pedido - descuento}")


# 6 - Cuál es el artículo más pedido y cuántos de ellos fueron entregados. 

def articulo_mas_pedido_y_entregados() -> None:
    """ Determina cual fue el articulo más pedido y cuántos de este fueron entregados.
    """
    DATA: list = csv_a_lista()
    articulos: dict = {}
    
    for fila in DATA:
        if fila != DATA[0] and fila != []:
            if articulos.get(f"{fila[5]} ({fila[6]})"):
                articulos[f"{fila[5]} ({fila[6]})"] += int(fila[7])
            else:
                articulos[f"{fila[5]} ({fila[6]})"] = int(fila[7])
    
    print(f"El articulo más pedido es el numero {max(articulos, key=articulos.get)} con {articulos[max(articulos, key=articulos.get)]} unidades entregadas")



def alta_pedidos(pedidos: list) -> list:
    """
    Solicita el ingreso de los datos necesarios para agregar un nuevo pedido a la lista
    """
    u.espacio()
    numero_pedido: str = str(u.input_numerico("Ingrese el numero de pedido: "))
    u.espacio()
    fecha: str = input("Ingrese la fecha del pedido en formato dd/mm/aaaa: ")
    u.espacio()
    cliente: str = input("Ingrese el nombre del cliente: ")
    u.espacio()
    provincia: str = input("Ingrese la provincia de destino: ")
    u.espacio()
    ciudad: str = input("Ingrese la ciudad de destino: ")
    u.espacio()
    cod_articulo: str = str(u.input_numerico("Ingrese el codigo de articulo: "))
    u.espacio()
    color: str = input("Ingrese el color del articulo: ")
    u.espacio()
    cantidad: str = str(u.input_numerico("Ingrese la cantidad de unidades: "))
    u.espacio()
    descuento: str = str(u.input_numerico("Ingrese el porcentaje de descuento: "))

    pedidos.append([numero_pedido, fecha, cliente, ciudad, provincia, cod_articulo, color, cantidad, descuento])

def modificacion_pedidos(pedidos: list) -> list:
    """
    Busqueda por numero de pedido, codigo y color de articulo para su modificacion
    """
    no_existe: bool = True
    while no_existe:
        u.espacio()
        numero_pedido: str = str(u.input_numerico("Ingrese el numero de pedido: "))
        for fila in pedidos:
            if fila:
                if (fila[0] == numero_pedido):
                    no_existe = False
        if (no_existe):
            u.espacio()
            print("No se encuentra el numero de pedido, intente nuevamente:")
            continuar: str = input("Presione ENTER para continuar...")
    u.espacio()
    cod_articulo: str = str(u.input_numerico("Ingrese el codigo de articulo: "))
    u.espacio()
    color: str = input("Ingrese el color del articulo: ")
    modificando: bool = True
    opciones: dict = {1: "Numero de pedido",
                      2: "Fecha",
                      3: "Cliente",
                      4: "Ciudad",
                      5: "Provincia",
                      6: "Codigo de artículo",
                      7: "Color",
                      8: "Cantidad",
                      9: "Descuento",
                      10: "Salir"}
    while modificando:
        u.espacio()
        eleccion: int = u.menu_generico(titulo=(f"Que desea modificar al pedido {numero_pedido}, articulo {cod_articulo}, color {color}?"), opciones=opciones)
        u.espacio()
        if not (eleccion == 10):
            cambio: str = input("Ingrese el nuevo valor: ")
            for fila in pedidos:
                if fila:
                    if (fila[0] == numero_pedido and fila[5] == cod_articulo and fila[6] == color):
                        fila[eleccion - 1] = cambio
        else:
            modificando = False

def baja_pedidos(pedidos: list) -> list:
    """
    Busqueda por numero de pedido, codigo y color de articulo para su eliminacion
    """
    no_existe: bool = True
    while no_existe:
        u.espacio()
        numero_pedido: str = str(u.input_numerico("Ingrese el numero de pedido: "))
        for fila in pedidos:
            if fila:
                if (fila[0] == numero_pedido):
                    no_existe = False
        if (no_existe):
            u.espacio()
            print("No se encuentra el numero de pedido, intente nuevamente:")
            continuar: str = input("Presione ENTER para continuar...")
    u.espacio()
    cod_articulo: str = str(u.input_numerico("Ingrese el codigo de articulo: "))
    u.espacio()
    color: str = input("Ingrese el color del articulo: ")
    u.espacio()
    print(f"Esta a punto de borrar el pedido {numero_pedido}, articulo {cod_articulo}, color {color}\n")
    continuar: str = input("Presione ENTER para continuar o ingrese '1' para salir")
    if continuar == "1":
        return True
    for fila in pedidos:
        if fila:
            if (fila[0] == numero_pedido and fila[5] == cod_articulo and fila[6] == color):
                pedidos.remove(fila)

def mostrar_menu(pedidos: list) -> None:
    """
    Muestra el menu de abm y ejecuta las funciones correspondientes dependiendo del input del usuario
    """
    opciones: dict = {1: "Alta de pedidos",
                          2: "Modificación de pedidos",
                          3: "Baja de pedidos",
                          4: "Salir"}
    titulo: str = "Menu de alta, baja o modificacion de pedidos"
    abm_ejecucion: bool = True

    while abm_ejecucion:
        eleccion: int = u.menu_generico(titulo=titulo, opciones=opciones)
        if (eleccion == 1):
            alta_pedidos(pedidos)
        if (eleccion == 2):
            modificacion_pedidos(pedidos)
        if (eleccion == 3):
            baja_pedidos(pedidos)
        if (eleccion == 4):
            u.espacio()
            abm_ejecucion = False

def lectura_csv() -> list:
    """
    Lee el csv y lo devuelve en forma de lista
    """
    with open('pedidos.csv', 'r') as archivo:
        leer: csv = csv.reader(archivo)
        pedidos_temporal: list = list(leer)
    pedidos: list = pedidos_temporal
    return pedidos

def limpiar_csv() -> None:
    """
    Limpia de informacion el csv para su reescritura
    """
    f = open("pedidos.csv", "w")
    f.truncate()
    f.close()

def escribir_csv(pedidos: list) -> None:
    """
    Reescribe linea a linea el csv ya limpio de informacion
    """
    with open('pedidos.csv', 'w', newline='') as archivo:
        writer: csv = csv.writer(archivo)
        for fila in pedidos:
            if fila: 
                writer.writerow(fila)

def abm_pedidos() -> None:
    """
    Muestra el menu abm con sus respectivas opciones
    """ 
    lista_pedidos: list = lectura_csv()
    mostrar_menu(lista_pedidos)
    limpiar_csv()
    escribir_csv(lista_pedidos)


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

def main_ia() -> None:
	"""
	PRE: no recibe ningun parametro
	POST: no devuelve nada, solo llama a las funciones
	"""
	dicc_objetos: dict = objetos()
	cantidad_botellas(dicc_objetos)
	cantidad_vasos(dicc_objetos)


def leer_csv()-> tuple:

    #POST: Lee el .csv, y devuelve la informacion que traía dentro

    with open(r"pedidos.csv") as archivo:
        informacion: csv = csv.reader(archivo)
        pedidos_temporal: list = list(informacion)

    return pedidos_temporal

def contador_vasos_botellas(ciudad, cod_articulo, cantidad, vasos, botellas, ciudad_destino)-> tuple:

    #PRE: Recibe como paramteros: la ciudad, el cod. del articulo y la cant. del envio. Ademas de 3 listas vacias (vasos, botellas, ciudad_destino)
    #POST: hace un append de cada ciudad a una de las listas vacias. Luego, verifica el contenido y la cant. de cada envio, para luego devolver esos datos

    ciudad_destino.append(ciudad)

    if cod_articulo == '1334':
        botellas+= int(cantidad)
    elif cod_articulo == '568':
        vasos+= int(cantidad)

    return vasos, botellas, ciudad_destino, cantidad


def decisicion_modificacion(total, lectura_csv, vasos, botellas, ciudad_destino)-> tuple:

    #PRE: Recibe como parametros: una lista vacia, la info del .csv, y 3 listas vacias
    #POST: Se crea un for simplemente para remover una lista vacia, luego se crea otro for donde se le preg. al usuario si quiere cambiar la cant. del pedido de cada uno
    # devolviendo una lista con todas las ciudades de los pedidos
    
    for fila in lectura_csv:
        if [] in lectura_csv: 
            lectura_csv.remove([])
    print("")
    for fila in lectura_csv:

        print(fila[0],"\t", fila[1],"\t", fila[2],"\t", fila[3],"\t",fila[4],"\t", fila[5],"\t", fila[6],"\t", fila[7])

        if not 'Cantidad' in fila[7]:
            desicion: str = input("\n\nDesea modificar la cantidad del pedido?\n(Presione 'y', si asi lo desea, sino presione 'Enter): ")
            
            if desicion == 'y':
                try:
                    cantidad: int = int(input("Escriba la nueva cantidad: "))
                    print("")
                    
                    contador: list = contador_vasos_botellas(fila[3], fila[5], cantidad, vasos, botellas, ciudad_destino)
                    total[0] += contador[0]
                    total[1] += contador[1]
                    print("-"*100)

                except ValueError:
                    print('')
                    print("Ese valor no es un numero")
                    print('')
            
            else:
                
                contador: list = contador_vasos_botellas(fila[3], fila[5], fila[7], vasos, botellas, ciudad_destino)
                total[0] += contador[0]
                total[1] += contador[1]
                print("-"*100)

    return contador


def imprimir_tablero(lectura_csv)-> None:

    #PRE: Recibe como parametros los datos del .csv
    #POST: Se encarga de imprimir el tablero. No devuelve nada

    for fila in lectura_csv:
        if not 'Nro. Pedidio' in fila[0]:

            print('\t'.join(str(x) for x in fila))
        
        else:
            print(' '.join(str(x) for x in fila))
            


def direccion_de_pedidos(ciudades_de_pedidos)-> list:

    #PRE: Recibe como parametros: una lista con todas las ciudades de los pedidos
    #POST: se crea una lista de listas con cada ciudad, y un contador de cuantos envios van para cada ciudad

    lista_de_ciudades: list = []

    for ciudad in ciudades_de_pedidos:
        if ciudad not in lista_de_ciudades:
            lista_de_ciudades.append(ciudad)

    for ciudad in range(len(lista_de_ciudades)):
        lista_de_ciudades[ciudad] = [lista_de_ciudades[ciudad], 0]

    for i in range(len(lista_de_ciudades)):
        for ciudad in ciudades_de_pedidos:
            if ciudad == lista_de_ciudades[i][0]:
                lista_de_ciudades[i][1] += 1

    return lista_de_ciudades

def main_ej4() -> None:    

    
    ciudad_destino: list = []
    vasos: int = 0
    botellas: int = 0
    total: list = [0, 0]

    lectura_csv: list = leer_csv()
    modificacion: tuple = decisicion_modificacion(total, lectura_csv, vasos, botellas, ciudad_destino)


    direccion_pedidos: list = direccion_de_pedidos(modificacion[2])


    imprimir_tablero(lectura_csv)

    
    print("\nfueron", len(lectura_csv)-1, "Pedidos")

    print(f"fueron", total[0], "vasos, y", total[1], "botellas")

    for i in range(len(direccion_pedidos)):
        
        print(f"Se dirigen", direccion_pedidos[i][1],"a", direccion_pedidos[i][0])


def zonas(geolocator, pedido: tuple, norte: list, sur: list, centro: list, caba: list, lugar: str, dicc_zonas: dict) -> None:
    """
    PRE: recibe el geolocalizador, una tupla con la informacion del pedido, cuatro listas (una de cada zona), 
    un str con la ubicacion (ciudad, provincia, pais) y un diccionario de zonas
    POST: no devuelve nada, solo modifica el diccionario de zonas
    """
    datos = geolocator.geocode(lugar)
    if abs(datos.latitude) < (35) and ("Ciudad Autónoma de Buenos Aires" not in datos.address):
        if lugar not in norte:
            norte.append(pedido)
        dicc_zonas["Zona Norte"] = norte
    elif (35) < abs(datos.latitude) < (40) and ("Ciudad Autónoma de Buenos Aires" not in datos.address):
        if lugar not in centro:
            centro.append(pedido)
        dicc_zonas["Zona Centro"] = centro
    elif abs(datos.latitude) > (40):
        if lugar not in sur:
            sur.append(pedido)
        dicc_zonas["Zona Sur"] = sur
    elif "Ciudad Autónoma de Buenos Aires" in datos.address:
        if lugar not in caba:
            caba.append(pedido)
        dicc_zonas["CABA"] = caba

def peso_zonas(dicc_zonas: dict, dicc_pesos: dict) -> dict:
    """
    PRE: recibe el diccionario de zonas y el de pesos de cada zona
    POST: modifica y devuelve el diccionario de pesos
    """
    for zona, pedidos in dicc_zonas.items():
        for pedido in pedidos:
            if pedido[4] == "1334":
                dicc_pesos[zona] += (PESO_BOTELLAS * int(pedido[6])) 
            elif pedido[4] == "568":
                dicc_pesos[zona] += (PESO_VASOS * int(pedido[6])) 

    return dicc_pesos

def utilitarios(dicc_pesos: dict) -> dict:
    """
    PRE: recibe el diccionario de pesos de cada zona
    POST: devuelve un diccionario de los utilitarios
    """
    dicc_utilitarios: dict = {}
    dicc_pesos_ord: list = sorted(dicc_pesos.items(), key=lambda x:x[1], reverse=True)
    dicc_utilitarios["Utilitario 001"] = dicc_pesos_ord[2]
    dicc_utilitarios["Utilitario 002"] = dicc_pesos_ord[1]
    dicc_utilitarios["Utilitario 003"] = dicc_pesos_ord[3]
    dicc_utilitarios["Utilitario 004"] = dicc_pesos_ord[0]

    return dicc_utilitarios

def geolocalizacion(lista_ciudades: list) -> list:
    """
    PRE: recibe una lista de ciudades
    POST: devuelve una lista con la ciudades y las distancias a la sede
    """
    distancia_de_ciudades: list = []

    for ciudad in range(len(lista_ciudades)):
        lista_ciudades[ciudad] = [lista_ciudades[ciudad], 'Argentina']

    for i in range(len(lista_ciudades)):

        localidad: location = GEOLOCALIZADOR.geocode(lista_ciudades[i])
        ubicacion: tuple = (localidad.latitude, localidad.longitude)
        distancia_ciudad: int = (distance.distance(ubicacion, COORDENADAS_DE_EMPRESA).km)
        distancia_de_ciudades.append(distancia_ciudad)
        distancia_de_ciudades[i] = [lista_ciudades[i][0], distancia_ciudad]

    distancia_de_ciudades: list = sorted(distancia_de_ciudades, key=lambda x: (x[1]))

    return distancia_de_ciudades

def ciudades(dicc_zonas: dict, ciudades_norte: list, ciudades_sur: list, ciudades_centro: list, ciudades_caba: list) -> list:
    """
    PRE: recibe el diccionario de zonas y cuatro listas de zonas
    POST: devuelve una lista con las cuatro listas de zonas
    """
    lista_ciudades: list = []
    for zona in dicc_zonas.values():
        for pedido in zona:    
            lista_ciudades.append(pedido[2])

    distancia_de_ciudades: list = geolocalizacion(lista_ciudades)

    for ciudad in distancia_de_ciudades:
        for itemzona in dicc_zonas["Zona Norte"]:
            if (ciudad[0] in itemzona and not ciudad[0] in ciudades_norte):
                ciudades_norte.append(ciudad[0])
        for itemzona in dicc_zonas["Zona Sur"]:
            if (ciudad[0] in itemzona and not ciudad[0] in ciudades_sur):
                ciudades_sur.append(ciudad[0])
        for itemzona in dicc_zonas["Zona Centro"]:
            if (ciudad[0] in itemzona and not ciudad[0] in ciudades_centro):
                ciudades_centro.append(ciudad[0])
        for itemzona in dicc_zonas["CABA"]:
            if (ciudad[0] in itemzona and not ciudad[0] in ciudades_caba):
                ciudades_caba.append(ciudad[0])

    return [ciudades_norte, ciudades_sur, ciudades_centro, ciudades_caba]

def ordenando_pedidos(pedidos) -> dict:
    """
    PRE: recibe un diccionario de pedidos
    POST: modifica y devuelve el diccionario de pedidos
    """
    with open("pedidos.csv", encoding="UTF-8") as pedidos_csv:
        lector_csv = csv.reader(pedidos_csv, delimiter=',')
        next(lector_csv)
        for row in lector_csv:
            if row:
                if row[0] not in pedidos:
                    pedidos[row[0]] = [(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])]
                else:
                    pedidos[row[0]].append((row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))

    return pedidos

def imprimir_txt(recorrido: list, peso_por_zonas: dict, info_utilitarios: dict) -> None:
    """
    PRE: recibe una lista con todos los recorridos y dos diccionarios del peso y los utilitarios
    POST: genera la salida.txt con los recorridos en orden
    """
    texto: list = []
    contador_principal: int = 0
    for pesozona in peso_por_zonas:
        texto.append(str(pesozona).upper())
        for utilitario in info_utilitarios:
            if (info_utilitarios[utilitario][0] == pesozona):
                texto.append(utilitario)
        texto.append(str(peso_por_zonas[pesozona]) + " Kg")
        texto.append(recorrido[contador_principal])
        contador_principal += 1

    with open('salida.txt', 'w') as f:
        for linea in texto:
            if (type(linea) == list):
                f.write("\n")
                len_maximo = len(linea)
                contador: int = 1
                for mini_linea in linea:
                    f.write(mini_linea)
                    if (not contador == len_maximo):
                        f.write(", ")
                        contador += 1
            else:
                f.write('\n')
                f.write(linea)

def imprimir_recorrido_zona(recorrido: list) -> None:
    """
    Solicita al usuario el nombre de la zona para mostrar su respectivo recorrido
    """
    #u.espacio()
    lista_zonas: dict = {"Zona Norte": recorrido[0], "Zona Sur": recorrido[1], "Zona Centro": recorrido[2], "Zona CABA": recorrido[3]}
    eleccion_zona: str = input("Ingrese la zona del recorrido a mostrar: ")
    try:
        for ciudad in lista_zonas[eleccion_zona]:
            print(ciudad)
    except:
        print("No existe esa zona...")


def ejercicio_3(activaej2: bool) -> None:
    """
    PRE: no recibe nada
    POST: solo llama a las funciones, no devuelve nada
    """

    dicc_zonas: dict = {}
    pedidos: dict = {}
    norte: list = []
    sur: list = []
    centro: list = []
    caba: list = []
    ciudades_norte: list = []
    ciudades_sur: list = []
    ciudades_centro: list = []
    ciudades_caba: list = []
    dicc_pesos: dict = {"Zona Norte": 0, "Zona Sur": 0, "Zona Centro": 0, "CABA": 0} #contador
    pedidos_ordenados: dict = ordenando_pedidos(pedidos)
    for datos in pedidos_ordenados.values():
        for pedido in datos:
            zonas(GEOLOCALIZADOR, pedido, norte, sur, centro, caba, f"{pedido[2]}, {pedido[3]}, Argentina", dicc_zonas)
    recorrido: list = ciudades(dicc_zonas, ciudades_norte, ciudades_sur, ciudades_centro, ciudades_caba)
    peso_por_zona: dict = peso_zonas(dicc_zonas, dicc_pesos)
    info_utilitarios: dict = utilitarios(dicc_pesos)
    if activaej2:
        imprimir_recorrido_zona(recorrido)
    else:
        imprimir_txt(recorrido, peso_por_zona, info_utilitarios)


def main() -> None:
    opciones: dict = {1: "Alta, baja y modificacion de pedidos",
                      2: "Generar recorrido",
                      3: "Procesar pedidos",
                      4: "Pedidos completados",
                      5: "Pedidos de Rosario",
                      6: "Articulo mas solicitado y numero de entregas",
                      7: "Generar archivo con productos procesados",
                      8: "Salir"}
    titulo: str = "Menú de gestión de Chilly Bottles"
    ejecutando: bool = True

    while ejecutando:
        u.espacio()
        eleccion: int = u.menu_generico(titulo=titulo, opciones=opciones)
        
        if (eleccion == 1):
            u.espacio()
            abm_pedidos()
        if (eleccion == 2):
            u.espacio()
            activaej2: bool = True
            ejercicio_3(activaej2)
        if (eleccion == 3):
            u.espacio()
            activaej2: bool = False
            ejercicio_3(activaej2)
        if (eleccion == 4):
            u.espacio()
            main_ej4()
        if (eleccion == 5):
            u.espacio()
            pedidos_a_ciudad()
        if (eleccion == 6):
            u.espacio()
            articulo_mas_pedido_y_entregados()
        if (eleccion == 7):
            u.espacio()
            main_ia()
        if (eleccion == 8):
            u.espacio()
            print("Gracias! Vuelva pronto\n")
            ejecutando = False

main()