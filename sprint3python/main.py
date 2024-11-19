from heroe import Heroe
from monstruo import Monstruo
from mazmorra import Mazmorra

if __name__ == "__main__":
    heroe = Heroe("David")
    monstruos = [
        Monstruo("Noemí", 8, 3, 30),
        Monstruo("Iria", 15, 5, 50),
        Monstruo("Rubén", 20, 10, 87),
        Monstruo("Carlos", 24, 15, 100)
    ]
    mazmorra = Mazmorra(heroe, monstruos)
    mazmorra.jugar()