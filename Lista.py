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

    def pop(self, i = None):
        if i is None:
            i = self.contador - 1
        if not (0 <= i < self.contador):
            raise IndexError("Índice fuera de rango")
        if i == 0:
            dato = self.cabeza.valor
            self.cabeza = self.cabeza.siguiente
        else:
            n_ant = self.cabeza
            n_act = n_ant.siguiente
            for pos in range(1, i):
                n_ant = n_act
                n_act = n_ant.siguiente
            dato = n_act.valor
            n_ant.siguiente = n_act.siguiente
        self.contador -= 1
        return dato
    
    def reset(self,i):
        self.pop(i)

    def __getitem__(self, i):
        return self.get(i)

    def length(self):
        return self.contador

    def primero(self):
        return self.get(0)

    def ultimo(self):
        return self.get(self.length() - 1)
