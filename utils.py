def input_numerico(texto: str) -> int:
    """
    Solicita un valor con el texto cargado en el argumento y mientras el valor no sea numerico, no termina el proceso.
    texto: Texto a mostrar para solicitar el input
    """
    ingreso: str
    valido: bool = False
    while (not valido):
        espacio()
        ingreso: str = input(f"{texto}")
        if (ingreso.isnumeric()):
            valido = True
        else:
            espacio()
            print("Ha ingresado un valor invalido, vuelva a intentar\n")
            continuar: str = input("Presione ENTER para continuar")
    ingreso = int(ingreso)
    return ingreso

def espacio() -> None:
    """
    Imprime saltos de linea para limpiar la consola de comandos para una mejor experiencia del usuario
    """ 
    print("\n" * 62)

def menu_generico(titulo:str = None, subtitulo: str = None, opciones:dict = None) -> int:
    """
    Muestra el menu de opciones y solicita una entrada que debe coincidir con alguna de las existentes, caso contrario
    informara el error de entrada y volvera a repetir el proceso.
    """
    valido = False
    while (not valido):
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
            else:
                espacio()
                print("Ha ingresado una opcion inexistente, vuelva a intentarlo\n")
                continuar: str = input("Presione ENTER para continuar")
        else:
            espacio()
            print("Entrada invalida, vuelva a intentarlo\n")
            continuar: str = input("Presione ENTER para continuar")
    return int(pregunta)