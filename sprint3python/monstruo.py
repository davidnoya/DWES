class Monstruo:
    def __init__(self, nombre, ataque, defensa, salud):
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.salud = salud

    def atacar(self, heroe):
        daño = max(0, self.ataque - heroe.defensa)
        heroe.salud -= daño
        if daño > 0:
            print(f"{self.nombre} ataca a {heroe.nombre} y causa {daño} puntos de daño.")
        else:
            print(f"{heroe.nombre} bloqueó el ataque de {self.nombre}.")

    def esta_vivo(self):
        return self.salud > 0