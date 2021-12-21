import csv

def csv_a_lista() -> list:
    with open('pedidos.csv', 'r') as archivo:
            leer: csv = csv.reader(archivo)
            lista: list = list(leer)
    return lista