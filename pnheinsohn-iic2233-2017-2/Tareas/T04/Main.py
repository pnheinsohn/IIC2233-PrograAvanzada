from Simulation import Simulation
from Functions import go_param_kwargs
import time
import os


class Main:

    def __init__(self):
        self.run()
        self.actual_scenario = ""

    def open_params(self, file):
        scenarios = []
        with open(file, "r", encoding="utf-8") as init_params:
            header = next(init_params)
            params = [go_param_kwargs([header.strip("\n").split(", "), param.strip("\n").split(",")])
                      for param in init_params]
            for param in params:
                if "escenario" in param:
                    scenarios.append("Escenario N°" + param["escenario"])
                    del param["escenario"]
        if len(scenarios) == 0:
            self.actual_scenario = "Initial Paramerets"
            self.run_simulation(params, 1)
        else:
            print("Escenarios Disponibles:")
            i = 0
            for i, scene in enumerate(scenarios):
                print("{}.\t{}".format(i + 1, scene))
            print("{}.\tSalir".format(i + 2))
            while True:
                answer = input("\nOpción elegida: ")
                if answer.isdigit() and 1 <= int(answer) <= len(scenarios):
                    self.actual_scenario = scenarios[int(answer) - 1]
                    print("¿Cantidad de Repeticiones?")
                    while True:
                        answer = input("Opción elegida (máximo 10... 0 para salir): ")
                        if answer.isdigit() and 1 <= int(answer) <= 10:
                            for i in range(int(answer)):
                                self.run_simulation(params, answer)
                            break
                        elif answer == "0":
                            break
                        else:
                            print("Respuesta inválida, pruebe nuevamente")
                    print("")
                    break
                elif answer.isdigit() and int(answer) == len(scenarios) + 1:
                    print("")
                    break
                else:
                    print("Opción inválida, pruebe nuevamente")

    def save_statistical_info(self, string):
        if os.path.isfile("resultados.csv"):
            file = open("resultados.csv", "a", encoding="utf-8")
        else:
            file = open("resultados.csv", "w", encoding="utf-8")
            file.write("name;min_prod;min_amount;max_prod;max_amount;prom_prod;stereo_times;temperature_times;")
            file.write("burger_rain_times;prom_ppl1;prom_ppl2;prom_ppl3;month1;month2;month3;month4;quality;toxic;")
            file.write("decompose;abandon_line;stockless")
        file.write("\n{};".format(self.actual_scenario) + string)
        file.close()

    def show_best_scenarios(self):
        with open("resultados.csv", "r", encoding="utf-8") as files:
            header = next(files)
            places = [(None, -float("Inf")), (None, -float("Inf")), (None, -float("Inf"))]
            for file in files:
                name_score = self.get_scores(file.strip("\n").split(";"))
                for place in places:
                    if place[1] < name_score[1]:
                        places[places.index(place)] = name_score
                        places = sorted(places, key=lambda tupla: tupla[1])
                        break
        places = places[::-1]
        for i, place in enumerate(places):
            print("{}. {} con {} puntos".format(i + 1, place[0], place[1]))

    @staticmethod
    def get_scores(array):
        score = 0
        name = array[0]
        if int(array[2]) > 0:  # min_amount
            score += 2
        if int(array[4]) > 8:  # max_amount
            score += 1
        if int(array[5]) > 120:  # prom_prod
            score += 10
        if int(array[6]) > 5:  # stereo_times
            score += 10
        if int(array[7]) <= 6:  # extreme_temp
            score += 10
        if int(array[8]) <= 6:  # Burger_rain
            score += 2
        if int(array[9]) > 50:  # people_12:00-12:59
            score += 5
        if int(array[10]) > 50:  # people_13:00-13:59
            score += 5
        if int(array[11]) > 50:  # people_14:00-14:59
            score += 5
        if int(array[12]) < 1000:  # monthly didn't eat
            score += 5
        if int(array[13]) < 1000:  # monthly didn't eat
            score += 5
        if int(array[14]) < 1000:  # monthly didn't eat
            score += 5
        if int(array[15]) < 1000:  # monthly didn't eat
            score += 5
        if float(array[16]) > 0.5:  # quality
            score += 15
        if int(array[17]) <= 10:  # toxic
            score += 20
        if int(array[18]) <= 500:  # decompose
            score += 10
        if float(array[19]) <= 5:  # abandon
            score += 10
        if float(array[20]) <= 5:  # stockless
            score += 5
        return name, score

    def run_simulation(self, params, index):
        scenario = Simulation(**params[int(index) - 1])
        time_before_simulation = time.time()
        scenario.run()
        print("\nSimulación completada\nTiempo Ejecución: {}\n¿Obtener información estadística de este escenario?"
              .format(time.time() - time_before_simulation))
        while True:
            answer = input("Opción elegida (y o n): ")
            string = scenario.get_statistical_information()
            self.save_statistical_info(string)
            if answer.lower() == "y":
                print('''\n\t\t[ESTADISTICAS {}]
                    Cantidad mínima, máxima y promedio de productos vendidos:
                    Min: {} fue vendido {} veces en un día
                    Max: {} fue vendido {} veces en un día
                    Promedio: {} productos por día
                    ------
                    Número de veces que ocurrió la concha acústica:
                    {}
                    ------
                    Número de veces que ocurrieron temperaturas extremas:
                    {}
                    ------
                    Número de veces que ocurrió una lluvia de hamburguesas:
                    {}
                    ------
                    Promedio de personas que almorzaron en los siguientes intervalos:
                    12:00-12:59: {} por dia
                    13:00-13:59: {} por dia
                    14:00-15:00: {} por dia
                    ------
                    Cantidad de estudiantes que no almorzaron por mes:
                    Mes N°1: {}
                    Mes N°2: {}
                    Mes N°3: {}
                    Mes N°4: {}
                    ------
                    Calidad promedio de productos de todos los vendedores:
                    {}
                    ------
                    Cantidad de miembros intoxicados por vendedor:
                    {}
                    ------
                    Cantidad de productos que se descompusieron:
                    {}
                    ------
                    Cantidad promedio de miembros UC que abandonaron una cola de espera por día:
                    {}
                    ------
                    Cantidad promedio de vendedores por día que se quedaron sin stock:
                    {}
                    '''.format(self.actual_scenario, *string.strip("\n").split(";")))
                print("")
                input("Ingrese cualquier tecla para continuar...")
                break
            elif answer.lower() == "n":
                break
            else:
                print("Opción inválida, pruebe nuevamente")

    def run(self):
        while True:
            print('''Simulación del 'Almuerzo UC':
                1. Parámetros Iniciales
                2. Escenarios
                3. Mostrar mejor escenario
                4. Salir
                ''')
            answer = input("Opción elegida (1, 2, 3 o 4): ")
            print("")
            if answer == "1":
                print("Abriendo parámetros iniciales...")
                self.open_params("parametros_iniciales.csv")
            elif answer == "2":
                self.open_params("escenarios.csv")
            elif answer == "3":
                if os.path.isfile("resultados.csv"):
                    self.show_best_scenarios()
                else:
                    print("\nNo se han ejecutado escenarios\n")
            elif answer == "4":
                if os.path.isfile("resultados.csv"):
                    os.remove("resultados.csv")
                print("¡Hasta pronto!")
                break
            else:
                print("Respuesta inválida, pruebe nuevamente")


if __name__ == "__main__":

    main_program = Main()
