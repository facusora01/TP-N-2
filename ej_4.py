import csv
from os import close


def leer_csv()-> tuple:

    #POST: Lee el .csv, y devuelve la informacion que traía dentro
    with open(r"pedidos.csv") as archivo:
        informacion: csv = csv.reader(archivo)
        pedidos_temporal: list = list(informacion)
    
    # lectura: csv = csv.reader(open(r"pedidos.csv"), delimiter=",")
    # ordenar_info: list = sorted(lectura, reverse = True)
    # close
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
                cantidad: int = int(input("Escriba la nueva cantidad: "))
                print("")
                
                contador: list = contador_vasos_botellas(fila[3], fila[5], cantidad, vasos, botellas, ciudad_destino)
                total[0] += contador[0]
                total[1] += contador[1]
                print("-"*100)
            
            else:
                
                contador: list = contador_vasos_botellas(fila[3], fila[5], fila[7], vasos, botellas, ciudad_destino)
                total[0] += contador[0]
                total[1] += contador[1]
                print("-"*100)

    return contador


def imprimir_tablero(lectura_csv)-> None:


    # for fila in lectura_csv:
    #     for item in fila:
    #         print(item, end=" ")

    for fila in lectura_csv:
        if not 'Nro. Pedidio' in fila[0]:

            print('\t'.join(str(x) for x in fila))
        
        else:
            print(' '.join(str(x) for x in fila))
            



    #PRE: Recibe como parametro: Los datos que traía el .csv
    #POST:  se hace un for con varios if dentro, los cuales se encargan simplemente de que la impresión del tablero se vea decente. No devuelve nada

    # for numero_pedido, fecha, cliente, ciudad, provincia, cod_articulo, color, cantidad, descuento in lectura_csv:
  
    #     if numero_pedido != 'Nro. Pedidio':

    #         numero_pedido: str = numero_pedido.center(len(numero_pedido)+5)
        
    #     if fecha != ' Fecha':

    #         fecha: str = fecha.rjust(len(fecha)+6)
        
    #     if cliente != ' Cliente':

    #         cliente: str = cliente.center(len(cliente))
        
    #     if ciudad == ' Ciudad':

    #         ciudad: str = ciudad.rjust(len(ciudad)+1)
        
    #     if ciudad != ' Ciudad':

    #         if len(cliente) < 16:

    #             ciudad: str = ciudad.rjust(len(ciudad)+8)

    #     if provincia == ' Provincia':

    #         provincia: str = provincia.rjust(len(provincia)+1)

    #     if provincia != ' Provincia':

    #         if len(cliente) > 16:

    #             provincia: str = provincia.rjust(len(provincia)+8)
            
    #         elif len(provincia) >= 12:

    #             provincia: str = provincia.rjust(len(provincia)+8)

    #     if cod_articulo != ' Cod. Artículo':

    #         cod_articulo: str = cod_articulo.center(len(cod_articulo)+6)

    #     if color != ' Color':

    #         color: str = color.rjust(len(color)+9)

    #     if cantidad != ' Cantidad':

    #         if color == '         Amarillo' or color == '         Negro':

    #             cantidad: str = cantidad.rjust(len(cantidad)+2)

    #         else:
    #             cantidad: str = cantidad.rjust(len(cantidad)+10)


    #     if descuento != ' Descuento':

    #         descuento: str = descuento.rjust(len(descuento)+10)

    #     print(numero_pedido,'\t', fecha,"\t", cliente,'\t', ciudad,"\t", provincia,"\t",cod_articulo,"\t", color,"\t", cantidad,'\t', descuento)



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

def main() -> None:    

    
    ciudad_destino: list = []
    vasos: int = 0
    botellas: int = 0
    total: list = [0, 0]

    lectura_csv: list = leer_csv()
    modificacion: tuple = decisicion_modificacion(total, lectura_csv, vasos, botellas, ciudad_destino)


    direccion_pedidos: list = direccion_de_pedidos(modificacion[2])


    imprimir_tablero(lectura_csv)

    
    print("\nfueron", len(lectura_csv[1])-1, "Pedidos")

    print(f"fueron", total[0], "vasos, y", total[1], "botellas")

    for i in range(len(direccion_pedidos)):
        
        print(f"Se dirigen", direccion_pedidos[i][1],"a", direccion_pedidos[i][0])

main()
