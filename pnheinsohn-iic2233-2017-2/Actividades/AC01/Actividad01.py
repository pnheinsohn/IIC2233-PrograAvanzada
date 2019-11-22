class Ciudad:

    lista_de_comunas = []

    def __init__(self, nombre_ciudad):
        self.nombre_ciudad = nombre_ciudad
        self.nombre_comuna = ""
        self.continuar = ""
        self.comuna = ""

    def agregar_comuna(self):
        while True:
            self.nombre_comuna = input("Inserte nombre de la comuna: ")
            self.comuna = Comuna(self.nombre_comuna)
            self.lista_de_comunas.append(self.comuna)
            Ciudad.lista_de_comunas = self.lista_de_comunas
            self.continuar = input("¿Desea agregar una nueva comuna? (si/no): ")
            if self.continuar.lower() == "no":
                return self.comuna
            elif self.continuar.lower() != "si":
                print("No es una opción válida, ingrese una nuevamente...")

    def get_lista_de_comunas(self):
        for i in range(len(Ciudad(self.nombre_ciudad).lista_de_comunas)):
            print(Ciudad(self.nombre_ciudad).lista_de_comunas[i].nombre_ciudad)
        return


class Comuna:

    lista_de_casas = []
    lista_de_edificios = []

    def __init__(self, nombre):
        self.nombre = nombre
        self.vivienda = ""

    def agregar_vivienda(self, casa_o_edificio):
        while True:
            if casa_o_edificio.lower() == "casa":
                self.vivienda = Comuna(self.nombre)._agregar_casa()
                self.lista_de_casas.append(self.vivienda)
                Comuna(self.nombre).lista_de_casas = self.lista_de_casas
            elif casa_o_edificio.lower() == "edificio":
                self.vivienda = Comuna(self.nombre)._agregar_edificio()
                self.lista_de_edificios.append(self.vivienda)
                Comuna(self.nombre).lista_de_edificios = self.lista_de_edificios
            else:
                print("No es una opción válida, ingrese una nuevamente...")

            pregunta1 = input("¿Desea agregar una vivienda nueva? (si/no): ")
            if pregunta1 == "no":
                break
            elif pregunta1 != "si":
                print("respuesta inválida")
            else:
                casa_o_edificio = input("¿Desea agregar una casa o un edificio? (casa/edificio): ")
        return self.vivienda

    def _agregar_casa(self):
        direccion = input("Ingrese dirección: ")
        pregunta = input("¿Es electrodependiente? (si/no): ")
        electrodependencia = False
        while True:
            if pregunta.lower() == "si":
                electrodependencia = True
                break
            elif pregunta.lower() != "no":
                print("No es una opción válida, ingrese una nuevamente...")
            else:
                break
        nueva_casa = Casa().agregar_casa(direccion, electrodependencia)
        return nueva_casa

    def _agregar_edificio(self):
        nombre_edificio = input("Nombre del edificio para agregar el departamento: ")
        direccion = input("ingrese dirección: ")
        edificio = Edificio(nombre_edificio, direccion)
        return edificio


class Casa:

    def __init__(self):
        # self.medidor = medidor o Medidor()
        self.direccion = ""
        self.cliente = ""
        self.persona_electrodependiente = False

    def agregar_casa(self, direccion, electrodependencia):
        self.direccion = direccion
        if electrodependencia:
            self.persona_electrodependiente = True
        self.cliente = Cliente()
        return self


class Edificio:

    lista_de_departamentos = []

    def __init__(self, nombre, direccion):
        # self.medidor = medidor o Medidor()
        self.nombre = nombre
        self.direccion = direccion
        self.departamentos = ""

    def agregar_departamentos(self):
        pregunta = input("¿Es electrodependiente? (si/no): ")
        electrodependientes = False
        while True:
            if pregunta.lower() == "si":
                electrodependientes = True
                break
            elif pregunta.lower() != "no":
                print("No es una opción válida, ingrese una nuevamente...")
            else:
                break
        self.departamentos = Departamento(electrodependientes)
        self.lista_de_departamentos.append(self.departamentos)
        Edificio(self.nombre, self.direccion).lista_de_departamentos = self.lista_de_departamentos
        return self.lista_de_departamentos
        

class Departamento:

    numero_departamento = 1

    def __init__(self, electrodependientes):
        # self.medidor = medidor o Medidor()
        self.personas_electrodependientes = electrodependientes
        self.numero = self.numero_departamento
        self.cliente = ""

    def agregar_cliente(self):
        self.cliente = Cliente()
        Departamento(self.personas_electrodependientes).numero_departamento += 1
        return self.cliente


class Cliente:

    def __init__(self):
        self.nombre = input("nombre del huesped: ")
        self.rut = input("rut: ")


santiago = Ciudad("Santiago")
print("agregando comunas")
florida = santiago.agregar_comuna()
print("agregar vivienda")
casa = florida.agregar_vivienda("casa")
edificio = florida.agregar_vivienda("edificio")
departamentos = edificio.agregar_departamentos()

for i in range(len(departamentos)):
    departamento = departamentos[i]
    print("departamento N°" + str(i))
for i in range(len(florida.lista_de_casas)):
    print("casas: ", florida.lista_de_casas[i].direccion)
for i in range(len(florida.lista_de_edificios)):
    print("edificios: ", florida.lista_de_edificios[i].direccion)
