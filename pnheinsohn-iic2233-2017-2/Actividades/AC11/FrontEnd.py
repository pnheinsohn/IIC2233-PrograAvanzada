import sys
from PyQt5.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QPixmap
from BackEnd import TragaMoneda
from random import choice
from PyQt5.Qt import QTest


class Ventana(QWidget):

    def __init__(self):
        super().__init__()
        self.__setUp()

    def __setUp(self):
        self.back_end = TragaMoneda()
        self.otra_ventana = Ventana2(self.back_end)
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("The Walking Luddite")
        self.set_initial_layout()

    def boton_ingresar_clickeado(self):
        self.hide()
        self.user = self.back_end.receive_username(self.edit1.text())
        self.otra_ventana.set_initial_layout(self.user)
        self.otra_ventana.show()


    def set_initial_layout(self):
        self.label1 = QLabel("Ingrese Nombre Usuario:", self)
        self.edit1 = QLineEdit('', self)
        self.boton_ingresar = QPushButton("Ingresar/Registrar", self)
        self.boton_ingresar.resize(self.boton_ingresar.sizeHint())
        self.boton_ingresar.clicked.connect(self.boton_ingresar_clickeado)

        hbox = QHBoxLayout()
        hbox.addWidget(self.label1)
        hbox.addStretch(1)
        hbox.addWidget(self.edit1)
        hbox.addStretch(1)
        hbox.addWidget(self.boton_ingresar)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(0.5)
        vbox.addLayout(hbox)
        vbox.addStretch(3)

        self.setLayout(vbox)


class Ventana2(QWidget):
    def __init__(self, back_end):
        super().__init__()
        self.back_end = back_end
        self.image1 = QLabel(self)
        self.image1.setPixmap(QPixmap("0.png").scaled(450 / 8, 300 / 4))
        self.image1.setFixedSize(80, 60)
        self.image1.show()

        self.image2 = QLabel(self)
        self.image2.setPixmap(QPixmap("0.png").scaled(450 / 8, 300 / 4))
        self.image2.setFixedSize(80, 60)
        self.image2.show()

        self.image3 = QLabel(self)
        self.image3.setPixmap(QPixmap("0.png").scaled(450 / 8, 300 / 4))
        self.image3.setFixedSize(80, 60)
        self.image3.show()

        self.__setUp()

    def __setUp(self):
        self.back_end = TragaMoneda()
        self.setGeometry(100, 100, 450, 300)
        self.setWindowTitle("The Walking Luddite")

    def set_initial_layout(self, user):
        self.user = user
        self.label2 = QLabel("¡Hola {}!".format(user.username))
        self.label3 = QLabel("Máximo Premio Ganado: {}".format(user.max_bid))
        self.label4 = QLabel("Última apuesta: {}".format(user.last_bid))
        self.label5 = QLabel("Saldo: {}".format(user.money))
        self.label6 = QLabel("Apuesta Actual:", self)
        self.label7 = QLabel("0", self)
        self.boton_sum = QPushButton("+", self)
        self.boton_sum.resize(self.boton_sum.sizeHint())
        self.boton_sum.clicked.connect(self.add)
        self.boton_restar = QPushButton("-", self)
        self.boton_restar.resize(self.boton_restar.sizeHint())
        self.boton_restar.clicked.connect(self.restar)

        vbox_botones_mas_menos = QVBoxLayout()
        vbox_botones_mas_menos.addWidget(self.boton_sum)
        vbox_botones_mas_menos.addWidget(self.boton_restar)

        hbox_apuesta = QHBoxLayout()
        hbox_apuesta.addStretch(2)
        hbox_apuesta.addWidget(self.label6)
        hbox_apuesta.addWidget(self.label7)
        hbox_apuesta.addStretch(1)
        hbox_apuesta.addLayout(vbox_botones_mas_menos)
        hbox_apuesta.addStretch(1)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.label2)
        hbox1.addStretch(1)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label3)
        vbox1.addWidget(self.label4)
        vbox1.addWidget(self.label5)

        vbox2 = QVBoxLayout()
        vbox2.addLayout(hbox1)
        vbox2.addLayout(vbox1)
        vbox2.addStretch(1)

        hbox_image = QHBoxLayout()

        self.boton_roll = QPushButton("Apostar!", self)
        self.boton_roll.resize(self.boton_roll.sizeHint())
        self.boton_roll.clicked.connect(self.roll)

        hbox_image.addWidget(self.image1)
        hbox_image.addWidget(self.image2)
        hbox_image.addWidget(self.image3)
        hbox_image.addStretch(1)
        hbox_image.addWidget(self.boton_roll)
        hbox_image.addStretch(1)

        vbox2.addLayout(hbox_image)
        vbox2.addLayout(hbox_apuesta)
        vbox2.addStretch(3)
        self.setLayout(vbox2)

    def roll(self):
        three_images = [choice(["1.png", "2.png", "3.png"]),
                        choice(["3.png", "1.png", "2.png"]),
                        choice(["3.png", "1.png", "2.png"])]
        QTest.qWait(500)
        self.image1.setPixmap(QPixmap(three_images[0]).scaled(450 / 8, 300 / 4))
        QTest.qWait(500)
        self.image2.setPixmap(QPixmap(three_images[1]).scaled(450 / 8, 300 / 4))
        QTest.qWait(500)
        self.image3.setPixmap(QPixmap(three_images[2]).scaled(450 / 8, 300 / 4))
        factor = self.back_end.calcular_puntaje(*three_images)
        earnings = self.user.apuesta_actual * factor
        self.user.money += earnings
        self.user.last_bid = self.user.apuesta_actual
        self.user.apuesta_actual = 0
        self.label7.setText(str(self.user.apuesta_actual))


    def add(self):
        if self.user.money >= 50:
            self.user.apuesta_actual += 50
            self.user.money -= 50
        self.label7.setText(str(self.user.apuesta_actual))
        self.label5.setText("Saldo: {}".format(self.user.money))

    def restar(self):
        if self.user.apuesta_actual >= 50:
            self.user.apuesta_actual -= 50
            self.user.money += 50
        self.label7.setText(str(self.user.apuesta_actual))
        self.label5.setText("Saldo: {}".format(self.user.money))

    def cerrar_sesion(self):
        self.hide()





if __name__ == "__main__":
    app = QApplication([])
    form = Ventana()
    form.show()
    sys.exit(app.exec_())