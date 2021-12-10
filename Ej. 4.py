from os import makedirs
import sys
import csv
#codigo de botellas es 1334, y los vasos 568
#botella pesan 450g = 0.45kg y cuestan 15 dolares. Vasos pesan 350g = 0.35kg y cuestan 8 dolares

def decisicion_modificacion(total, lectura_csv, vasos, botellas, ciudad_destino):
    for numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento in lectura_csv:
        if [] in lectura_csv: 
            lectura_csv.remove([])
    print("")
    for numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento in lectura_csv:

        print(numero_pedido, "\t", fecha,"\t", cliente, "\t",cod_articulo,"\t", color,"\t", cantidad)

        if not cantidad == ' Cantidad':
            desicion: str = input("\n\nDesea modificar la cantidad del pedido?(y/n): ")

            if desicion == 'y':
                cantidad: int = int(input("Escriba la nueva cantidad: "))
                print("")
                
                verificacion: list = verificar_pedidos(numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento, lectura_csv, vasos, botellas, ciudad_destino)
                total[0] += verificacion[0]
                total[1] += verificacion[1]
                print("-"*100)
            
            else:
                
                verificacion: list = verificar_pedidos(numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento, lectura_csv, vasos, botellas, ciudad_destino)
                total[0] += verificacion[0]
                total[1] += verificacion[1]
                print("-"*100)
    return verificacion

def leer_csv():
    reader: csv = csv.reader(open(r"C:\\Users\\FacuS\Desktop\\TRABAJOS PRACTICOS\\Trabajo Nº2\\pedidos.csv"), delimiter=",")
    ordenar: list = sorted(reader, reverse = True)
    return reader, ordenar

def imprimir_pedidos(direccion_pedidos)-> None:

    for i in range(len(direccion_pedidos)):
        
        print(f"Se dirigen", direccion_pedidos[i][1],"a", direccion_pedidos[i][0])

def direccion_de_pedidos(lista_de_ciudades)-> list:

    lista = []

    for i in lista_de_ciudades:
        if i not in lista:
            lista.append(i)

    for i in range(len(lista)):
        lista[i] = [lista[i], 0]

    for i in range(len(lista)):
        for e in lista_de_ciudades:
            if e == lista[i][0]:
                lista[i][1] += 1

    return lista

def verificar_pedidos(numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento, ordenar, vasos, botellas, ciudad_destino)-> list:

    ciudad_destino.append(ciudad)

    if cod_articulo == '1334':
        botellas+= int(cantidad)
    elif cod_articulo == '568':
        vasos+= int(cantidad)
    
    return vasos, botellas, ciudad_destino

def main() -> None:
    utilitario_01: int = 600
    utilitario_02: int = 1000
    utilitario_03: int = 500
    utilitario_04: int = 2000
    peso_botellas: int = 0.45
    peso_vasos   : int = 0.35
    
    ciudad_destino: list = []
    vasos: int = 0
    botellas: int = 0
    total: list = [0, 0]
    
    lectura_csv = leer_csv()
    modificacion = decisicion_modificacion(total, lectura_csv[1], vasos, botellas, ciudad_destino)

    
    direccion_pedidos: list = direccion_de_pedidos(modificacion[2])
        
    for numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento in lectura_csv[1]:

        print(numero_pedido, "\t", fecha,"\t", cliente,"\t", ciudad, "\t",cod_articulo,"\t", color,"\t", cantidad)
    
    print("\nfueron", len(lectura_csv[1])-1, "Pedidos")

    print(f"fueron", total[0], "vasos, y", total[1], "botellas")

    imprimir_pedidos(direccion_pedidos)
    
    
main()

