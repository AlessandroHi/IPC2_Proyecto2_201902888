from Lista import Lista
class UnidadCivil(Lista):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        super().__init__()