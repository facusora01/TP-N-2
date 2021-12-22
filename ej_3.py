from geopy import Nominatim, location
from geopy import distance
import csv

PESO_BOTELLAS: int = 0.45
PESO_VASOS: int = 0.35
GEOLOCALIZADOR: Nominatim = Nominatim(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36")
COORDENADAS_DE_EMPRESA: tuple = (-34.9204529,-57.9881899)

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

def geolocalizacion(lista_ciudades):

    distancia_de_ciudades: list = []

    for ciudad in range(len(lista_ciudades)):
        lista_ciudades[ciudad] = [lista_ciudades[ciudad], 'Argentina']

    for i in range(len(lista_ciudades)):

        localidad = GEOLOCALIZADOR.geocode(lista_ciudades[i])
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

    distancia_de_ciudades = geolocalizacion(lista_ciudades)

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

def imprimir_txt(recorrido: list, peso_por_zonas: dict, info_utilitarios: dict):
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
                for mini_linea in linea:
                    f.write(mini_linea)
                    f.write(", ")
            else:
                f.write('\n')
                f.write(linea)

def main() -> None:
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
    dicc_pesos: dict = {"Zona Norte": 0, "Zona Centro": 0, "Zona Sur": 0, "CABA": 0} #contador
    pedidos_ordenados: dict = ordenando_pedidos(pedidos)
    for datos in pedidos_ordenados.values():
        for pedido in datos:
            zonas(GEOLOCALIZADOR, pedido, norte, sur, centro, caba, f"{pedido[2]}, {pedido[3]}, Argentina", dicc_zonas)
    
    recorrido: list = ciudades(dicc_zonas, ciudades_norte, ciudades_sur, ciudades_centro, ciudades_caba)
    peso_por_zona: dict = peso_zonas(dicc_zonas, dicc_pesos)
    info_utilitarios: dict = utilitarios(dicc_pesos)
    imprimir_txt(recorrido, peso_por_zona, info_utilitarios)

main()