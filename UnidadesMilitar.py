from Lista import Lista
class UnidadesMilitar(Lista):
    def __init__(self,x,y,valor):
        self.x = x
        self.y = y
        self.valor = valor
        super().__init__()