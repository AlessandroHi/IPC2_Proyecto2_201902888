from Nodo import Nodo

class Lista(Nodo):
    def __init__(self):
        super().__init__()
        self.cabeza = Nodo()
        self.contador = 0
        self.valor = self.__str__()
        
    def append(self, nuevo_nodo):
        nodo = self.cabeza
        while(nodo.siguiente):
            nodo = nodo.siguiente
        nodo.siguiente = nuevo_nodo
        self.contador += 1
        self.valor = self.__str__()
        
    def get(self, i):
        if (i >= self.contador):
            return None
        nodo = self.cabeza.siguiente
        n = 0
        while(nodo):
            if (n == i):
                return nodo
            nodo = nodo.siguiente
            n += 1

        return    
    def __getitem__(self, i):
        return self.get(i)

    def length(self):
        return self.contador

    def primero(self):
        return self.get(0)

    def ultimo(self):
        return self.get(self.length() - 1)

   