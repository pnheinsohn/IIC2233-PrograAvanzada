class Node:

    def __init__(self, letter):
        self.childs = {}
        self.value = 0
        self.letter = letter

    def add_child(self, string, number):
        if len(string) > 1:
            if string[0] not in self.childs:
                self.childs[string[0]] = Node(string[0])
            self.childs[string[0]].add_child(string[1:], number)
        elif len(string) == 1:
            if string[0] not in self.childs:
                self.childs[string[0]] = Node(string[0])
                self.childs[string[0]].value = number
                print("Contacto agregado con exito")
            else:
                print("Contacto ya Existe")

    def contact_change_number(self, string, number):
        if len(string) > 1 and string[0] in self.childs:
            self.childs[string[0]].contact_change_number(string[1:], number)
        elif len(string) == 1 and string[0] in self.childs:
            self.childs[string[0]].value = number
            print("Cambio realizado con exito")
        else:
            print("Contacto Inexistente")

    def contact_ask_number(self, name, string):
        if len(string) > 1 and string[0] in self.childs:
            self.childs[string[0]].contact_ask_number(name, string[1:])
        elif len(string) == 1 and string[0] in self.childs:
            print("({}, {})".format(name, self.childs[string[0]].value))
        else:
            print("Contacto Inexistente")

    def __repr__(self):
        ret = "Valor: {} -> hijos: {}".format(self.value, self.childs) + "\n"
        return ret


class ContacTrie:

    def __init__(self):
        self.childs = {}
        self.value = ""

    def __add_suffix(self, string, number):
        if string[0] not in self.childs:
            self.childs[string[0]] = Node(string[0])
        self.childs[string[0]].add_child(string[1:], number)

    def add_contact(self, string, number):
        if self.check_inputs(string, number):
            string = string.upper()
            self.__add_suffix(string, number)

    def change_contact_number(self, string, number):
        if self.check_inputs(string, number):
            string = string.upper()
            if string[0] in self.childs:
                self.childs[string[0]].contact_change_number(string[1:], number)
            else:
                print("Contacto Inexistente")

    def ask_for_contact(self, string):
        if string.isalpha():
            string = string.upper()
            if string[0] in self.childs:
                self.childs[string[0]].contact_ask_number(string, string[1:])
            else:
                print("Contacto Inexistente")

    def get_all_contacts(self):
        def recorrer_arbol(raiz, letter=""):
            self.name += letter
            if raiz.value != 0 and self.name != "":
                print("({}, {})".format(self.name, raiz.value))
                self.name = ""
            for hijo in raiz.childs.values():
                recorrer_arbol(hijo, hijo.letter)
            return

        self.name = ""
        recorrer_arbol(self)

    def merge_tries(self, tree):
        if not isinstance(tree, ContacTrie):
            print("Debe ser un ContacTrie")
            return
        else:
            pass

    def __add__(self, other):
        if not isinstance(other, ContacTrie):
            print("Operacion No Soportada")
            return
        else:
            pass

    def check_inputs(self, string, number=0):
        if string == "" and not string.isalpha():
            print("Nombre Invalido")
            return False
        if not isinstance(number, int) or not number > 0:
            print("Numero Invalido")
            return False
        return True

    def __repr__(self):
        return self.childs.__repr__()

tree = ContacTrie()
tree1 = ContacTrie()
tree.add_contact("C-137", 1000)
tree.add_contact("WhereAreMyTesticlesSummer", 525)
tree.add_contact("PickleRick", 10)
tree.change_contact_number("PickleRick", 6969)
tree.ask_for_contact("WhereAreMyTesticlesSummer")
tree.get_all_contacts()
print("________________________________")
tree1.add_contact("HammerHead Morty", 69)
tree1.add_contact("Morty", 13)
tree1.add_contact("RickmancingTheStone", 10)
tree1.change_contact_number("Morty", 1)
tree1.ask_for_contact("Morty")
tree1.get_all_contacts()
