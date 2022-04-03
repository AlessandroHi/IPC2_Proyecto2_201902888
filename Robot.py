from Lista import Lista
class Robot(Lista):
    def __init__(self,nombre, tipo, capacidad):
        self.nombre = nombre
        self.tipo = tipo
        self.capacidad = capacidad
        super().__init__()