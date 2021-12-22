import csv
from geopy.geocoders import Nominatim, nominatim
from geopy import distance, location

#Constantes:

#decidimos por poner nuestra sede en La Plata
COORDENADAS_DE_EMPRESA: tuple = (-34.9204529,-57.9881899)


def lectura_del_csv()-> list:
    
    #POST: Se lee el .csv, y se extrae su informacion

    with open(r"pedidos.csv") as archivo:
        ciudad: csv = csv.reader(archivo, delimiter=',')
        next(ciudad)
        lista_de_ciudades: list = []
        
        for ciudades in ciudad:
            if ciudades[3] not in lista_de_ciudades:
                lista_de_ciudades.append(ciudades[3])

    return lista_de_ciudades



def geolocalizacion(ciudades)-> list:

    #PRE: Recibe como parametros una lista con las ciudades de los envios
    #POST: Se hace un for, para especificar que las ciudades son de Argentina, luego en , otro for, revisa cada distancia de cada ciudad conrespecto a la ubicacion de la sede,
    # luego se hace un sorted() para organizar las ciudades de las mas cercana a la mas lejana. Devolviendo una lista ya organizada.


    
    geolocalizador: nominatim = Nominatim(user_agent="TP_2")
    

    distancia_de_ciudades: list = []

    for ciudad in range(len(ciudades)):
        ciudades[ciudad] = [ciudades[ciudad], 'Argentina']

    for i in range(len(ciudades)):

        localidad: location = geolocalizador.geocode(ciudades[i])
        ubicacion: tuple = (localidad.latitude, localidad.longitude)
        distancia_ciudad: int = (distance.distance(ubicacion, COORDENADAS_DE_EMPRESA).km)
        distancia_de_ciudades.append(distancia_ciudad)
        distancia_de_ciudades[i] = [ciudades[i][0], distancia_ciudad]

    distancia_de_ciudades: list = sorted(distancia_de_ciudades, key=lambda x: (x[1]))
    

    return distancia_de_ciudades
    

def main()-> None:
    print('')


    ciudades: list = lectura_del_csv()

    coordenadas: list = geolocalizacion(ciudades)

    print(coordenadas)

main()