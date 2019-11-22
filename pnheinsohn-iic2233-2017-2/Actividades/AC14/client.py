import threading
import socket
import sys
import pickle


class Client:

    def __init__(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.choosing = False
        self.host = "localhost"
        self.port = 8000

        try:
            self.socket_client.connect((self.host, self.port))
            print("Client successfully has connected to {}:{}".format(self.host, self.port))

            self.connected = True

            listen_thread = threading.Thread(target=self.listen_thread, daemon=True)
            listen_thread.start()

        except ConnectionRefusedError:
            print("Connection Ended")
            self.socket_client.close()
            exit()

    def listen_thread(self):
        while self.connected:
            response_byte_length = self.socket_client.recv(4)
            response_length = int.from_bytes(response_byte_length, byteorder="big")

            response = bytearray()

            while len(response) < response_length:
                response += self.socket_client.recv(256)

            decoded = pickle.loads(response)

            self.handle_command(decoded)

    def handle_command(self, message):
        if message["status"] == "actualize_board":
            print("\n{}\n".format(message["data"]))
            self.choosing = True
            self.run()
        elif message["status"] == "show_winner":
            if message["data"]:
                print("\nYou Win!\n")
            else:
                print("\nYo Loose u.u\n")
            self.socket_client.close()
            sys.exit()

    def run(self):
        while self.choosing:
            attack_position = input("Attack Position ('exit' to retreat): ")
            self.choosing = False
            self.send({"status": "attack", "data": attack_position})

    def send(self, message):
        message = pickle.dumps(message)
        message_length = len(message).to_bytes(4, byteorder="big")

        self.socket_client.send(message_length + message)


if __name__ == "__main__":
    client1 = Client()

    while True:
        pass
