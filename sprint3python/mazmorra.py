from heroe import Heroe
from monstruo import Monstruo
from tesoro import Tesoro

class Mazmorra:
    def __init__(self, heroe, monstruos):
        self.heroe = heroe
        self.monstruos = monstruos
        self.tesoro = Tesoro()

    def jugar(self):
        print(f"{self.heroe.nombre} entra en la mazmorra...")
        for monstruo in self.monstruos:
            print(f"¡Te has encontrado con {monstruo.nombre}!")
            self.enfrentar_enemigo(monstruo)
            if not self.heroe.esta_vivo():
                print(f"{self.heroe.nombre} ha sido derrotado. Fin del juego.")
                return
            self.buscar_tesoro()
        print(f"¡{self.heroe.nombre} ha derrotado a todos los monstruos y conquistado la mazmorra!")

    def enfrentar_enemigo(self, monstruo):
        while monstruo.esta_vivo() and self.heroe.esta_vivo():
            print("\n¿Qué deseas hacer?")
            print("1. Atacar")
            print("2. Defender")
            print("3. Curarte")
            opcion = input("Elige una opción: ")
            if opcion == "1":
                self.heroe.atacar(monstruo)
            elif opcion == "2":
                self.heroe.defenderse()
            elif opcion == "3":
                self.heroe.curarse()
            else:
                print("Opción no válida.")
            if monstruo.esta_vivo():
                monstruo.atacar(self.heroe)
            self.heroe.reset_defensa()

    def buscar_tesoro(self):
        print("Buscando tesoro...")
        self.tesoro.encontrar_tesoro(self.heroe)
    