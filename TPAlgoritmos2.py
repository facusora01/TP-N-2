from utils import csv_a_lista

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

