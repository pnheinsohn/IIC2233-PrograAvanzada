import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget)
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, QAction)


class MiFormulario(QWidget):
    def __init__(self):
        super().__init__()
        self.init_GUI()

    def init_GUI(self):
        """
        Este m?todo inicializa el main widget y sus elementos.
        """
        self.label1 = QLabel('Texto', self)
        self.label2 = QLabel('Echo texto:', self)

        print(self.__dict__)

        self.edit = QLineEdit('', self)
        self.edit.setGeometry(45, 15, 100, 20)

        self.boton = QPushButton('&Procesar', self)
        self.boton.resize(self.boton.sizeHint())
        self.boton.clicked.connect(self.boton1_callback)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.label1)
        hbox.addWidget(self.edit)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.label2)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.boton)
        hbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)

    def boton1_callback(self):
        """
        Este m?todo es el encargado ejecutar una acci?n cada vez que el bot?n
        es presionado. En esta caso, realiza el cambio en label2 y el status bar
        mediate la emisi?n de una se?al en la cual se env?a el texto correspondiente.
        """
        self.label2.setText('Echo texto: {}'.format(self.edit.text()))
        self.status_bar.emit('Qedit: {}'.format(self.edit.text()))

    def load_status_bar(self, signal):
        """
        Este m?todo recibir? una se?al desde el MainWindow que permitir? hacer cambios
        en el status bar desde el widget central.
        """
        self.status_bar = signal


class MainWindow(QMainWindow):
    """
    Esta se?al permite comunicar la barra de estados con el resto de los widgets
    en el formulario, incluidos el central widget.
    """
    onchange_statusbar = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        """Configuramos la geometr?a de la ventana."""
        self.setWindowTitle('Ventana con Boton')
        self.setGeometry(200, 100, 300, 250)

        """Configuramos las acciones."""
        ver_status = QAction(QIcon(None), '&Cambiar Status', self)
        ver_status.setStatusTip('Este es un ?tem de prueba')
        ver_status.triggered.connect(self.cambiar_status_bar)

        salir = QAction(QIcon(None), '&Exit', self)
        salir.setShortcut('Ctrl+Q')
        salir.setStatusTip('Exit application')
        salir.triggered.connect(QApplication.quit)

        """Creamos la barra de men?."""
        menubar = self.menuBar()
        archivo_menu = menubar.addMenu('&Archivo')  # primer men?
        archivo_menu.addAction(ver_status)
        archivo_menu.addAction(salir)

        otro_menu = menubar.addMenu('&Otro Men?')  # segundo men?

        """Inclu?mos la barra de estado."""
        self.statusBar().showMessage('Listo')
        self.onchange_statusbar.connect(self.update_status_bar)

        """
        Configuramos el widget central con una instancia de la clase
        Formulario(). Adem?s cargamos la se?al en el central widget para 
        que este pueda interactuar con la barra de estados de la ventana 
        principal.
        """
        self.form = MiFormulario()
        self.setCentralWidget(self.form)
        self.form.load_status_bar(self.onchange_statusbar)

    def cambiar_status_bar(self):
        self.statusBar().showMessage('Cambi? el Status')

    def update_status_bar(self, msg):
        self.statusBar().showMessage(msg)


if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())