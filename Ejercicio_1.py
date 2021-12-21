import csv
import time
import utils as u

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
        leer = csv.reader(archivo)
        pedidos_temporal = list(leer)
    pedidos = pedidos_temporal
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
        writer = csv.writer(archivo)
        for fila in pedidos:
            writer.writerow(fila)

def abm_pedidos() -> None:
    """
    Muestra el menu abm con sus respectivas opciones
    """ 
    lista_pedidos: list = lectura_csv()
    mostrar_menu(lista_pedidos)
    limpiar_csv()
    escribir_csv(lista_pedidos)

abm_pedidos()