import sys
import csv
def main():
    reader = csv.reader(open(r"C:\Users\FacuS\Desktop\TRABAJOS PRACTICOS\Trabajo Nº2\pedidos.csv"), delimiter=",")
    ordenar = sorted(reader, reverse = True)
    for numero_pedido, fecha, cliente, ciudad, provicnia, cod_articulo, color, cantidad, descuento in ordenar:
        if [] in ordenar: 
            ordenar.remove([])
        print(fecha)
    print("fueron", len(ordenar)-1, "Pedidos")
main()       