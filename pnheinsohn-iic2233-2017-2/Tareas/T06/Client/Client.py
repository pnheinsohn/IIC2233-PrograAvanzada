import json
import pickle
import sys
import os
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from FrontEnd import MainWindow
from PyQt5.QtWidgets import QApplication
from Variables import *


class Client:

    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.frontend = MainWindow(self)
        self.frontend.show()

        try:
            self.client_socket.connect((self.host, self.port))
            print("Client successfully has connected to {}:{}".format(self.host, self.port))

            self.connected = True

            listen_thread = Thread(target=self.listen_server_thread, daemon=True)
            listen_thread.start()

        except ConnectionRefusedError:
            print("Connection Ended")
            self.client_socket.close()
            exit()

    def listen_server_thread(self):
        while self.connected:
            try:
                response_byte_length = self.client_socket.recv(4)
                response_length = int.from_bytes(response_byte_length, byteorder="big")

                response = bytearray()

                while len(response) < response_length:
                    response += self.client_socket.recv(256)

                decoded_message = json.loads(response.decode())  # Json
                self.handle_command(decoded_message)
            except UnicodeDecodeError:
                decoded_message = pickle.loads(response)  # Pickle
                self.handle_command(decoded_message)
            except ConnectionResetError:
                print("Connection Ended")
                self.client_socket.close()
                break
        exit()

    def handle_command(self, message):
        if message["status"] == "check_username_response":
            if message["data"][0]:
                self.frontend.main_widget_signal.emit("DashboardWidget")
                self.send_message_to_server_json({"status": "add_username", "data": message["data"][1]})
            else:
                self.frontend.raise_username_pop_up_signal.emit(message["data"][1])

        elif message["status"] == "actualize_client_list":
            self.frontend.dashboard_window.show_online_clients(message["data"])

        elif message["status"] == "display_initial_photos":
            if not os.path.exists("Imagenes"):
                os.makedirs("Imagenes")
            for i, photo_byte in enumerate(message["data"]):
                with open("Imagenes/image_{}.png".format(i), "wb") as fixed_file:
                    fixed_file.write(photo_byte)
            self.frontend.show_gallery_images_signal.emit()

        elif message["status"] == "start_editing":
            self.frontend.start_editing_signal.emit()

        elif message["status"] == "spectator_mode_pop_up":
            self.frontend.raise_spectator_mode_pop_up_signal.emit()

        elif message["status"] == "actualize_commentaries":
            self.frontend.actualize_commentaries_signal.emit(message["data"])

    def send_message_to_server_json(self, dict_):
        encoded_message = json.dumps(dict_).encode()  # Json
        message_length = len(encoded_message).to_bytes(4, byteorder="big")
        self.client_socket.send(message_length + encoded_message)

    def send_message_to_server_pickle(self, dict_):
        encoded_message = pickle.dumps(dict_)  # Pickle
        message_length = len(encoded_message).to_bytes(4, byteorder="big")
        self.client_socket.send(message_length + encoded_message)

    def end_connection(self):
        print("Connection Ended")
        self.connected = False
        self.client_socket.close()
        exit()


if __name__ == "__main__":

    app = QApplication([])
    client = Client()
    sys.exit(app.exec_())
