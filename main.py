import Ejercicio_1 as ej1
import ej_4 as ej4
import TPAlgoritmos2 as ej5y6
import Ej_7 as ej7
import inteligencia_artificial as ia

def main() -> None: 
    ia.main()
    opciones: dict = {1: "Alta, baja y modificacion de pedidos",
                      2: "Generar recorrido",
                      3: "Procesar pedidos",
                      4: "Pedidos completados",
                      5: "Pedidos de Rosario",
                      6: "Articulo mas solicitado y numero de entregas",
                      7: "Generar archivo con productos procesados",
                      8: "Salir"}
    titulo: str = "Menú de gestión de Chilly Bottles"
    ejecutando: bool = True

    while ejecutando:
        ej1.espacio()
        eleccion: int = ej1.menu_generico(titulo=titulo, opciones=opciones)
        
        if (eleccion == 1):
            ej1.abm_pedidos()
        if (eleccion == 2):
            pass
        if (eleccion == 3):
            pass
        if (eleccion == 4):
            ej1.espacio()
            ej4.main()
        if (eleccion == 5):
            ej1.espacio()
            ej5y6.pedidos_a_ciudad("Rosario")
        if (eleccion == 6):
            ej1.espacio()
            ej5y6.articulo_mas_pedido_y_entregados()
        if (eleccion == 7):
            ej1.espacio()
            ej7.main()
        if (eleccion == 8):
            ej1.espacio()
            print("Gracias! Vuelva pronto\n")
            ejecutando = False

main()