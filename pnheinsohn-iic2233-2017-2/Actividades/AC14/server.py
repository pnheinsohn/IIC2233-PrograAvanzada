import socket
import threading
import sys
import pickle
from time import sleep
from battleship import Battleship


class Server:

    def __init__(self):
        self.game = Battleship(loaded=True)

        self.host = "localhost"
        self.port = 8000

        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))
        print("Host and port binded")

        self.socket_server.listen(2)
        print("Server listening in {}:{}".format(self.host, self.port))

        accept_connections = threading.Thread(target=self.accept_connections_thread, daemon=True)
        accept_connections.start()
        print("Server accepting connections")

        self.players = {}
        self.players_sockets = {"player_1": None, "player_2": None}
        self.players_moves = {"player_1": None, "player_2": None}

    def accept_connections_thread(self):
        while True:
            client_socket, _ = self.socket_server.accept()

            if len(self.players) == 0:
                self.players[client_socket] = "player_1"
                self.players_sockets["player_1"] = client_socket
                message = {"status": "actualize_board", "data": self.game.view_from("P1")}
                self.send(message, client_socket)
            elif len(self.players) == 1:
                self.players[client_socket] = "player_2"
                self.players_sockets["player_2"] = client_socket
                message = {"status": "actualize_board", "data": self.game.view_from("P2")}
                self.send(message, client_socket)

            print("Server has connected a new client")

            listen_player_thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket,),
                daemon=True)
            listen_player_thread.start()

            if len(self.players) == 2:
                break

    def listen_client_thread(self, client_socket):
        while True:
            response_byte_length = client_socket.recv(4)
            response_length = int.from_bytes(response_byte_length, byteorder="big")

            response = bytearray()

            while len(response) < response_length:
                response += client_socket.recv(256)

            decoded = pickle.loads(response)

            self.handle_command(decoded, client_socket)

    def handle_command(self, message, client_socket):
        if message["status"] == "attack":
            if message["data"] == "exit":
                print(self.players[client_socket])
                if self.players[client_socket] == "player_1":
                    self.check_winner("P2")
                else:
                    self.check_winner("P1")
                return
            if not self.players_moves[self.players[client_socket]]:
                self.players_moves[self.players[client_socket]] = message["data"]

                if None not in self.players_moves.values():
                    self.play_game()

    def play_game(self):
        player_1 = self.players_moves["player_1"]
        player_2 = self.players_moves["player_2"]

        self.players_moves = {"player_1": None, "player_2": None}

        self.game.attack("P1", player_1)
        self.game.attack("P2", player_2)

        self.send({"status": "actualize_board", "data": self.game.view_from("P1")}, self.players_sockets["player_1"])
        self.send({"status": "actualize_board", "data": self.game.view_from("P2")}, self.players_sockets["player_2"])

        self.check_winner()

    def check_winner(self, winner=None):
        if not winner and self.game.game_over():
            self.send({"status": "show_winner", "data": self.game.get_winner() == "P1"},
                      self.players_sockets["player_1"])
            self.send({"status": "show_winner", "data": self.game.get_winner() == "P2"},
                      self.players_sockets["player_2"])
            self.end_game()
        elif winner == "P1" or winner == "P2":
            self.send({"status": "show_winner", "data": winner == "P1"}, self.players_sockets["player_1"])
            self.send({"status": "show_winner", "data": winner == "P2"}, self.players_sockets["player_2"])
            self.end_game()

    def end_game(self):
        sleep(2)
        self.socket_server.close()
        sys.exit()

    @staticmethod
    def send(message, client_socket):
        encoded_msg = pickle.dumps(message)
        msg_length = len(encoded_msg).to_bytes(4, byteorder="big")
        client_socket.send(msg_length + encoded_msg)


if __name__ == "__main__":
    server = Server()

    while True:
        pass
