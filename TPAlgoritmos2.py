import csv

# 5 - Determinar cuáles fueron los pedidos que fueron a la ciudad de Rosario y valorizarlos. 

def pedidosRosarinos():
    with open('pedidos.csv', 'r') as archivo:
        leer = csv.reader(archivo)
        lista = list(leer)

    precio_1334: int = 15
    precio_568: int = 8

    print("Los pedidos a Rosario fueron:")
    for fila in lista:
        if fila != lista[0]:
            try:
                if fila[3] == "Rosario":
                    print(f"El pedido número {fila[0]} de la fecha {fila[1]} con {fila[7]} unidades del articulo numero {fila[5]} de color {fila[6]}.")
                    if fila[5] == "1334":
                        precio_pedido = int(fila[7]) * precio_1334
                    elif fila[5] == "568":
                        precio_pedido = int(fila[7]) * precio_568
                    porcentajeDescuento: int = int(fila[8])
                    descuento: float = precio_pedido * (porcentajeDescuento / 100)
                    print(f"Costo: ${precio_pedido - descuento}")
            except IndexError:
                pass

pedidosRosarinos()

# 6 - Cuál es el artículo más pedido y cuántos de ellos fueron entregados. 

def articuloMasPedidosYMasEntregados():
    with open('pedidos.csv', 'r') as archivo:
        leer = csv.reader(archivo)
        lista = list(leer)

    articulos: dict = {}
    
    for fila in lista:
        try:
            if fila != lista[0]:
                if articulos.get(f"{fila[5]} ({fila[6]})"):
                    articulos[f"{fila[5]} ({fila[6]})"] += int(fila[7])
                else:
                    articulos[f"{fila[5]} ({fila[6]})"] = int(fila[7])
        except IndexError:
            pass
    
    print(f"El articulo más pedido es el numero {max(articulos, key=articulos.get)} con {articulos[max(articulos, key=articulos.get)]} unidades entregadas")

articuloMasPedidosYMasEntregados()