import sys

from PyQt5.QtCore import (QObject, pyqtSignal)
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel)


class MiSenhal(QObject):
    """
    Esta clase contiene las se?ales que permite la comunicaci?n entre
    elementos de la GUI.
    """
    escribe_senhal = pyqtSignal()


class MiFormulario(QWidget):
    def __init__(self):
        super().__init__()
        self.inicializa_GUI()

    def inicializa_GUI(self):
        # Creamos un objeto para manejar las se?ales y conectamos el mtodo
        # encargado de ejecutar la tarea
        self.s = MiSenhal()
        self.s.escribe_senhal.connect(self.escribe_etiqueta)

        self.etiqueta1 = QLabel('Etiqueta', self)
        self.etiqueta1.move(20, 10)
        self.resize(self.etiqueta1.sizeHint())

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mousePressEvent(self, event):
        """
        Este evento maneja cuando se presiona alguno de los botones del
        mouse. Nada nos impide emitir una se?al hacia la interfaz cuando ocurre
        este evento.
        """
        self.s.escribe_senhal.emit()

    def escribe_etiqueta(self):
        self.etiqueta1.setText('Presionaron el mouse')
        self.etiqueta1.resize(self.etiqueta1.sizeHint())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MiFormulario()
    sys.exit(app.exec_())