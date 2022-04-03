from Lista import Lista

class Ciudad(Lista):
     def __init__(self,nombre,fila,columna,entradas,unidadCiviles, recursos):
        self.nombre = nombre
        self.fila = fila
        self.columna = columna
        self.entradas = entradas
        self.unidadCiviles = unidadCiviles
        self.recursos = recursos
        super().__init__()


     def obtener_elem(self, x, y):
        if((x >= self.fila) or (y >= self.columna)):
            raise RuntimeError('Límites no definidos en la matriz')
        fila = self.get(x)
        celda = fila.get(y)
        return celda.valor 