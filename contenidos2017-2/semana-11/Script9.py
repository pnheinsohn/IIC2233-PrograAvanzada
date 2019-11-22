import sys
from threading import Thread
from time import sleep

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton)


class Evento:
    """
    Esta clase maneja el evento que ser? transmitido por la se?al a su
    respectivo slot cada vez que se produzca la emisi?n. Por simplicidad este
    evento solo incluye un mensaje, pero en la medida que se requiera podr?a
    portar m?s informaci?n.
    """

    def __init__(self, msg=''):
        self.msg = msg


class MiThread(Thread):
    """
    Esta clase representa un thread personalizado que ser? utilizado durante
    la ejecuci?n de la GUI.
    """

    def __init__(self, trigger_signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trigger = trigger_signal

    def run(self):
        # Creamos un evento para transmitir datos desde el thread a la interfaz
        evento = Evento()

        # TO-DO
        for i in range(10):
            sleep(0.5)
            evento.msg = str(i)
            self.trigger.emit(evento)

        evento.msg = 'Status: thread terminado'
        self.trigger.emit(evento)


class MiVentana(QWidget):

    # Creamos una se?al para manejar la respuesta del thread
    threads_response = pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_gui()
        self.thread = None

    def init_gui(self):
        # Configuramos los widgets de la interfaz
        self.label = QLabel('Status: esperando thread', self)
        self.boton = QPushButton('Start Thread', self)
        self.boton.clicked.connect(self.start_threads)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.label)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.boton)
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(2)
        self.setLayout(vbox)

        # Conectamos la se?al del thread al m?todo que maneja
        self.threads_response.connect(self.update_labels)

        # Configuramos las propiedades de la ventana.
        self.setWindowTitle('Ejemplo threads')
        self.setGeometry(50, 50, 250, 200)
        self.show()

    def start_threads(self):
        """
        Este m?todo crea un thread cada vez que se presiona el bot?n en la
        interfaz. El thread recibir? como argumento la se?al sobre la cual
        debe operar.
        """
        if self.thread is None or not self.thread.is_alive():
            self.thread = MiThread(self.threads_response)
            self.thread.start()

    def update_labels(self, evento):
        """
        Este m?todo actualiza el label seg?n los datos enviados desde el
        thread atrav?s del objeto evento. Para este ejemplo, el m?todo
        recibe el evento, pero podr?a
        eventualmente no recibir nada.
        """
        self.label.setText(evento.msg)


if __name__ == '__main__':
    app = QApplication([])
    form = MiVentana()
    sys.exit(app.exec_())