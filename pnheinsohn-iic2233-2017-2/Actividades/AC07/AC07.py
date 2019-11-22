import json
import time
import os


stopwords = {'en': ['the', 'a', 'we'], 'es': ['los', 'las', 'él']}
stem = {'Porter': lambda x: x[:2], 'Snowball': lambda x: x[:3]}

##########################################################################

#                   ESCRIBE TUS DECORADORES AQUI

##########################################################################


def verify_types(in_type, out_type):
    def _verify_types(function):
        def __verify_types(*args, **kwargs):
            for i, arg in enumerate(args):
                if i == 0 and not isinstance(arg, in_type):
                    raise TypeError
            if not isinstance(function(*args, **kwargs), out_type):
                raise TypeError
            return function(*args, **kwargs)
        return __verify_types
    return _verify_types


def to_lower_case(function):
    def _to_lower_case(*args, **kwargs):
        list_of_args = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, str):
                arg = arg.lower()
            elif i == 0 and isinstance(arg, list):
                new_args = []
                for arg_ in arg:
                    arg_ = arg_.lower()
                    new_args.append(arg_)
                list_of_args.append(new_args)
                continue
            list_of_args.append(arg)
        return function(*list_of_args, **kwargs)
    return _to_lower_case


def check_file(function):
    def _check_file(*args):
        for i, arg in enumerate(args):
            if i == 0 and os.path.isfile(arg + ".nlp"):
                return function(*args)
    return _check_file


def timer(function):
    def _timer(*args, **kwargs):
        print("Ejecutando Funcion...")
        start = time.time()
        function(*args, **kwargs)
        print("Tiempo tardado: {}".format((time.time() - start)))
        return function(*args, **kwargs)
    return _timer


def remove_special_characters(function):
    def _remove_special_characters(*args, **kwargs):
        list_of_args = []
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, str):
                string = ""
                for letra in arg:
                    if letra.isalnum() or letra == " ":
                        string += letra
                list_of_args.append(string)
            elif i == 0 and isinstance(arg, list):
                new_arg = []
                for arg_ in arg:
                    string = ""
                    for letra in arg_:
                        if letra.isalnum() or letra == " ":
                            string += letra
                    new_arg.append(string)
                list_of_args.append(new_arg)
        return function(*list_of_args, **kwargs)
    return _remove_special_characters


def get_stats(function):
    def _get_stats(*args, **kwargs):
        for i, arg in enumerate(args):
            if i == 0 and isinstance(arg, str):
                print("Input Length: {}".format(len(arg)))
            elif i == 0 and isinstance(arg, list):
                numero = 0
                for arg_ in arg:
                    numero += len(arg_)
                print("Input Length: {}".format(numero))
        if isinstance(function(*args, **kwargs), str):
            print("Output Length: {}".format(len(function(*args, **kwargs))))
        if isinstance(function(*args, **kwargs), list):
            numero = 0
            for arg_ in function(*args, **kwargs):
                numero += len(arg_)
            print("Output Length: {}".format(numero))
        return function(*args, **kwargs)
    return _get_stats


def logging(name_func):
    def _logging(function):
        def __logging(*args, **kwargs):
            if os.path.isfile("log.txt"):
                s = "a"
            else:
                s = "w"
            final_string = ""
            with open("log.txt", s, encoding="utf-8") as file:
                final_string += name_func + "\nArgs: "
                for arg in args:
                    final_string += "{}, ".format(arg)
                final_string += "\nKwargs: "
                for key in kwargs:
                    final_string += "{}: {}".format(key, kwargs.get(key))
                final_string += "\nOutput: "
                final_string += "{}".format(function(*args, **kwargs))
                file.write(final_string + "\n\n")
            return function(*args, **kwargs)
        return __logging
    return _logging


##########################################################################

#                       CODIGO A DECORAR

##########################################################################

@logging("tokenize")
@timer
@verify_types(str, list)
def tokenize(text, sep, ngrams=1):
    text_splitted = text.split(sep)
    if ngrams == 1:
        return text_splitted

    text_splitted_ngrams = []
    number_of_tokens = int(len(text_splitted)/ngrams) + 1
    for token in range(number_of_tokens):
        text_splitted_ngrams.append(sep.join(text_splitted[token*ngrams:token*ngrams + ngrams]))
    return text_splitted_ngrams


@logging("remove_stopwords")
@get_stats
@remove_special_characters
@timer
@verify_types(list, list)
@to_lower_case
def remove_stopwords(text, language='es'):
    return list(filter(lambda token: token not in stopwords[language], text))


@logging("apply_stem")
@get_stats
def apply_stem(text, type_='Porter'):
    return list(map(stem[type_], text))


@timer
def save(text, filename, **kwargs):
    with open(filename + '.nlp', 'w+') as file:
        content = {'text': text}
        content.update(kwargs)
        json.dump(content, file)


@timer
@check_file
def read(filename):
    with open(filename + '.nlp', 'r') as file:
        content = json.load(file)
    text = content['text']
    del content['text']
    return text, content

    
if __name__ == "__main__":
    try:
        archivo = read("archivo")
    except FileNotFoundError as err:
        print("Esto no es un archivo")

    eng = read("ingles")
    esp = read("español")

    print("Esto son los datos sin procesar como lista")
    list_ = tokenize(esp[0], " ", 1)
    print(list_)
    print(tokenize(eng[0], " ", 2))

    print("--------------------------------------\n")
    
    print("Probado stem")

    print(apply_stem(list_, type_='Porter'))
    print(apply_stem(list_, type_='Snowball'))

    print("--------------------------------------\n")

    print(" Ahora le quitaremos las palabras extra")

    lists = tokenize(esp[0], ' ', 1)
    lists = remove_stopwords(lists, language='es')

    liste = tokenize(eng[0], ' ', 1)
    liste = remove_stopwords(liste, language='en')

    string = " ".join(liste) + " : " + " ".join(lists)
    save(string, "resultados", iluminador="Hernan")
