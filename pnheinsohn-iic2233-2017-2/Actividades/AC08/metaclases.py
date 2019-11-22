from functions import chess_valid_move

def decorador_meta_init(funcion):
    def _decorador_meta_init(self, *args):
        instancia = funcion(self)
        if len(args) == 0 or instancia == None:
            return
    return _decorador_meta_init



class MetaChess(type):

    instancia = None
    piezas = False

    def __new__(meta, name, base, cls_dict):
        funcion = cls_dict.get("__init__")
        cls_dict["__init__"] = decorador_meta_init(funcion)
        cls_dict["valid_move"] = chess_valid_move
        return super().__new__(meta, name, base, cls_dict)

    def __call__(cls, *args, **kwargs):
        if len(args) == 0:
            return MetaChess.instancia

        if MetaChess.instancia == None:
            MetaChess.instancia = super().__call__(*args, **kwargs)

        if not MetaChess.piezas and len(args) != 0:
            for arg in args:
                MetaChess.instancia.add_piece(arg)
            MetaChess.piezas = True
        return MetaChess.instancia

class MetaPiece(type):

    dic_true = {"Peon": 8, "Alfil": 2, "Torre": 2, "Caballo": 2, "Rey": 1, "Reina": 1}
    dic_false = {"Peon": 8, "Alfil": 2, "Torre": 2, "Caballo": 2, "Rey": 1, "Reina": 1}

    def __call__(cls, *args, **kwargs):
        instancia = super().__call__(*args, **kwargs)
        if instancia.allied:
            diccionario = MetaPiece.dic_true
        else:
            diccionario = MetaPiece.dic_false

        if cls.__name__ == "Peon" and diccionario["Peon"] != 0:
            diccionario["Peon"] -= 1
            return instancia
        elif cls.__name__ == "Torre" and diccionario["Torre"] != 0:
            diccionario["Torre"] -= 1
            return instancia
        elif cls.__name__ == "Alfil" and diccionario["Alfil"] != 0:
            diccionario["Alfil"] -= 1
            return instancia
        elif cls.__name__ == "Caballo" and diccionario["Caballo"] != 0:
            diccionario["Caballo"] -= 1
            return instancia
        elif cls.__name__ == "Rey" and diccionario["Rey"] != 0:
            diccionario["Rey"] -= 1
            return instancia
        elif cls.__name__ == "Reina" and diccionario["Reina"] != 0:
            diccionario["Reina"] -= 1
            return instancia
        else:
            return super().__init__(*args, **kwargs)
