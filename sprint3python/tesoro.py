import random

class Tesoro:
    def __init__(self):
        self.beneficios = ["aumento ataque", "aumento defensa", "restaurar salud"]

    def encontrar_tesoro(self, heroe):
        beneficio = random.choice(self.beneficios)
        if beneficio == "aumento ataque":
            heroe.ataque += 5
            print(f"{heroe.nombre} ha encontrado un tesoro: aumento de ataque. Ataque actual: {heroe.ataque}")
        elif beneficio == "aumento defensa":
            heroe.defensa += 5
            print(f"{heroe.nombre} ha encontrado un tesoro: aumento de defensa. Defensa actual: {heroe.defensa}")
        elif beneficio == "restaurar salud":
            heroe.salud = heroe.salud_max
            print(f"{heroe.nombre} ha encontrado un tesoro: restauración de salud. Salud actual: {heroe.salud}")