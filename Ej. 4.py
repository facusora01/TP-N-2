from os import makedirs
import sys
import csv
#codigo de botellas es 1334, y los vasos 568
#botella pesan 450g = 0.45kg y cuestan 15 dolares. Vasos pesan 350g = 0.35kg y cuestan 8 dolares
def direccion_de_pedidos(lista_de_ciudades, contador):
    print(lista_de_ciudades)
    pass


def verificar_pedidos(numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento, ordenar, vasos, botellas, ciudad_destino)-> list:
    utilitario_01: int = 600
    utilitario_02: int = 1000
    utilitario_03: int = 500
    utilitario_04: int = 2000
    peso_botellas: int = 0.45
    peso_vasos   : int = 0.35

    ciudad_destino.append(ciudad)



    if cod_articulo == '1334':
        botellas+= int(cantidad)
    elif cod_articulo == '568':
        vasos+= int(cantidad)
    
    return vasos, botellas, ciudad_destino

def main() -> None:
    contador_ciudades: list = []
    ciudad_destino: list = []
    vasos: int = 0
    botellas: int = 0
    total: list = [0, 0]
    

    reader: csv = csv.reader(open(r"C:\\Users\\FacuS\Desktop\\TRABAJOS PRACTICOS\\Trabajo Nº2\\pedidos.csv"), delimiter=",")
    ordenar: list = sorted(reader, reverse = True)
    for numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento in ordenar:
        if [] in ordenar: 
            ordenar.remove([])
    print("")
    for numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento in ordenar:

        print(numero_pedido, "\t", fecha,"\t", cliente, "\t",cod_articulo,"\t", color,"\t", cantidad)

        if not cantidad == ' Cantidad':
            desicion: str = input("\n\nDesea modificar la cantidad del pedido?(y/n): ")

            if desicion == 'y':
                cantidad: int = int(input("Escriba la nueva cantidad: "))
                print("")
                
                verificacion: list = verificar_pedidos(numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento, ordenar, vasos, botellas, ciudad_destino)
                total[0] += verificacion[0]
                total[1] += verificacion[1]
                print("-"*100)
            
            else:
                
                verificacion: list = verificar_pedidos(numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento, ordenar, vasos, botellas, ciudad_destino)
                total[0] += verificacion[0]
                total[1] += verificacion[1]
                print("-"*100)
    
    direccion_pedidos: list = direccion_de_pedidos(verificacion[2], contador_ciudades)
        
    for numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento in ordenar:

        print(numero_pedido, "\t", fecha,"\t", cliente,"\t", ciudad, "\t",cod_articulo,"\t", color,"\t", cantidad)
    
    print("\nfueron", len(ordenar)-1, "Pedidos")

    print(f"fueron", total[0], "vasos, y", total[1], "botellas")

    print(verificacion[2])
    
    
main()

