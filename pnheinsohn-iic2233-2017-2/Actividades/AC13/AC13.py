import pickle
import json
import os
from random import randint


class Client:

    def __init__(self, nombre, rut, balance, apellido, clave, fecha_nacimiento, numero_cuenta, tipo_cuenta):
        self.nombre = nombre
        self.apellido = apellido
        self.rut = rut
        self.clave = clave
        self.balance = balance
        self.fecha_nacimiento = fecha_nacimiento
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta

    def __getstate__(self):
        dict_ = self.__dict__.copy()
        new_dict = {}
        for keys, values in dict_.items():
            if isinstance(values, str):
                values = cdad(values)
            if isinstance(keys, str):
                keys = cdad(keys)
            new_dict.update({keys: values})
        return new_dict

    def __setstate__(self, state):
        dict_ = {}
        for keys, values in state.items():
            if isinstance(values, str):
                values = anti_cdad(values)
            if isinstance(keys, str):
                keys = anti_cdad(keys)
            dict_.update({keys: values})
        self.__dict__ = dict_


class ClientEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Client):
            return {"nombre": obj.nombre,
                    "apellido": obj.apellido,
                    "rut": obj.rut,
                    "clave": obj.clave,
                    "balance": obj.balance,
                    "fecha nacimiento": obj.fecha_nacimiento,
                    "numero cuenta": obj.numero_cuenta,
                    "tipo cuenta": obj.tipo_cuenta}
        return super().default(obj)


def get_affected_clients():
    with open("ruts_para_leer.txt", "r", encoding="utf-8") as ruts:
        result = []
        for rut in ruts:
            for root, dirs, files in os.walk("base_de_datos_banco"):
                ad = "{}.json".format(rut.strip("\n"))
                for file in files:
                    if file == ad:
                        result.append(os.path.join(root, rut.strip("\n")))
        return result


def json_get_clients(clients):
    clients_ = []
    for client in clients:
        with open("{}.json".format(client, "r")) as c:
            client_atts = json.load(c, object_hook=json_filter_attributes)
            clients_.append(Client(**client_atts))
    return clients_


def json_filter_attributes(dict_obj):
    new_dict = {}
    with open("DocumentacionJSON.json", "r") as relevant_atts:
        atts = json.load(relevant_atts)
        for att in atts:
            att = att.lower()
            if dict_obj.get(att.replace(" ", "_")):
                new_dict.update({att.replace(" ", "_"): dict_obj[att.replace(" ", "_")]})
    return new_dict


def json_save_clients(clients):
    for client in clients:
        with open("bd_json/{}.json".format(client.rut), "w", encoding="utf-8") as data:
            json.dump(client, data, cls=ClientEncoder)


def cdad(string):  # Cifrado de Alfabeto Desplazado
    new_string = ""
    for s in string:
        new_string += chr(ord(s) + 22)
    return new_string


def anti_cdad(string):
    new_string = ""
    for s in string:
        new_string += chr(ord(s) - 22)
    return new_string


def save_encripted_clients(clients):
    for client in clients:
        with open("bd_segura/{}.seguro".format(randint(0, 999999999999999999)), "wb") as data:
            pickle.dump(client, data)


def open_encripted_clients():
    clientes = []
    for root, dirs, files in os.walk("bd_segura"):
        for file in files:
            with open(os.path.join(root, file), "rb") as f:
                client = pickle.load(f)
                clientes.append(client)
    return clientes


if __name__ == "__main__":

    affected_clients = get_affected_clients()
    json_clients = json_get_clients(affected_clients)
    json_save_clients(json_clients)

    save_encripted_clients(json_clients)
    clients = open_encripted_clients()
