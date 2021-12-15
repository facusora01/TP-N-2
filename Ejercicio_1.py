import csv
import time

def input_numerico(texto: str) -> int:
    """
    Solicita un valor con el texto cargado en el argumento y mientras el valor no sea numerico, no termina el proceso.
    texto: Texto a mostrar para solicitar el input
    """
    ingreso: str
    espacio()
    valido: bool = False
    ingreso: str = input(f"{texto}")
    if (ingreso.isnumeric()):
        valido = True
    while (not valido):
        espacio()
        print("Ha ingresado un valor invalido, vuelva a intentar\n")
        continuar: str = input("Presione ENTER para continuar")
        espacio()
        ingreso: str = input(f"{texto}")
        if (ingreso.isnumeric()):
            valido = True
    ingreso = int(ingreso)
    return ingreso

def espacio() -> None:
    """
    Imprime saltos de linea para limpiar la consola de comandos para una mejor experiencia del usuario
    """ 
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def menu_generico(titulo:str = None, subtitulo: str = None, opciones:dict = None) -> int:
    """
    Muestra el menu de opciones y solicita una entrada que debe coincidir con alguna de las existentes, caso contrario
    informara el error de entrada y volvera a repetir el proceso.
    """
    espacio()
    contador_opciones: int = 1
    valido = False
    if (titulo):
        print(f"{titulo}\n")
    if (subtitulo):
        print(f"{subtitulo}\n")
    for i in (opciones):
        print(f"[{contador_opciones}] {opciones[i]}\n")
        contador_opciones += 1
    pregunta: str = input("")
    if (pregunta.isnumeric()):
        if (int(pregunta) in opciones.keys()):
            valido = True
    while (not valido):
        espacio()
        print("Entrada invalida, vuelva a intentarlo\n")
        continuar: str = input("Presione ENTER para continuar")
        espacio()
        contador_opciones: int = 1
        if (titulo):
            print(f"{titulo}\n")
        if (subtitulo):
            print(f"{subtitulo}\n")
        for i in (opciones):
            print(f"[{contador_opciones}] {opciones[i]}\n")
            contador_opciones += 1
        pregunta: str = input("")
        if (pregunta.isnumeric()):
            if (int(pregunta) in opciones.keys()):
                valido = True
    return int(pregunta)

def alta_pedidos(lista: list) -> list:
    """
    Solicita el ingreso de los datos necesarios para agregar un nuevo pedido a la lista
    """
    espacio()
    print("Alta de pedidos\n")
    continuar: str = input("Presione ENTER para continuar...")
    espacio()
    numero_pedido: str = str(input_numerico("Ingrese el numero de pedido: "))
    espacio()
    fecha: str = input("Ingrese la fecha del pedido en formato dd/mm/aaaa: ")
    espacio()
    cliente: str = input("Ingrese el nombre del cliente: ")
    espacio()
    provincia: str = input("Ingrese la provincia de destino: ")
    espacio()
    ciudad: str = input("Ingrese la ciudad de destino: ")
    espacio()
    cod_articulo: str = str(input_numerico("Ingrese el codigo de articulo: "))
    espacio()
    color: str = input("Ingrese el color del articulo: ")
    espacio()
    cantidad: str = str(input_numerico("Ingrese la cantidad de unidades: "))
    espacio()
    descuento: str = str(input_numerico("Ingrese el porcentaje de descuento: "))

    lista.append([numero_pedido, fecha, cliente, ciudad, provincia, cod_articulo, color, cantidad, descuento])

    return lista

def modificacion_pedidos(lista: list) -> list:
    """
    Busqueda por numero de pedido, codigo y color de articulo para su modificacion
    """
    espacio()
    print("Modificacion de pedidos")
    continuar: str = input("Presione ENTER para continuar...")
    no_existe: bool = True
    while no_existe:
        espacio()
        numero_pedido: str = str(input_numerico("Ingrese el numero de pedido: "))
        for fila in lista:
            if (fila[0] == numero_pedido):
                no_existe = False
        if (no_existe):
            espacio()
            print("No se encuentra el numero de pedido, intente nuevamente:")
            continuar: str = input("Presione ENTER para continuar...")
    espacio()
    cod_articulo: str = str(input_numerico("Ingrese el codigo de articulo: "))
    espacio()
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
        espacio()
        eleccion: int = menu_generico(titulo=(f"Que desea modificar al pedido {numero_pedido}, articulo {cod_articulo}, color {color}?"), opciones=opciones)
        espacio()
        if not (eleccion == 10):
            cambio: str = input("Ingrese el nuevo valor: ")
            for fila in lista:
                if (fila[0] == numero_pedido and fila[5] == cod_articulo and fila[6] == color):
                    fila[eleccion - 1] = cambio
        else:
            modificando = False
    return lista

def baja_pedidos(lista: list) -> list:
    """
    Busqueda por numero de pedido, codigo y color de articulo para su eliminacion
    """
    espacio()
    print("Baja de pedidos")
    continuar: str = input("Presione ENTER para continuar...")
    no_existe: bool = True
    while no_existe:
        espacio()
        numero_pedido: str = str(input_numerico("Ingrese el numero de pedido: "))
        for fila in lista:
            if (fila[0] == numero_pedido):
                no_existe = False
        if (no_existe):
            espacio()
            print("No se encuentra el numero de pedido, intente nuevamente:")
            continuar: str = input("Presione ENTER para continuar...")
    espacio()
    cod_articulo: str = str(input_numerico("Ingrese el codigo de articulo: "))
    espacio()
    color: str = input("Ingrese el color del articulo: ")
    espacio()
    print(f"Esta a punto de borrar el pedido {numero_pedido}, articulo {cod_articulo}, color {color}\n")
    continuar: str = input("Presione ENTER para continuar o ingrese '1' para salir")
    if continuar == "1":
        return lista
    for fila in lista:
        if (fila[0] == numero_pedido and fila[5] == cod_articulo and fila[6] == color):
            lista.remove(fila)
    return lista

def abm_pedidos() -> None:
    """
    Muestra el menu abm con sus respectivas opciones
    """
    with open('pedidos.csv', 'r') as archivo:
        leer = csv.reader(archivo)
        lista = list(leer)
        opciones: dict = {1: "Alta de pedidos",
                          2: "Modificación de pedidos",
                          3: "Baja de pedidos",
                          4: "Salir"}
        titulo: str = "Menu de alta, baja o modificacion de pedidos"
        abm_ejecucion: bool = True

        while abm_ejecucion:
            eleccion: int = menu_generico(titulo=titulo, opciones=opciones)
            if (eleccion == 1):
                lista = alta_pedidos(lista)
            if (eleccion == 2):
                lista = modificacion_pedidos(lista)
            if (eleccion == 3):
                lista = baja_pedidos(lista)
            if (eleccion == 4):
                espacio()
                print("Saliendo del menu ABM...")
                time.sleep(2)
                espacio()
                abm_ejecucion = False

    f = open("pedidos.csv", "w")
    f.truncate()
    f.close()

    with open('pedidos.csv', 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        for fila in lista:
            writer.writerow(fila)