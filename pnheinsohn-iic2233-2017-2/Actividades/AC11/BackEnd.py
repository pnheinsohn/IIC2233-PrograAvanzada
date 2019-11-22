from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtCore import QObject
from collections import namedtuple


class TragaMoneda(QObject):

    def __init__(self):
        super().__init__()
        self.usernames = {}
        self.last_user = None

    def receive_username(self, texto):
        if self.usernames.get(texto):
            pass
        else:
            self.usernames[texto] = Usuario(texto)
        self.last_user = self.usernames[texto]
        return self.last_user

    def calcular_puntaje(self, *imagenes):
        amount_seven = imagenes.count("1.png")
        amount_guindas = imagenes.count("2.png")
        amount_limones = imagenes.count("3.png")
        if amount_seven == 3:
            return 2
        elif amount_guindas == 3:
            return 1.5
        elif amount_limones == 3:
            return 1.25
        elif amount_seven == 1 or amount_seven == 2:
            return 0.9
        elif amount_guindas== 2:
            return 0.8
        else:
            return 0


class Usuario:

    def __init__(self, user):
        self.username = user
        self.last_bid = 0
        self.money = 1500
        self.max_bid = 0
        self.apuesta_actual = 0