import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QGridLayout, QVBoxLayout, QLineEdit)


class MiVentana(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_GUI()

    def init_GUI(self):

        # Creamos una etiqueta para status. Recordar que los os Widget simples
        # no tienen StatusBar.
        self.label1 = QLabel('Status:', self)
        self.insertar = QLineEdit('', self)
        self.insertar.setGeometry(10, 10, 50, 50)

        # Creamos la grilla para ubicar los Widget (botones) de manera matricial
        self.grilla = QGridLayout()

        valores = ['1', '2', '3',
                   '4', '5', '6',
                   '7', '8', '9',
                   '0', 'CE', 'C']

        # Generamos las posiciones de los botones en la grilla y le asociamos
        # el texto que debe desplegar cada boton guardados en la lista valores

        posicion = [(i, j) for i in range(4) for j in range(3)]

        for pos, valor in zip(posicion, valores):
            if valor == '':
                continue

            boton = QPushButton(valor)

            # El * permite convertir los elementos de la tupla como argumentos
            # independientes

            """
            Aqu? conectamos el evento clicked() de cada boton con el slot 
            correspondiente. En este ejemplo todos los botones usan el 
            mismo slot.
            """
            boton.clicked.connect(self.boton_clickeado)

            self.grilla.addWidget(boton, *pos)

        # Creamos un layout vertical
        vbox = QVBoxLayout()

        # Agregamos el label al layout con addWidget
        vbox.addWidget(self.label1)
        vbox.addWidget(self.insertar)

        # Agregamos el layout de la grilla al layout vertical con addLayout
        vbox.addLayout(self.grilla)
        self.setLayout(vbox)

        self.move(300, 150)
        self.setWindowTitle('Calculator')

    def boton_clickeado(self):
        """
        Esta funcion se ejecutar? cada vez que uno de los botones de la grilla
        es presionado. Cada vez que el bot?n genera el evento, la funci?n inspecciona
        cual boton fue presionado y recupera la posicion en que se encuentra en
        la grilla.
        """

        # Sender retorna el objeto que fue clickeado. En boton ahora hay una
        # instancia de QPushButton()
        boton = self.sender()

        # Obtenemos el identificador del elemento en la grilla
        idx = self.grilla.indexOf(boton)

        # Con el identificador obtenemos la posici?n del ?tem en la grilla
        posicion = self.grilla.getItemPosition(idx)

        # Actualizamos label1
        self.label1.setText('Presionado boton {}, en fila/columna: {}.'.format(idx + 1, posicion[:2]))


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    form.show()
    sys.exit(app.exec_())