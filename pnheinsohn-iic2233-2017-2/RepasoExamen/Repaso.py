import unittest
import os


'''
#########################
## PARTE 1: Pa' Pollos ##
#########################
___________________
Pregunta 1: Testing

Para generar un ambiente de testing que emplee variables que se re-inicializan y sean eliminadas al final de este, es
necesario crear una clase Testing que herede de unittest.TestCase que contenga el metodo setUp y tearDown, junto a los
metodos necesarios para hacer el testing los que necesariamente deben partir su nombre con "test_" (dado PEP8, y
libreria unittest). El metodo setUp se llamara cada antes de ejecutar cada metodo que tenga el nombre "test_" para que
asi uno pueda settear las variables necesarias a ser usadas, mientras que el metodo tearDown borra todas esas variables
mutables para que no ocurran conflictos en los futuros tests. La principal razon de usar estos dos metodos, es para
crear archivos en el setUp, poder trabajar con ellos mediante los tests y finalmente usar el metodo tearDown para borrar
el archivo creado.

ejemplo:
'''


class Testing(unittest.TestCase):

    def setUp(self):
        self.archivo = open("archivo.txt", "w", encoding="utf-8")
        self.lista = ["c", "a", "m", "i", "s", "a"]

    def test_suma_string(self):
        string = ""
        for s in self.lista:
            string += s
        self.assertEqual("camisa", string)

    def tearDown(self):
        self.archivo.close()
        if os.path.isfile("archivo.txt"):
            os.remove("archivo.txt")

suite = unittest.TestLoader().loadTestsFromTestCase(Testing)
unittest.TextTestRunner().run(suite)


'''
________________________
Pregunta 2: Strings, GUI

parte b:
self.backend = BackEnd()
self.line_edit1 = LineEdit("", self)
self.boton = QPushButton("Send", self)
self.boton.clicked.connect(corroborar_correo)

def corroborar_correo(self):
    if self.backend.verificar_correo(self.line_edit1.text()):
        self.setCentralWidget(otro_widget)
    else:
        QMessageBox().warning(self, "Email Error", "Correo ingresado es invalido", QMessageBox.Ok, QMessageBox.NoButton)

parte a:
'''


def verificar_correo(correo):
    arroba = correo.find("@")
    arroba2 = correo.rfind("@")
    if len(correo) == 0:
        return False
    elif correo[-3:len(correo)] != ".cl":
        return False
    elif arroba == -1 or arroba != arroba2:
        return False
    elif not (correo[:arroba].isalnum() or correo[arroba + 1:].replace(".", "").isalnum()):
        return False
    return True


'''
_____________________________
Pregunta 3: Clases Abstractas

Una clase abstracta es una clase cuyo fin es nunca ser instanciada, pero si heredada, debido a que representan clases
generalizadas que comparten ciertos atributos y/o metodos. Por ejemplo, una Persona tiene nombre completo, edad, 
domicilio, entre otros atributos, mientras que puede caminar, correr, comer, entre otros metodos. Sin embargo, carece de
sentido instanciar al objeto persona si quiero realizar una simulacion del funcionamiento de una empresa, ya que hay 
tanto funcionarios de planta, gerentes, jefes, y otras entidades distintas que no actuan de la misma forma, pero si 
comparten lo mencionado anteriormente. Luego, resulta muy util desde un punto de vista de modelamiento crear una clase
abstracta llamada Persona de la cual todas las entidades humanas de la simulacion puedan heredar de ella, asi se evita
escribir codigo repetido para cada entidad, creando un codigo mas limpio y claro. Ademas, este modelamiento permite el 
uso de metodos abstractos, los que deben ser sobreescribidos por cada clase, asi facilitando al programador a acordarse
y mantener mayor orden a la hora de escribir, sin pasar por alto elementos importantes, como comer jajaja.
_______________
Pregunta 4: OOP

Herencia es la capacidad que tienen unas subclases de heredar/obtener todos aquellos atributos y metodos que una clase 
tiene, con el fin de tener un codigo mas limpio, legible, y mejor modelado, por ejemplo, un Vehiculo, este tiene las
acciones de avanzar, virar, frenar, etc. por lo que varias subclases como Avion, Auto, Bote, etc. pueden adquirir lo de
Vehiculo para asi comportarse como tal. Sin embargo, composicion corresponde a la accion de componer, es decir, aquello
es aquello necesario para que una clase pueda ser como tal, por ejemplo, en el caso anterior, ruedas.
_________________
Pregunta 5: Bytes

i)   bytearray(b'Hola')
ii)  72
iii) bytearray(b'hola')
iv)  b'Hola'
v)   72
vi)  No alcanza a imprimirse, pero deberia ser b'Hola'
_____________________
Pregunta 6: Funcional

i) [[25], [16], [36, 100], [49]]
______________________
Pregunta 7: Metaclases

i)   representa a la clase Examen
ii)  Es un metodo estatico de las instancias de la clase examen
iii) {"E1": 0, "E2": 1, "E3": 2}
iv)  [0, 1, 2]

##################
## Pa' Mortales ##
##################
_________________________
Pregunta 1: Serializacion

parte a:
# asd

parte b:
# asd
_________________
Pregunta 2: Regex
'''

# asd

'''
_____________________
Pregunta 3: Funcional

i) # Hardcoreana

_____________________
Pregunta 4: Funcional
'''


def rec(functon, lista):
    for i in range(len(lista)):
        if isinstance(lista[i], list):
            rec(functon, lista[i])
        else:
            lista[i] = functon(lista[i])
    return lista
print(rec(lambda x: x * x, [1, 2, [3, 4, [3, 5]]]))


'''
Ayudantia Extra:
Grafos:
'''


class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
        self.amigos = []

    def add_connection(self, persona):
        self.amigos.append(persona)

    def recorrer(self):
        from collections import deque
        personas_alcanzables = deque()
        visitados = []
        for amigo in self.amigos:
            personas_alcanzables.append(amigo)
            visitados.append(amigo)
        while len(personas_alcanzables) > 0:
            current = personas_alcanzables.pop()
            for amigo in current.amigos:
                if amigo not in visitados:
                    visitados.append(amigo)
                    personas_alcanzables.append(amigo)
        return visitados

    def __repr__(self):
        return self.nombre + " -> (" + \
               ",".join([c.nombre for c in self.amigos]) + ")"


# El mundo
nodes = {}
personas = ["Jorge", "Enzo", "Flo", "Diego", "Alejandro",
            "Octavio", "Cata", "Rosario", "Sofia", "Isi",
            "Carlos", "Cristiano Ronaldo", "Leonardo Dicaprio",
            "Angelina Jolie", "Donald Trump", "Kim Jong Un",
            "Margot Robbie", "Roger Federer"]

for p in personas:
    n = Persona(p)
    nodes[p] = n

nodes["Jorge"].add_connection(nodes["Enzo"])
nodes["Jorge"].add_connection(nodes["Diego"])
nodes["Jorge"].add_connection(nodes["Cata"])
nodes["Diego"].add_connection(nodes["Flo"])
nodes["Diego"].add_connection(nodes["Rosario"])
nodes["Diego"].add_connection(nodes["Jorge"])
nodes["Diego"].add_connection(nodes["Cata"])
nodes["Cata"].add_connection(nodes["Isi"])
nodes["Cata"].add_connection(nodes["Sofia"])
nodes["Cata"].add_connection(nodes["Rosario"])
nodes["Enzo"].add_connection(nodes["Jorge"])
nodes["Enzo"].add_connection(nodes["Sofia"])
nodes["Isi"].add_connection(nodes["Carlos"])
nodes["Carlos"].add_connection(nodes["Octavio"])
nodes["Carlos"].add_connection(nodes["Cristiano Ronaldo"])
nodes["Octavio"].add_connection(nodes["Donald Trump"])
nodes["Octavio"].add_connection(nodes["Carlos"])
nodes["Cristiano Ronaldo"].add_connection(nodes["Margot Robbie"])
nodes["Donald Trump"].add_connection(nodes["Kim Jong Un"])

print(nodes["Jorge"].recorrer())

import re

asd = "".join(["<{0}>{1}</{0}>".format("u", a) for a in "Este mensaje incluye 4 espacios".split()])
print(asd)
print(re.split('(<[^>]+>)', asd))
print(re.match("abc", "abcsgsffdasd"))
