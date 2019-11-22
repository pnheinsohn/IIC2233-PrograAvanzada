from collections import namedtuple
from functools import reduce
import random


class Persona:

    def __init__(self, nombre, apellido, edad, sexo, ciudad_residencia, area_trabajo, sueldo):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = int(edad)
        self.sexo = sexo
        self.ciudad_residencia = ciudad_residencia
        self.area_de_trabajo = area_trabajo
        self.sueldo = float(sueldo)

    def __repr__(self):
        return "Nombre: {} {} | Edad: {} | Sexo: {} | City: {} | Job: {} | Sueldo: {}".format(self.nombre,
                                                                                              self.apellido,
                                                                                              self.edad, self.sexo,
                                                                                              self.ciudad_residencia,
                                                                                              self.area_de_trabajo,
                                                                                              self.sueldo)


# 1 Ciudades por pais
def ciudad_por_pais(nombre_pais, paises, ciudades):
    paises_ = filter(lambda pais: pais.name_pais == nombre_pais, paises)
    pais = next(paises_)
    return filter(lambda city: city.sigla_pais == pais.sigla_pais, ciudades)


# 2 Personas por pais
def personas_por_pais(nombre_pais, paises, ciudades, personas):
    city = [ciudad.nombre for ciudad in ciudad_por_pais(nombre_pais, paises, ciudades)]
    return filter(lambda persona: persona.ciudad_residencia in city, personas)


# 3 Personas por ciudad
def personas_por_ciudad(nombre_ciudad, personas):
    cities = filter(lambda city: city.nombre == nombre_ciudad, ciudades)
    city = next(cities)
    return filter(lambda persona: persona.ciudad_residencia == city.nombre, personas)


# 4 Personas con sueldo mayor a x
def personas_con_sueldo_mayor_a(personas, sueldo):
    return filter(lambda persona: persona.sueldo > sueldo, personas)


# 5 Personas ciudad y sexo dado
def personas_por_ciudad_sexo(nombre_ciudad, sexo, personas):
    return filter(lambda persona: persona.sexo == sexo, personas_por_ciudad(nombre_ciudad, personas))


# 6 Personas por pais sexo y profesion
def personas_por_pais_sexo_profesion(nombre_pais, paises, sexo, profesion, ciudades, personas):
    personas_del_sexo = filter(lambda persona: persona.sexo == sexo, personas_por_pais(nombre_pais, paises, ciudades,
                                                                                       personas))
    return filter(lambda persona: persona.area_de_trabajo == profesion, personas_del_sexo)


# 7 Sueldo promedio mundo
def sueldo_promedio(personas):
    return reduce(lambda x, y: x + y, map(lambda persona: persona.sueldo, personas)) / len(personas)


# 8 Sueldo promedio de una ciudad x
def sueldo_ciudad(nombre_ciudad, personas):
    return reduce(
        lambda x, y: x + y, map(
            lambda persona: persona.sueldo, personas_por_ciudad(nombre_ciudad, personas))) / \
           len(list(personas_por_ciudad(nombre_ciudad, personas)))


# 9 Sueldo promedio de un pais x
def sueldo_pais(nombre_pais, paises, ciudades, personas):
    return reduce(
        lambda x, y: x + y, map(
            lambda persona: persona.sueldo, personas_por_pais(nombre_pais, paises, ciudades, personas))) / \
           len(list(personas_por_pais(nombre_pais, paises, ciudades, personas)))


# 10 Sueldo promedio de un pais y profesion x
def sueldo_pais_profesion(nombre_pais, paises, profesion, ciudades, personas):
    return reduce(
        lambda x, y: x + y, map(
            lambda persona: persona.sueldo, filter(
                lambda persona: persona.area_de_trabajo == profesion, personas_por_pais(
                    nombre_pais, paises, ciudades, personas)))) /\
           len(list(filter(
               lambda persona: persona.area_de_trabajo == profesion, personas_por_pais(nombre_pais, paises, ciudades,
                                                                                       personas))))


if __name__ == '__main__':

    """Abra los archivos y guarde en listas las instancias; paises, ciudades,
    personas"""

    abrir = lambda x: x.rstrip("\n").split(",")
    Ciudad = namedtuple("Ciudad", ["sigla_pais", "nombre"])
    Pais = namedtuple("Pais", ["sigla_pais", "name_pais"])

    with open('Ciudades.txt', 'r', encoding="utf-8") as file1:
        ciudades = [Ciudad(*abrir(line)) for line in file1]

    with open('Informacion_personas.txt', 'r', encoding="utf-8") as file2:
        personas = [Persona(*abrir(line)) for line in file2]

    with open('Paises.txt', 'r', encoding="utf-8") as file3:
        paises = [Pais(*abrir(line)) for line in file3]

    """NO DEBE MODIFICAR CODIGO DESDE EL PUNTO (1) AL (10).
    EN (11) y (12) DEBEN ESCRIBIR SUS RESPUESTAS RESPECTIVAS."""

    # (1) Ciudades en Chile
    print("1")
    ciudades_chile = ciudad_por_pais('Chile', paises, ciudades)
    count = 0
    for ciudad in ciudades_chile:
        print(ciudad.sigla_pais, ciudad.nombre)
        count += 1
        if count == 10:
            break

    # (2) Personas en Chile
    print("2")
    personas_chile = personas_por_pais('Chile', paises, ciudades, personas)
    count = 0
    for p in personas_chile:
        print(p.nombre, p.ciudad_residencia)
        count += 1
        if count == 10:
            break

    # (3) Personas en Osorno, Chile
    print("3")
    personas_stgo = personas_por_ciudad('Osorno', personas)
    for p in personas_stgo:
        print(p.nombre, p.ciudad_residencia)

    # (4) Personas en el mundo con sueldo mayor a 600
    print("4")
    p_sueldo_mayor_600 = personas_con_sueldo_mayor_a(personas, 600)
    count = 0
    for p in p_sueldo_mayor_600:
        print(p.nombre, p.sueldo)
        count += 1
        if count == 10:
            break

    # (5) Personas en ViñaDelMar, Chile de sexo femenino
    print("5")
    pxcs = personas_por_ciudad_sexo('ViñaDelMar', 'Femenino', personas)
    for p in pxcs:
        print(p.nombre, p.ciudad_residencia, p.sexo)

    # (6) Personas en Chile de sexo masculino y area Medica
    print("6")
    pxpsp = personas_por_pais_sexo_profesion('Chile', paises, 'Masculino',
                                             'Medica', ciudades, personas)
    for p in pxpsp:
        print(p.nombre, p.sexo, p.area_de_trabajo)

    # (7) Sueldo promedio de personas del mundo
    print("7")
    sueldo_mundo = sueldo_promedio(personas)
    print('Sueldo promedio: ', sueldo_mundo)

    # (8) Sueldo promedio Osorno, Chile
    print("8")
    sueldo_santiago = sueldo_ciudad('Osorno', personas)
    print('Sueldo Osorno: ', sueldo_santiago)

    # (9) Sueldo promedio Chile
    print("9")
    sueldo_chile = sueldo_pais('Chile', paises, ciudades, personas)
    print('Sueldo Chile: ', sueldo_chile)

    # (10) Sueldo promedio Chile de un estudiante
    print("10")
    sueldo_chile_estudiantes = \
        sueldo_pais_profesion('Chile', paises, 'Estudiante', ciudades,
                              personas)
    print('Sueldo estudiantes Chile: ', sueldo_chile_estudiantes)

    # (11) Muestre a los 10 Chilenos con mejor sueldo con un indice de orden
    # desde 0.

    pais = next(filter(lambda pais: pais.name_pais == "Chile", paises))
    ciudades = filter(lambda ciudad: ciudad.sigla_pais == pais.sigla_pais, ciudades)
    nombre_ciudades = [ciudad.nombre for ciudad in ciudades]
    chilenos_por_sueldo = sorted(filter(lambda persona: persona.ciudad_residencia in nombre_ciudades, personas),
                                 key=lambda x: float(x.sueldo))
    chilenos_por_sueldo.reverse()
    print(chilenos_por_sueldo[:10])

    # (12) Se pide seleccionar 10 personas al azar y generar tuplas con sus:
    # nombres, apellidos y sueldos.

    numeros_azar = [random.randint(0, len(personas)) for i in range(10)]
    personas_azar = [personas[i] for i in numeros_azar]
    tuple_list = [(persona.nombre, persona.apellido, persona.sueldo) for persona in personas_azar]
    for i, tupla in enumerate(tuple_list):
        print("\n{}) {}".format(i + 1, tupla))