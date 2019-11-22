from collections import Counter
from functools import reduce
import Exceptions as Ex
import Fenotypes as Fen
from OpenFilesFunctions import person, otras_personas


# Receiver
def process_query(consulta, personas):
    try:
        if consulta[0] not in consultas:
            raise Ex.BadRequest("Consulta {} no disponible".format(consulta[0]))
        return "---------------- Consulta N°" + str(consultas.get(consulta[0])(personas, *consulta[1:])) + "\n"
    except Ex.NotFound as err1:
        print(err1)
        return "---------------- Consulta N°{} ----------------\n{}\n".format(next(num_request), err1.comando)
    except Ex.NotAcceptable as err2:
        print(err2)
        return "---------------- Consulta N°{} ----------------\n{}\n".format(next(num_request), err2.comando)
    except Ex.GenomeError as err3:
        print(err3)
        return "---------------- Consulta N°{} ----------------\n{}\n".format(next(num_request), err3.comando)


# Consultas
def ascendencia(personas, *args):  # args[0] = complete_name
    check_amount_args(1, args)
    ascendencias = get_ascendencia(person(args[0], personas))
    return "{} ----------------\n{}".format(next(num_request), ascendencias)


def indice_de_tamano(personas, *args):  # args[0] = complete_name
    check_amount_args(1, args)
    persona = person(args[0], personas)
    percentage_agt_act_height = Fen.percentage_agt_act(persona, "height")[0]
    percentage_agt_act_stomach = Fen.percentage_agt_act(persona, "stomach")[0]
    return "{} ----------------\nIndice de tamaño de {}: {}".format(
        next(num_request), args[0], (percentage_agt_act_height * percentage_agt_act_stomach) ** (1 / 2))


def pariente_de(personas, *args):  # args[0] = grado, args[1] = complete_name
    check_amount_args(2, args)
    persona = person(args[1], personas)
    return get_pariente_de(args[0], persona, personas)


def gemelo_genetico(personas, *args):  # args[0] = complete_name
    check_amount_args(1, args)
    persona = person(args[0], personas)
    return get_gemelo_genetico(persona, personas)


def valor_caracteristica(personas, *args):  # args[0] = tag_identificador, args[1] = complete_name
    check_amount_args(2, args)
    if not caracteristicas.get(args[0]):
        Ex.NotFound("Parámetro 'tag característica' erroneo")
    char = caracteristicas.get(args[0])(person(args[1], personas))
    if isinstance(char, tuple):
        char = char[0]
    return "{} ----------------\nValor de la característica {} de {}:\n{}".format(next(num_request), args[0], args[1],
                                                                                  char)


def min(personas, *args):  # args[0] = tag_característica
    check_amount_args(1, args)
    if not (args[0] == "AAG" or args[0] == "CTC" or args[0] == "GTC" or args[0] == "GGA" or args[0] == "TCT"
            or args[0] == "GTA"):
        raise Ex.NotFound("Parámetro 'tag característica' erroneo")
    return "{} ----------------\nMínimo de {}:\n{}".format(next(num_request), args[0],
                                                           least_common(valor_caracteristicas_totales(personas,
                                                                                                      args[0])))


def max(personas, *args):  # args[0] = tag_característica
    check_amount_args(1, args)
    if not (args[0] == "AAG" or args[0] == "CTC" or args[0] == "GTC" or args[0] == "GGA" or args[0] == "TCT"
            or args[0] == "GTA"):
        raise Ex.NotFound("Parámetro 'tag característica' erroneo")
    return "{} ----------------\nMáximo de {}:\n{}".format(next(num_request), args[0],
                                                           most_common(valor_caracteristicas_totales(personas,
                                                                                                     args[0])))


def prom(personas, *args):  # args[0] = tag_característica
    check_amount_args(1, args)
    if not (args[0] == "AAG" or args[0] == "CTC"):
        raise Ex.NotFound("Parámetro 'tag_característica' erroneo")
    valores = list(valor_caracteristicas_totales(personas, args[0]))
    return "{} ----------------\nPromedio de {}:\n{}".format(next(num_request), args[0],
                                                             reduce(lambda x, y: x + y, valores) / len(valores))


# Funciones Aparte
def number():
    numero = 1
    while True:
        yield numero
        numero += 1


def check_amount_args(number, args):
    if len(args) != number:
        raise Ex.NotFound("Cantidad de parámetros incorrecta")


def get_ascendencia(persona):
    ascendencias = ""
    cn = persona.complete_name
    if "AAT" in persona.GTC and "AAT" in persona.GGA and "AAT" in persona.TCT:
        ascendencias += "Albina, "
    if Fen.get_hair_color(persona) == "Negro" and "Pecho" in Fen.get_body_hair(persona) \
            and Fen.get_nose_type(persona) == "Recta":
        ascendencias += "Mediterránea, "
    if Fen.get_hair_color(persona) == Fen.get_skin_color(persona) == "Negro" and Fen.get_feet_type(persona) > 44:
        ascendencias += "Africana, "
    if Fen.get_stomach_type(persona)[0] == "Guatón Parrillero" and "Espalda" in Fen.get_body_hair(persona):
        ascendencias += "Estadounidense, "
    if len(ascendencias) == 0:
        raise Ex.NotAcceptable("Ascendencia no encontrada")
    else:
        return "Ascendencias de {}:\n{}".format(cn, ascendencias[:-2])


def get_pariente_de(grado, persona, personas):
    try:
        parientes = parentesco.get(str(grado))(persona, personas)
    except TypeError:
        raise Ex.NotFound("Grado de parentezco inválido")
    else:
        return "{} ----------------\n{}".format(next(num_request), parientes)


def no_likehood(persona, personas):
    first_filter = filter(lambda p: Fen.get_eye_color(p) != Fen.get_eye_color(persona),
                          filter(lambda p: Fen.get_height(persona) != Fen.get_height(p),
                                 otras_personas(personas, persona.complete_name)))
    personas_name = list(map(lambda p: p.complete_name, filter(
        lambda p: Fen.get_vision_type(p) != Fen.get_vision_type(persona),
        filter(lambda p: Fen.get_feet_type(p) != Fen.get_feet_type(persona),
               filter(lambda p: Fen.get_nose_type(p) != Fen.get_nose_type(persona),
                      filter(lambda p: Fen.get_body_hair(p) != Fen.get_body_hair(persona),
                             filter(lambda p: Fen.get_stomach_type(p) != Fen.get_stomach_type(persona),
                                    filter(lambda p: Fen.get_skin_color(p) != Fen.get_skin_color(persona),
                                           filter(lambda p: Fen.get_hair_color(p) != Fen.get_hair_color(persona),
                                                  first_filter)))))))))
    if len(personas_name) == 0:
        raise Ex.NotAcceptable("No hay personas totalmente distintas a {}".format(persona.complete_name))
    return "Personas totalmente distinto a {}:\n{}".format(persona.complete_name, ",\n".join(personas_name))


def identical_likehood(persona, personas):
    first_filter = filter(lambda p: Fen.get_stomach_type(p) == Fen.get_stomach_type(persona),
                          filter(lambda p: Fen.get_skin_color(p) == Fen.get_skin_color(persona),
                                 filter(lambda p: Fen.get_hair_color(p) == Fen.get_hair_color(persona),
                                        filter(lambda p: Fen.get_eye_color(p) == Fen.get_eye_color(persona),
                                               filter(lambda p: Fen.get_height(p) == Fen.get_height(persona),
                                                      otras_personas(personas, persona.complete_name))))))
    personas_name = list(map(lambda p: p.complete_name,
                             filter(lambda p: Fen.get_vision_type(p) == Fen.get_vision_type(persona),
                                    filter(lambda p: Fen.get_feet_type(p) == Fen.get_feet_type(persona),
                                           filter(lambda p: Fen.get_nose_type(p) == Fen.get_nose_type(persona),
                                                  filter(lambda p: Fen.get_body_hair(p) == Fen.get_body_hair(
                                                      persona), first_filter))))))
    if len(personas_name) == 0:
        raise Ex.NotAcceptable("No hay personas totalmente iguales a {}".format(persona.complete_name))
    return "Personas totalmente iguales a {}:\n{}".format(persona.complete_name, ",\n".join(personas_name))


def like_likehood(persona, personas):
    first_filter = filter(lambda p: Fen.get_skin_color(p) == Fen.get_skin_color(persona),
                          filter(lambda p: Fen.get_hair_color(p) == Fen.get_hair_color(persona),
                                 filter(lambda p: Fen.get_hair_color(p) == Fen.get_hair_color(persona),
                                        filter(lambda p: Fen.get_eye_color(p) == Fen.get_eye_color(persona),
                                               filter(lambda p: abs(Fen.get_height(p) - Fen.get_height(
                                                   persona)) <= 0.2, otras_personas(personas,
                                                                                    persona.complete_name))))))
    personas_name = list(map(lambda p: p.complete_name,
                             filter(lambda p: Fen.get_vision_type(p) == Fen.get_vision_type(persona),
                                    filter(lambda p: abs(Fen.get_feet_type(p) - Fen.get_feet_type(persona)) <= 2,
                                           filter(lambda p: Fen.get_nose_type(p) == Fen.get_nose_type(persona),
                                                  first_filter)))))
    if len(personas_name) == 0:
        raise Ex.NotAcceptable("No hay parientes de grado 1 de {}".format(persona.complete_name))
    return "Parientes grado 1 de {}:\n{}".format(persona.complete_name, ",\n".join(personas_name))


def slike_likehood(persona, personas):
    first_filter = filter(lambda p: Fen.get_vision_type(p) == Fen.get_vision_type(persona),
                          filter(lambda p: abs(Fen.get_height(p) - Fen.get_height(persona)) <= 0.5,
                                 otras_personas(personas, persona.complete_name)))
    personas_name = list(map(lambda p: p.complete_name,
                             filter(lambda p: abs(Fen.get_feet_type(p) - Fen.get_feet_type(persona)) <= 4,
                                    filter(lambda p: Fen.get_skin_color(p) == Fen.get_skin_color(persona),
                                           filter(lambda p: Fen.get_hair_color(p) == Fen.get_hair_color(persona),
                                                  first_filter)))))
    if len(personas_name) == 0:
        raise Ex.NotAcceptable("No hay parientes de grado 2 de {}".format(persona.complete_name))
    return "Parientes grado 2 de {}:\n{}".format(persona.complete_name, ",\n".join(personas_name))


def nlike_likehood(persona, personas):
    first_filter = filter(lambda p: abs(Fen.get_stomach_type(p)[1] - Fen.get_stomach_type(persona)[1]) <= 1,
                          otras_personas(personas, persona.complete_name))
    personas_name = list(map(lambda p: p.complete_name,
                             filter(lambda p: abs(Fen.get_feet_type(p) - Fen.get_feet_type(persona)) <= 6,
                                    filter(lambda p: Fen.get_skin_color(p) == Fen.get_skin_color(persona),
                                           filter(lambda p: abs(Fen.get_height(p) - Fen.get_height(persona)) <= 0.7,
                                                  first_filter)))))
    if len(personas_name) == 0:
        raise Ex.NotAcceptable("No hay parientes de grado n de {}".format(persona.complete_name))
    return "Parientes grado n de {}:\n{}".format(persona.complete_name, ",\n".join(personas_name))


def get_gemelo_genetico(persona, personas):
    otras_persons = list(otras_personas(personas, persona.complete_name))
    counters_char = get_counters_chars(persona, otras_persons)
    total_counters = [counters_char[0][i][1] + counters_char[1][i][1] + counters_char[2][i][1] +
                      counters_char[3][i][1] + counters_char[4][i][1] + counters_char[5][i][1] +
                      counters_char[6][i][1] + counters_char[7][i][1] + counters_char[8][i][1]
                      for i in range(len(otras_persons))]
    return "{} ----------------\nGemelo genético de {}:\n{}".\
        format(next(num_request), persona.complete_name, otras_persons[total_counters.index(sorted(total_counters)[-1])]
               .complete_name)


def get_counters_chars(persona, otras_persons):
    if "Error" in persona.AAG or "Error" in persona.GGA or "Error" in persona.TCT or "Error" in persona.CGA \
            or "Error" in persona.TAG or "Error" in persona.GTC or "Error" in persona.CTC \
            or "Error" in persona.TGG or "Error" in persona.GTA:
        raise Ex.GenomeError("La persona {} posee un error en su genoma".format(persona.complete_name),
                             persona.complete_name)
    counters_height = [compare_adn_char(per, persona.AAG.copy(), per.AAG.copy()) for per in otras_persons]
    counters_eyes = [compare_adn_char(per, persona.GTC.copy(), per.GTC.copy()) for per in otras_persons]
    counters_hair = [compare_adn_char(per, persona.GGA.copy(), per.GGA.copy()) for per in otras_persons]
    counters_skin = [compare_adn_char(per, persona.TCT.copy(), per.TCT.copy()) for per in otras_persons]
    counters_nose = [compare_adn_char(per, persona.GTA.copy(), per.GTA.copy()) for per in otras_persons]
    counters_feet = [compare_adn_char(per, persona.CTC.copy(), per.CTC.copy()) for per in otras_persons]
    counters_body_hair = [compare_adn_char(per, persona.CGA.copy(), per.CGA.copy()) for per in otras_persons]
    counters_stomach = [compare_adn_char(per, persona.TGG.copy(), per.TGG.copy()) for per in otras_persons]
    counters_vision = [compare_adn_char(per, persona.TAG.copy(), per.TAG.copy()) for per in otras_persons]
    return counters_height, counters_eyes, counters_hair, counters_skin, counters_nose, \
        counters_feet, counters_body_hair, counters_stomach, counters_vision


def go_adn_comparison(person_char, other_person_char, number):
    if len(person_char) == 0 or len(other_person_char) == 0:
        return number
    if person_char[0] in other_person_char:
        other_person_char.pop(other_person_char.index(person_char[0]))
        person_char.pop(0)
        number += 1
        return go_adn_comparison(person_char, other_person_char, number)
    return number


def compare_adn_char(other_person, person_char, other_person_char):
    number = 0
    number = go_adn_comparison(person_char, other_person_char, number)
    return other_person.complete_name, number


def valor_caracteristicas_totales(personas, tag_caracteristica, *personas_cn):
    return map(lambda persona: caracteristicas.get(tag_caracteristica)(persona), otras_personas(personas,
                                                                                                personas_cn))


def most_common(list):
    return Counter(list).most_common()[0][0]


def least_common(list):
    return Counter(list).most_common()[-1][0]


num_request = number()
consultas = {"ascendencia": ascendencia, "pariente_de": pariente_de, "gemelo_genético": gemelo_genetico,
             "valor_característica": valor_caracteristica, "índice_tamaño": indice_de_tamano, "min": min, "max": max,
             "prom": prom}
parentesco = {"-1": no_likehood, "0": identical_likehood, "1": like_likehood, "2": slike_likehood, "n": nlike_likehood}
caracteristicas = {"AAG": Fen.get_height, "GTC": Fen.get_eye_color, "GGA": Fen.get_hair_color,
                   "TCT": Fen.get_skin_color, "GTA": Fen.get_nose_type, "CTC": Fen.get_feet_type,
                   "CGA": Fen.get_body_hair, "TGG": Fen.get_stomach_type, "TAG": Fen.get_vision_type}
