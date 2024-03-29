import sys

from PyQt5.QtWidgets import (QWidget, QApplication)


class MiVentana(QWidget):
    def __init__(self):
        super().__init__()

        # Definimos la geometr?a de la ventana.
        # Par?metros: (x_top_left, y_top_left, width, height)
        self.setGeometry(100, 100, 500, 300)

        # Podemos dar nombre a la ventana (Opcional)
        self.setWindowTitle('Mi Primera Ventana')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec_())