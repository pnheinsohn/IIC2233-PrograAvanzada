import os

class BackEnd:

    def __init__(self):
        self.initial_images = []
        self.file_names = []
        self.commentaries = []
        for root, dirs, files in os.walk("Imagenes"):
            for file in files:
                if root == "Imagenes" and file != "comentarios.csv":
                    with open(os.path.join(root, file), "rb") as image:
                        self.initial_images.append([bytearray(image.read()), None])
                        self.file_names.append(file)
                elif file == "comentarios.csv":
                    with open(os.path.join(root, file), "r") as commentaries:
                        pre_commentaries = list(map(lambda row: row.strip("\n").split(";"), commentaries))
                        for file_, commentary in pre_commentaries:
                            self.commentaries.append([file_, commentary.replace("\t", "\n")])

        if not os.path.isfile("Imagenes/comentarios.csv"):
            with open("Imagenes/comentarios.csv", "w", encoding="utf-8") as csv:
                for file in self.file_names:
                    self.commentaries.append([file, ""])
                    csv.write("{};\n".format(file))

    @staticmethod
    def check_username_requirements(username, client_sockets):
        if username.isalnum() and len(username) >= 2 and username not in client_sockets.values():
            return True, username
        elif username in client_sockets.values():
            return False, "Username '{}' is already in use, please choose another one".format(username)
        elif username.isalnum():
            return False, "The minimum username's length must be of 2 characters"
        else:
            return False, "The username must have only alphanumeric characters"

    def available_for_editing(self, index, client_socket):
        if self.initial_images[index][1]:
            return False
        self.initial_images[index][1] = client_socket
        return True

    def save_commentaries(self):
        with open("Imagenes/comentarios.csv", "w", encoding="utf-8") as csv:
            for file_name, commentary in self.commentaries:
                csv.write("{};{}\n".format(file_name, commentary.replace("\n", "\t")))
