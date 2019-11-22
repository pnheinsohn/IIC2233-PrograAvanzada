import json
import pickle
import time
import datetime
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from BackEnd import BackEnd
from Variables import *


class Server:

    def __init__(self):
        print("Initializing Server...")
        self.host = HOST
        self.port = PORT
        self.backend = BackEnd()

        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        print("Host and port synchronized")
        self.server_socket.listen()
        print("Server listening in {}:{}".format(self.host, self.port))

        listening_thread = Thread(target=self.accept_connections_thread, daemon=True)
        listening_thread.start()
        print("Server accpeting connections...")

        self.client_sockets = {}

    def accept_connections_thread(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets.update({client_socket: None})

            print("Server connecting {}:{}".format(client_socket, client_address))

            listening_client_thread = Thread(target=self.listen_client_thread, args=(client_socket,), daemon=True)
            listening_client_thread.start()

    def listen_client_thread(self, client_socket):
        while True:
            try:
                response_byte_length = client_socket.recv(4)
                response_length = int.from_bytes(response_byte_length, byteorder="big")

                response = bytearray()
                while len(response) < response_length:
                    response += client_socket.recv(256)

                decoded_message = json.loads(response.decode())  # Json
                self.handle_command(decoded_message, client_socket)
            except UnicodeDecodeError:
                decoded_message = pickle.loads(response)  # Pickle
                self.handle_command(decoded_message, client_socket)
            except ConnectionResetError:
                decoded_message = {"status": "exit_app"}
                self.handle_command(decoded_message, client_socket)
                break

    def actualize_client_list(self):
        for client_socket in self.client_sockets:
            usernames = [self.client_sockets[key] for key in self.client_sockets if self.client_sockets[key]]
            send_dict = {"status": "actualize_client_list", "data": usernames}
            self.send_message_to_client_json(send_dict, client_socket)

    def actualize_commentaries(self):
        for client_socket in self.client_sockets:
            send_dict = {"status": "actualize_commentaries", "data": self.backend.commentaries}
            self.send_message_to_client_json(send_dict, client_socket)

    def handle_command(self, dict_, client_socket):
        if dict_["status"] == "check_username":
            send_dict = {"status": "check_username_response",
                         "data": self.backend.check_username_requirements(dict_["data"], self.client_sockets)}
            self.send_message_to_client_json(send_dict, client_socket)

        elif dict_["status"] == "add_username":
            print("Username '{}' is now taken".format(dict_["data"]))
            self.client_sockets[client_socket] = dict_["data"]
            time.sleep(1)
            self.actualize_client_list()

        elif dict_["status"] == "ask_initial_photos":
            send_dict = {"status": "display_initial_photos", "data": [elem[0] for elem in self.backend.initial_images]}
            self.send_message_to_client_pickle(send_dict, client_socket)

        elif dict_["status"] == "available_for_editing":
            if self.backend.available_for_editing(dict_["data"], client_socket):
                send_dict = {"status": "start_editing"}
                self.send_message_to_client_json(send_dict, client_socket)
            else:
                send_dict = {"status": "spectator_mode_pop_up"}
                self.send_message_to_client_json(send_dict, client_socket)

        elif dict_["status"] == "get_commentaries":
            self.actualize_commentaries()

        elif dict_["status"] == "new_commentary_message":
            self.backend.commentaries[dict_["data"][0]][1] += "({}) {}: {}\n" \
                .format(datetime.datetime.now().strftime("%d/%m/%Y|%H:%M"),
                        self.client_sockets.get(client_socket), dict_["data"][1])
            self.actualize_commentaries()
            self.backend.save_commentaries()

        elif dict_["status"] == "stop_editing":
            self.backend.initial_images[dict_["data"]][1] = None

        elif dict_["status"] == "log_out":
            print("Username '{}' is now available".format(self.client_sockets[client_socket]))
            self.client_sockets[client_socket] = None
            self.actualize_client_list()
            for i in range(len(self.backend.initial_images)):
                if client_socket == self.backend.initial_images[i][1]:
                    self.backend.initial_images[i][1] = None
                    return

        elif dict_["status"] == "exit_app":
            actualize = False
            if self.client_sockets[client_socket]:
                print("Username '{}' is now available".format(self.client_sockets[client_socket]))
                self.client_sockets[client_socket] = None
                actualize = True
            print("Client '{}' has disconnected from server".format(client_socket))
            del self.client_sockets[client_socket]
            if actualize:
                self.actualize_client_list()
                for i in range(len(self.backend.initial_images)):
                    if client_socket == self.backend.initial_images[i][1]:
                        self.backend.initial_images[i][1] = None
                        return

    @staticmethod
    def send_message_to_client_json(dict_, client_socket):
        encoded_message = json.dumps(dict_).encode()
        message_length = len(encoded_message).to_bytes(4, byteorder="big")
        client_socket.send(message_length + encoded_message)

    @staticmethod
    def send_message_to_client_pickle(dict_, client_socket):
        encoded_message = pickle.dumps(dict_)
        message_length = len(encoded_message).to_bytes(4, byteorder="big")
        client_socket.send(message_length + encoded_message)


if __name__ == "__main__":
    server = Server()

    while True:
        pass
