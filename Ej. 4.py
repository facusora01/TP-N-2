from os import makedirs
import sys
import csv
#codigo de botellas es 1334, y los vasos 568
#botella pesan 450g = 0.45kg y cuestan 15 dolares. Vasos pesan 350g = 0.35kg y cuestan 8 dolares

def leer_csv()-> tuple:
    reader: csv = csv.reader(open(r"C:\\Users\\FacuS\Desktop\\TRABAJOS PRACTICOS\\Trabajo Nº2\\pedidos.csv"), delimiter=",")
    ordenar: list = sorted(reader, reverse = True)
    return reader, ordenar

def verificar_pedidos(ciudad, cod_articulo, cantidad, vasos, botellas, ciudad_destino)-> tuple:

    ciudad_destino.append(ciudad)

    if cod_articulo == '1334':
        botellas+= int(cantidad)
    elif cod_articulo == '568':
        vasos+= int(cantidad)

    return vasos, botellas, ciudad_destino, cantidad


def decisicion_modificacion(total, lectura_csv, vasos, botellas, ciudad_destino)-> tuple:
    for numero_pedido, fecha, cliente, ciudad, provincia, cod_articulo, color, cantidad, descuento in lectura_csv:
        if [] in lectura_csv: 
            lectura_csv.remove([])
    print("")
    for numero_pedido, fecha, cliente, ciudad, provincia, cod_articulo, color, cantidad, descuento in lectura_csv:

        print(numero_pedido,"\t", fecha,"\t", cliente,"\t", provincia,"\t",cod_articulo,"\t", color,"\t", cantidad,"\t", descuento)

        if not cantidad == ' Cantidad':
            desicion: str = input("\n\nDesea modificar la cantidad del pedido?(y/n): ")

            if desicion == 'y':
                cantidad: int = int(input("Escriba la nueva cantidad: "))
                print("")
                
                verificacion: list = verificar_pedidos(ciudad, cod_articulo, cantidad, vasos, botellas, ciudad_destino)
                total[0] += verificacion[0]
                total[1] += verificacion[1]
                print("-"*100)
            
            else:
                
                verificacion: list = verificar_pedidos(ciudad, cod_articulo, cantidad, vasos, botellas, ciudad_destino)
                total[0] += verificacion[0]
                total[1] += verificacion[1]
                print("-"*100)
    return verificacion

def imprimir_tablero(lectura_csv):
    for numero_pedido, fecha, cliente, ciudad, provincia, cod_articulo, color, cantidad, descuento in lectura_csv:
  
        if numero_pedido != 'Nro. Pedidio':

            numero_pedido = numero_pedido.center(len(numero_pedido)+5)
        
        if fecha != ' Fecha':

            fecha = fecha.rjust(len(fecha)+6)
        
        if cliente != ' Cliente':

            cliente = cliente.center(len(cliente))
        
        if ciudad == ' Ciudad':

            ciudad = ciudad.rjust(len(ciudad)+1)
        
        if ciudad != ' Ciudad':

            if len(cliente) < 16:

                ciudad = ciudad.rjust(len(ciudad)+8)

        if provincia == ' Provincia':

            provincia = provincia.rjust(len(provincia)+1)

        if provincia != ' Provincia':

            if len(cliente) > 16:

                provincia = provincia.rjust(len(provincia)+8)
            
            if len(provincia) >= 12:

                provincia = provincia.rjust(len(provincia)+8)

        if cod_articulo != ' Cod. ArtÃ­culo':

            cod_articulo = cod_articulo.center(len(cod_articulo)+6)

        if color != ' Color':

            color = color.rjust(len(color)+9)

        if cantidad != ' Cantidad':

            if color == '         Amarillo' or color == '         Negro':

                cantidad = cantidad.rjust(len(cantidad)+2)

            else:
                cantidad = cantidad.rjust(len(cantidad)+10,)


        if descuento != ' Descuento':

            descuento = descuento.rjust(len(descuento)+6)

        print(numero_pedido,'\t', fecha,"\t", cliente,'\t', ciudad,"\t", provincia,"\t",cod_articulo,"\t", color,"\t", cantidad,"\t", descuento)



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

def main() -> None:    
    ciudad_destino: list = []
    vasos: int = 0
    botellas: int = 0
    total: list = [0, 0]
    
    lectura_csv = leer_csv()
    modificacion = decisicion_modificacion(total, lectura_csv[1], vasos, botellas, ciudad_destino)

    
    direccion_pedidos: list = direccion_de_pedidos(modificacion[2])


    imprimir_tablero(lectura_csv[1])

    
    print("\nfueron", len(lectura_csv[1])-1, "Pedidos")

    print(f"fueron", total[0], "vasos, y", total[1], "botellas")

    for i in range(len(direccion_pedidos)):
        
        print(f"Se dirigen", direccion_pedidos[i][1],"a", direccion_pedidos[i][0])
    
main()

