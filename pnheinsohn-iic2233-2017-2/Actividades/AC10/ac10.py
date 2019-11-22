import threading
import time
from random import randint


class Bicicleta(threading.Thread):

    _id = 0
    lista_llegados = []

    def __init__(self):
        self.bicicleta = "Equipo {}".format(Bicicleta._id)
        self.ciclista = "Ciclista {}".format(Bicicleta._id)
        self.genio = Genio(Bicicleta._id)
        super().__init__(name=self.bicicleta)
        Bicicleta._id += 1
        self.distancia = 0
        self.velocidad_inicial = randint(20, 60)
        self.tiempo_actual = 0
        self.bici_terminado = False
        self.terminado = False
        self.daemon = True
        self.start()

    def proxima_averia(self):
        if randint(0, 100) <= 10:
            return True
        return False

    def run(self):
        print("El {} ha comenzado su camino hacia el rescate!".format(self.bicicleta))
        while not self.bici_terminado and self.distancia < 600:
            self.tiempo_actual += 1
            time.sleep(1)
            self.distancia += self.velocidad_inicial
            if self.distancia > 600:
                self.distancia = 600
                Bicicleta.lista_llegados.append(self)
                break
            if self.distancia % 200 == 0:
                cansancio = randint(0, 5)
                if self.velocidad_inicial - cansancio >= 15:
                    self.velocidad_inicial -= cansancio
                else:
                    self.velocidad_inicial = 15
            if self.distancia >= 300 and self.proxima_averia():
                with Tecnico.Lock:
                    print("(Segundo {}) El Técnico ha llegado a auxiliar al {}".format(self.tiempo_actual,
                                                                                       self.ciclista))
                    tiempo = randint(2, 5)
                    time.sleep(tiempo)
                    self.tiempo_actual += tiempo
                    print("(Segundo {}) El {} reanuda su carrera!".format(self.tiempo_actual, self.ciclista))
        print("El {} ha llegado a su destino!".format(self.ciclista))
        self.genio.join()
        self.terminado = True
        self.tiempo_actual = max(self.tiempo_actual, self.genio.tiempo)
        print("El {} ha rescatado a la princesa en {} segundos!!!".format(self.bicicleta, self.tiempo_actual))

    def __str__(self):
        pass


class Tecnico(threading.Thread):

    Lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.daemon = True
        self.start()


class Rescate(threading.Thread):

    def __init__(self):
        super().__init__()
        self.equipos = []
        self.agregar_participante()
        self.rescate_terminado = False

    def agregar_participante(self):
        self.equipos.append(Bicicleta())
        self.equipos.append(Bicicleta())
        self.equipos.append(Bicicleta())

    def run(self):
        while not self.rescate_terminado:
            for equipo in self.equipos:
                if equipo.terminado:
                    self.rescate_terminado = True
                    break
        print("Posición de los Equipos:")
        for i, equipo in enumerate(Bicicleta.lista_llegados):
            print("{}. {} llegó a los {} metros!".format(i + 1, equipo.bicicleta, equipo.distancia))
            print("Este equipo esta conformado por el {} y el {}".format(equipo.ciclista, equipo.genio.name))
        equipos_restantes = filter(lambda x: x not in Bicicleta.lista_llegados,
                                   sorted(self.equipos, key=lambda x: x.distancia)[::-1])
        for i, equipo in enumerate(equipos_restantes):
            print("{}. {} llegó a los {} metros!".format(i + len(Bicicleta.lista_llegados), equipo.bicicleta,
                                                         equipo.distancia))
            print("Este equipo esta conformado por el {} y el {}".format(equipo.ciclista, equipo.genio.name))

class Genio(threading.Thread):

    Lock = threading.Lock()

    def __init__(self, _id):
        super().__init__()
        self.name = "Genio {}".format(_id)
        self.tiempo = 0
        self.terminado = False
        self.daemon = True
        self.start()

    @staticmethod
    def murcielago(text):
        diccionario = {"0": "m", "1": "u", "2": "r", "3": "c", "4": "i", "5": "e", "6": "l", "7": "a", "8": "g",
                       "9": "o"}
        resultado = ""
        for elem in text:
            for s in elem:
                code = diccionario.get(s)
                if code:
                    resultado += code
                else:
                    resultado += s
        return resultado

    def open_files(self):
        with open("Problema.txt", "r", encoding="utf-8") as file:
            return "".join(map(lambda x: x.lower(), file))

    def run(self):
        while not self.terminado:
            self.tiempo = randint(15, 25)
            time.sleep(self.tiempo)
            respuesta = Genio.murcielago(self.open_files())
            self.terminado = True
        print("El {} ha completado la solución!!\n".format(self.name))
        self.generate_file(respuesta)

    def generate_file(self, answer):
        with open("solucion.txt", "w", encoding="utf-8") as file:
            file.write(answer)
        print(answer)


if __name__ == "__main__":
    rescate1 = Rescate()
    rescate1.start()
    rescate1.join()
    #gl & hf

