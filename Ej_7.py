import os
import inteligencia_artificial as ia

def cantidad_botellas(dicc_botellas: dict) -> None:
    valores: dict = dicc_botellas.get("Botellas")
    with open("botellas.txt", "w") as botellas:
        for valor in valores:
            botellas.write(f"{valor} {valores[valor]}")
            botellas.write("\n")
    
def cantidad_vasos(dicc_vasos: dict) -> None:
    valores: dict = dicc_vasos.get("Vasos")
    with open("vasos.txt", "w") as vasos:
        for valor in valores:
            vasos.write(f"{valor} {valores[valor]}")
            vasos.write("\n")

def main() -> None:
    dicc_objetos: dict = ia.main()
    cantidad_botellas(dicc_objetos)
    cantidad_vasos(dicc_objetos)
