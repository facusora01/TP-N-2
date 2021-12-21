import csv
from geopy.geocoders import Nominatim
from geopy import distance


def lectura_del_csv():

    with open(r"pedidos.csv") as archivo:
        ciudad: csv = csv.reader(archivo, delimiter=',')
        lista_de_ciudades: list = []

        for ciudades in ciudad:
            if ciudades[3] not in lista_de_ciudades:
                lista_de_ciudades.append(ciudades[3])

    return lista_de_ciudades



def geolocalizacion(ciudades):
    ciudades.pop(0)
    geolocalizador = Nominatim(user_agent="TP_2")
    cooredenadas_de_empresa: tuple = (-34.9204529,-57.9881899)

    distancia_de_ciudades: list = []

    for ciudad in range(len(ciudades)):
        ciudades[ciudad] = [ciudades[ciudad], 'Argentina']

    for i in range(len(ciudades)):

        localidad = geolocalizador.geocode(ciudades[i])
        ubicacion: tuple = (localidad.latitude, localidad.longitude)
        distancia_ciudad: int = (distance.distance(ubicacion, cooredenadas_de_empresa).km)
        distancia_de_ciudades.append(distancia_ciudad)
        distancia_de_ciudades[i] = [ciudades[i][0], distancia_ciudad]

    distancia_de_ciudades: list = sorted(distancia_de_ciudades, key=lambda x: (x[1]))
    

    return distancia_de_ciudades
    

def main():
    print('')


    ciudades: list = lectura_del_csv()

    coordenadas: list = geolocalizacion(ciudades)

    print(coordenadas)

main()