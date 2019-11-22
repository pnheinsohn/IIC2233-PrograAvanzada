from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import OpenFilesFunctions as Files
import Exceptions as Ex
import Consultas
import time
import sys
import os


class T03Window(MyWindow):

    def __init__(self):
        super().__init__()

    def process_query(self, query_array):
        numero = str(next(num_consulta))
        respuestas = "----------- Set de Consultas N°{} ------------".format(numero)
        respuestas = "-" * (49 + len(numero)) + "\n{}\n".format(respuestas) + "-" * (49 + len(numero)) + "\n\n"
        try:
            for consulta in query_array:
                respuestas += Consultas.process_query(consulta, personas)
            self.add_answer(respuestas + "\n\n")
        except Ex.BadRequest as err1:
            print(err1)
            self.add_answer(respuestas + err1.comando + "\n")
            self.process_query([elem for elem in query_array if Consultas.consultas.get(elem[0])])
        finally:
            resultados["{}:\n".format(numero) + str(query_array)] = respuestas + "\n\n"

    def save_file(self, query_array):
        string = ["Número de veces guardado {}:\n{}".format(next(times_file_saved),
                                                            str(resultados[key])) for key in resultados]
        if not os.path.isfile("resultados.txt"):
            with open("resultados.txt", 'w', encoding='utf-8') as file:
                file.write("\n".join(string))
        else:
            with open("resultados.txt", 'a', encoding='utf-8') as file:
                file.write("\n".join(string))


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)

    before = time.time()

    with open("listas.txt", 'r', encoding="utf-8") as file:
        listas_dict = dict(map(lambda row: (row[:row.index(";")], row[row.index(";") + 2:].strip('\n')), file))

    with open("genomas.txt", 'r', encoding='utf-8') as file:
        personas = list(map(lambda row: Files.Persona(**Files.get_all_data(row, listas_dict)), file))
    print("Tiempo en leer genomas: {}".format(time.time() - before))

    num_consulta = Consultas.number()
    times_file_saved = Consultas.number()
    resultados = {}

    sys.__excepthook__ = hook

    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
