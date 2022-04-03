from Lista import Lista
class Casilla(Lista):
    def __init__(self,caracteristica, valor):
        self.caracteristica = caracteristica
        self.valor = valor
        super().__init__()