class Heroe:
    def __init__(self, nombre):
        self.nombre = nombre
        self.ataque = 10
        self.defensa = 5
        self.salud = 100
        self.salud_max = 100
        self.defensa_aumentada = False
    
    def atacar(self, enemigo):
        daño = max(0, self.ataque - enemigo.defensa)
        enemigo.salud -= daño
        if daño > 0:
            print(f"{self.nombre} ataca a {enemigo.nombre} y causa {daño} de daño.")
        else:
            print(f"{enemigo.nombre} bloqueó el ataque de {self.nombre}.")

    
    def curarse(self):
        curacion = min(20, self.salud_max - self.salud)
        self.salud += curacion
        print(f"{self.nombre} se ha curado. Salud actual: {self.salud}")

    def defenderse(self):
        self.defensa += 5
        self.defensa_aumentada = True
        print(f"{self.nombre} se defiende. Defensa aumentada a {self.defensa}.")

    def reset_defensa(self):
        if self.defensa_aumentada:
            self.defensa -= 5
            self.defensa_aumentada = False
            print(f"La defensa de {self.nombre} vuelve a su valor normal ({self.defensa}).")
    
    def esta_vivo(self):
        return self.salud > 0