import os

def cantidad_botellas(dicc_botellas: dict):
    valores: dict = dicc_botellas.get("Botellas")
    with open("botellas.txt", "w") as botellas:
        for valor in valores:
            botellas.write(f"{valor} {valores[valor]}")
            botellas.write("\n")

def cantidad_vasos(dicc_vasos: dict):
    valores: dict = dicc_vasos.get("Vasos")
    with open("vasos.txt", "w") as vasos:
        for valor in valores:
            vasos.write(f"{valor} {valores[valor]}")
            vasos.write("\n")

# esto es asumiendo esta estructura (se puede adaptar): 
# cantidad_botellas({'Vasos': {'Negro': 2, 'Azul': 0}, 'Botellas': {'Amarillo': 2, 'Rojo': 0, 'Azul': 1, 'Negro': 0, 'Verde': 0}})
