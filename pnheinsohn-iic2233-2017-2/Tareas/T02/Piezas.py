from EDD import ListaLigada


class TipoPieza:

    def __init__(self, type, cantidad):
        self.id = id
        self.type = type
        self.cantidad = cantidad
        self.next_node = None

    def __repr__(self):
        return "Tipo: {} | Cantidad Restante: {}".format(self.type, self.cantidad)


class Pieza:

    def __init__(self, type, i, j, num_arriba, color):
        self.type = type
        self.i = int(i)
        self.j = int(j)
        self.num_arriba = num_arriba
        self.color = color
        self.vecinos_disponibles = self.get_possible_neighbors()
        self.vecinos_actuales = ListaLigada()
        self.next_node = None

    def get_possible_neighbors(self):
        type = self.type
        for i in range(self.num_arriba):
            if i != 0:
                type = type[-1] + type[:-1]
        type = type[-1] + type[:2] + type[4:1:-1]
        return type

    def __repr__(self):
        return "Piece: {} | ij: {},{}".format(self.type, self.i, self.j)