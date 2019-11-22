import gui
import sys
import random
from Piezas import Pieza, TipoPieza
from EDD import ListaLigada, Node


def get_next_number():
    num = 1
    while True:
        yield num
        num += 1

a = get_next_number()


class Tablero(gui.GameInterface):

    def __init__(self):
        self.guardados = ""
        self.pieces_to_add_check = ""
        self.pieces_to_add = ""
        self.numbers_saved = ""
        self._color = ""
        self._piece_type = ""
        self.historial = ""
        self.used_ij = ""
        self.i_inicial = random.randint(0, 7)
        self.j_inicial = random.randint(0, 7)
        self._num_arriba = 1
        self.cantidad_juegos = 1
        self.int_pieces_left = 0
        self.lista_piezas_totales = ListaLigada()
        self.lista_piezas_tablero = ListaLigada()
        self.iterable = None
        self.game_ended = False

    @property
    def num_arriba(self):
        return self._num_arriba

    @num_arriba.setter
    def num_arriba(self, value):
        if value > 6:
            self._num_arriba = 1
        else:
            self._num_arriba = value

    @property
    def piece_type(self):
        number_chosen = random.randint(1, self.int_pieces_left)
        actual_number = 0
        for piece in self.lista_piezas_totales:
            actual_number += piece.cantidad
            if actual_number >= number_chosen:
                piece.cantidad -= 1
                self.int_pieces_left -= 1
                self._piece_type = piece.type
                return self._piece_type

    @piece_type.setter
    def piece_type(self, value):
        first = False
        second = False
        for piece in self.lista_piezas_totales:
            if piece.type == value:
                piece.cantidad -= 1
                self._piece_type = value
                first = True
            elif piece.type == self._piece_type:
                piece.cantidad += 1
                second = True
            if first and second:
                break

    @property
    def color(self):
        if self._color == "red":
            self._color = "blue"
        elif self._color == "blue":
            self._color = "red"
        else:
            self._color = random.choice(["red", "blue"])
        return self._color

    def colocar_pieza(self, i, j):
        if not self.game_ended:
            print("Presionaste", (i, j))
            piece = Node(Pieza(self._piece_type, i, j, self.num_arriba, self._color))
            if "{},{}\n".format(i, j) not in self.historial and self.valid_position(self.historial, piece.valor):
                self.cantidad_juegos += 1
                gui.add_piece(i, j)
                self.lista_piezas_tablero.append(piece)
                self.historial += "{},{},{},{},{}\n".format(self._color[0], self._piece_type, self.num_arriba, i, j)
                gui.nueva_pieza(color=self.color, piece_type=self.piece_type)
                self.num_arriba = 1
                self.check_tablero()
            else:
                print("Espacio invalido")
        else:
            print("Juego terminado")

    def rotar_pieza(self, orientation):
        self.num_arriba += 1
        print(orientation)

    def retroceder(self):
        if not self.game_ended:
            print("Presionaste retroceder")
            enter = False
            first = False
            second = False
            self.lista_piezas_tablero.reverse()
            for i in range(len(self.lista_piezas_tablero)):
                if i == len(self.lista_piezas_tablero) - 1:
                    break
                elif self.lista_piezas_tablero[i].valor.color == self._color:
                    enter = True
                    self.cantidad_juegos -= 1
                    for piece_types in self.lista_piezas_totales:
                        if self.lista_piezas_tablero[i].valor.type == piece_types.type:
                            piece_types.cantidad += 1
                            self.int_pieces_left += 1
                            first = True
                        elif piece_types.type == self._piece_type:
                            piece_types.cantidad += 1
                            self.int_pieces_left += 1
                            second = True
                        if first and second:
                            break
                    break
            if enter:
                piece = self.lista_piezas_tablero.pop(i)
                self.lista_piezas_tablero.reverse()
                index = self.historial.find("{},{}\n".format(piece.valor.i, piece.valor.j))
                self.historial = self.historial[:index - 11] + self.historial[index + 4:]
                gui.pop_piece(piece.valor.i, piece.valor.j)
                gui.nueva_pieza(color=self.color, piece_type=self.piece_type)
                return
            else:
                self.lista_piezas_tablero.reverse()
                print("No Piece To Take Out")
                return
        else:
            print("Juego Terminado")

    def terminar_juego(self):
        self.game_ended = True
        string = self.count_points()
        gui.set_points(string[:string.find(":") + 1], string[string.find(":") + 1:string.find("/")])
        gui.set_points(string[string.find("/") + 1:string.rfind(":")], string[string.rfind(":") + 1:])
        print("Juego terminado\nPuntajes: {}".format(string))
        if int(string[string.find(":") + 1:string.find("/")]) > int(string[string.rfind(":") + 1:]):
            print("Jugador rojo ha ganado!")
        elif int(string[string.find(":") + 1:string.find("/")]) < int(string[string.rfind(":") + 1:]):
            print("Jugador azul ha ganado!")
        else:
            print("Empate!")

    def hint_asked(self):
        if not self.game_ended:
            for i in range(8):
                for j in range(8):
                    for index in range(6):
                        piece = Node(Pieza(self._piece_type, i, j, index + 1, self._color))
                        if "{},{}\n".format(i, j) not in self.historial and self.valid_position(self.historial,
                                                                                                piece.valor):
                            gui.add_hint(i, j)
                            return
            print("Me pediste una pista y no te la dare :P")
        else:
            print("Juego terminado")

    def click_number(self, number):
        self.game_ended = False
        self.save_history_csv()
        self.lista_piezas_tablero = ListaLigada()
        self.historial = ""
        for i in range(self.numbers_saved[self.numbers_saved.find(number):].count("/")):
            gui.pop_number()
        self.numbers_saved = self.numbers_saved.replace(self.numbers_saved[self.numbers_saved.find(number):], "")
        i = 0
        tablero_ = ""
        for string in self.guardados:
            tablero_ += string
            if string == "/":
                i += 1
            if i == int(number):
                tablero_ = tablero_[:-1]
                break
        numero = int(tablero_[tablero_.rfind("/") + 1:])
        self.generate_old_pieces(numero)
        self.generate_piece_to_add(number)
        self.check_tablero()

    def guardar_juego(self):
        print("Presionaron guardar")
        number = next(a)
        self.guardados += str(self.cantidad_juegos) + "/"
        self.pieces_to_add += "{},{}/".format(self._color[0], self._piece_type)
        self.numbers_saved += str(number) + "/"
        self.save_history_csv()
        gui.add_number(number, self._color)
        for piece_type in self.lista_piezas_totales:
            if piece_type.type == self._piece_type:
                piece_type.cantidad += 1
                self.int_pieces_left += 1
                break
        gui.nueva_pieza(color=self.color, piece_type=self.piece_type)
        print("Estado guardado con exito")

    def first_random_piece(self):
        gui.nueva_pieza(color=self.color, piece_type=self.piece_type)  # Para que la regla del color alternado se cumpla
        gui.add_piece(self.i_inicial, self.j_inicial)
        piece = Node(Pieza(self._piece_type, self.i_inicial, self.j_inicial, self.num_arriba, self._color))
        self.lista_piezas_tablero.append(piece)
        self.historial += "{},{},{},{},{}\n".format(self._color[0], self._piece_type, 1, self.i_inicial, self.j_inicial)
        gui.nueva_pieza(color=self.color, piece_type=self.piece_type)

    def valid_position(self, string, piece):
        validated = ""
        self.used_ij = ""
        self.recursion_check(string, piece.i, piece.j)
        while len(self.used_ij) != 0:
            validated += str(self.check_type_validation(int(self.used_ij[0]), int(self.used_ij[2]), piece)) + "/"
            self.used_ij = self.used_ij[4:]
        if validated.find("False") != -1 or len(validated) == 0:
            return False
        else:
            return True

    def recursion_check(self, string, i, j):
        used_i = int(string[11])
        used_j = int(string[13])
        string = string[string.find("\n") + 1:]
        if len(string) != 0:
            self.recursion_check(string, i, j)
        if self.check_ij_validation(i, j, used_i, used_j):
            self.used_ij += "{},{}/".format(used_i, used_j)

    def check_ij_validation(self, i, j, used_i, used_j):
        i_dif = used_i - i
        j_dif = used_j - j
        if (used_j % 2 == 0 and -1 <= i_dif <= 1 and -1 <= j_dif <= 1 and not  # Caso en que se verifica con used_j par
                (i_dif == j_dif == 1 or (i_dif == 1 and j_dif == -1))) or \
            (used_j % 2 != 0 and -1 <= i_dif <= 1 and -1 <= j_dif <= 1 and not  # Caso used_j impar
                (i_dif == j_dif == -1 or (i_dif == -1 and j_dif == 1))):
            return True
        else:
            return False

    def check_type_validation(self, used_i, used_j, piece):
        for used_piece in self.lista_piezas_tablero:
            if used_piece.valor.i == used_i and used_piece.valor.j == used_j:
                if (used_j % 2 == 0 and used_i == piece.i - 1 and used_j == piece.j - 1) or \
                        (used_j % 2 != 0 and used_i == piece.i and used_j == piece.j - 1):  # used is top left
                    return piece.vecinos_disponibles[0] == used_piece.valor.vecinos_disponibles[5]
                elif used_i == piece.i - 1 and used_j == piece.j:  # used is up
                    return piece.vecinos_disponibles[1] == used_piece.valor.vecinos_disponibles[4]
                elif (used_j % 2 == 0 and used_i == piece.i - 1 and used_j == piece.j + 1) or \
                        (used_j % 2 != 0 and used_i == piece.i and used_j == piece.j + 1):  # used is top right
                    return piece.vecinos_disponibles[2] == used_piece.valor.vecinos_disponibles[3]
                elif (used_j % 2 == 0 and used_i == piece.i and used_j == piece.j - 1) or \
                        (used_j % 2 != 0 and used_i == piece.i + 1 and used_j == piece.j - 1):  # used is down left
                    return piece.vecinos_disponibles[3] == used_piece.valor.vecinos_disponibles[2]
                elif used_i == piece.i + 1 and used_j == piece.j:  # used is down
                    return piece.vecinos_disponibles[4] == used_piece.valor.vecinos_disponibles[1]
                elif (used_j % 2 == 0 and used_i == piece.i and used_j == piece.j + 1) or \
                        (used_j % 2 != 0 and used_i == piece.i + 1 and used_j == piece.j + 1):  # used is down right
                    return piece.vecinos_disponibles[5] == used_piece.valor.vecinos_disponibles[0]

    def check_tablero(self):
        self.check_colors()
        if not self.can_play():  # Con None/False entra
            self.terminar_juego()

    def check_colors(self):
        pass

    def can_play(self):
        if self.int_pieces_left > 0:
            for i in range(8):
                for j in range(8):
                    for index in range(6):
                        piece = Node(Pieza(self._piece_type, i, j, index + 1, self._color))
                        if "{},{}\n".format(i, j) not in self.historial and self.valid_position(self.historial,
                                                                                                piece.valor):
                            return True

    def count_points(self):
        red_points = 0
        blue_points = 0
        return "red:{}/blue:{}".format(red_points, blue_points)

    def generate_all_pieces(self):
        csv = open("pieces.csv", "r", encoding="utf-8")
        for row in csv:
            index = row.find(",")
            self.int_pieces_left += int(row[index + 1:])
            new_piece = TipoPieza(row[:index], int(row[index + 1:]))
            self.lista_piezas_totales.append(new_piece)

    def generate_old_pieces(self, number):
        csv = open("historial.csv", 'r', encoding="utf-8")
        self.cantidad_juegos = 0
        for i, row in enumerate(csv):
            if i <= number - 1:
                if row[0] == "r":
                    self._color = "red"
                else:
                    self._color = "blue"
                new_piece = Node(Pieza(row[2:8], int(row[11]), int(row[13]), int(row[9]), self._color))
                self.historial += "{},{},{},{},{}\n".format(new_piece.valor.color[0], new_piece.valor.type,
                                                            new_piece.valor.num_arriba, new_piece.valor.i,
                                                            new_piece.valor.j)
                self.lista_piezas_tablero.append(new_piece)
                self.cantidad_juegos += 1
            else:
                gui.pop_piece(int(row[11]), int(row[13]))
                for piece in self.lista_piezas_totales:
                    if piece.type == row[2:8]:
                        piece.cantidad += 1
                        self.int_pieces_left += 1
                        break
        csv.close()

    def generate_piece_to_add(self, number):
        piece_info = ""
        i = 0
        for string in self.pieces_to_add:
            piece_info += string
            if string == "/":
                i += 1
            if i == int(number):
                piece_info = piece_info[:-1]
                break
        self.pieces_to_add = piece_info + "/"
        index = piece_info.rfind("/")
        if piece_info[index + 1] == "r":
            self._color = "red"
        else:
            self._color = "blue"
        self.piece_type = piece_info[index + 3:]
        gui.nueva_pieza(color=self._color, piece_type=self._piece_type)

    def save_history_csv(self):
        save_csv = open("historial.csv", "w", encoding="utf-8")
        save_csv.write(self.historial)
        save_csv.close()


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)


    sys.__excepthook__ = hook

    tablero = Tablero()
    gui.set_scale(False)  # Any float different from 0
    gui.init()
    gui.set_quality("ultra")  # low, medium, high ultra
    gui.set_animations(False)
    gui.set_game_interface(tablero)  # GUI Listener
    gui.init_grid()
    tablero.generate_all_pieces()
    tablero.first_random_piece()
    gui.run()
