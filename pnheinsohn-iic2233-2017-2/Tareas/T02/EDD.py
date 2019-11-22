class Node:

    def __init__(self, valor):
        self.valor = valor
        self.next_node = None

    def __repr__(self):
        return self.valor.__repr__()


class ListaLigada:

    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, objeto):
        if not self.head:
            self.head = objeto
            self.tail = self.head
        else:
            self.tail.next_node = objeto
            self.tail = self.tail.next_node

    def pop(self, index=-1):
        if index >= len(self) or -1 * index > len(self):
            raise IndexError
        elif not isinstance(index, int):
            raise TypeError
        if index < 0:
            index = len(self) + index
        for i in range(len(self)):
            if index == 0:
                head = self.head
                self.head = self.head.next_node
                return head
            elif index - 1 == i:
                tokill = self[i + 1]
                self[i].next_node = tokill.next_node
                return tokill

    def reverse(self):
        prev = None
        self.tail = self.head
        current = self.tail
        while current:
            next_node = current.next_node
            current.next_node = prev
            prev = current
            current = next_node
        self.head = prev

    def __iter__(self):
        return Iterador(self.head)

    def __getitem__(self, index):
        i = 0
        head = self.head
        while i != index:
            head = head.next_node
            i += 1
        if head:
            return head
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if key >= len(self) or -1 * key > len(self):
            raise IndexError
        if key < 0:
            key = len(self) + key
        self[key] = value

    def __delitem__(self, key):
        self.pop(key)

    def __len__(self):
        i = 0
        head = self.head
        while head:
            head = head.next_node
            i += 1
        return i

    def __repr__(self):
        string = "["
        head = self.head
        while head:
            if isinstance(head, Node):
                string += "Pieza: {},\n".format(head.valor.type)
            else:
                string += "Pieza: {},\n".format(head.type)
            head = head.next_node
        string += "]"
        return string.replace(",\n]", "]")


class PilaAndQueue(ListaLigada):

    def pop(self, index=-1):
        if not isinstance(index, int):
            raise TypeError("Solo se acepta el entero -1")
        elif index != -1:
            raise ValueError("Solo se acepta el entero -1")
        tail = self.tail
        self[len(self) - 2].next_node = None
        self.tail = self[len(self) - 2]
        return tail

    def popleft(self):
        head = self.head
        self.head = self.head.next_node
        return head


class Iterador:

    def __init__(self, iterable):
        self.iterable = iterable

    def __next__(self):
        if self.iterable is None:
            raise StopIteration("Llegamos al final")
        else:
            to_return = self.iterable
            self.iterable = self.iterable.next_node
            return to_return
