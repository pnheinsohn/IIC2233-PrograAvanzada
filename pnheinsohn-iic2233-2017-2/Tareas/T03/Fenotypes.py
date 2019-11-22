import Exceptions as Ex


def get_feet_type(persona):
    if "Error" in persona.CTC:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de pies".format(persona.complete_name),
                             persona.complete_name)
    amounts = persona.CTC.count("GTA"), persona.CTC.count("CCA")
    return percentage(amounts[0], amounts[1]) * 48 + (percentage(amounts[1], amounts[0])) * 34


def get_height(persona):
    if "Error" in persona.AAG:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de altura".format(persona.complete_name),
                             persona.complete_name)
    return percentage_agt_act(persona, "height")[0] * 2.1 + percentage_agt_act(persona, "height")[1] * 1.4


def get_stomach_type(persona):
    if "Error" in persona.TGG:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de estómago".format(persona.complete_name),
                             persona.complete_name)
    gen = percentage_agt_act(persona, "stomach")[1]
    if gen < 0.25:
        return "Guatón Parrillero", 0
    elif gen < 0.5:
        return "Mañana empiezo la dieta", 1
    elif gen < 0.75:
        return "Atleta", 2
    else:
        return "Modelo", 3


def get_skin_color(persona):
    if "Error" in persona.TCT:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de piel".format(persona.complete_name),
                             persona.complete_name)
    amounts = persona.TCT.count("AAT"), persona.TCT.count("GCG")
    gen = percentage(amounts[0], amounts[1])
    if gen < 0.25:
        return "Negro"
    elif gen < 0.5:
        return "Moreno"
    elif gen < 0.75:
        return "Blanco"
    else:
        return "Albino"


def get_eye_color(persona):
    if "Error" in persona.GTC:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de ojos".format(persona.complete_name),
                             persona.complete_name)
    amounts = persona.GTC.count("CCT"), persona.GTC.count("AAT"), persona.GTC.count("CAG")
    if amounts[0] > 0:
        return "Cafes"
    elif amounts[1] > 0:
        return "Azules"
    elif amounts[2] > 0:
        return "Verdes"


def get_hair_color(persona):
    if "Error" in persona.GGA:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de pelo".format(persona.complete_name),
                             persona.complete_name)
    amounts = persona.GGA.count("GTG"), persona.GGA.count("AAT"), persona.GGA.count("CCT")
    if amounts[0] > 0:
        return "Negro"
    elif amounts[1] > 0:
        return "Rubio"
    elif amounts[2] > 0:
        return "Pelirrojo"


def get_nose_type(persona):
    if "Error" in persona.GTA:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de nariz".format(persona.complete_name),
                             persona.complete_name)
    amounts = persona.GTA.count("TCG"), persona.GTA.count("CAG"), persona.GTA.count("TAC")
    if amounts[0] > 0:
        return "Aguileña"
    elif amounts[1] > 0:
        return "Respingada"
    elif amounts[2] > 0:
        return "Recta"
    else:
        return ""


def get_body_hair(persona):
    if "Error" in persona.CGA:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de vello corporal".format(
            persona.complete_name), persona.complete_name)
    amounts = persona.CGA.count("TGC"), persona.CGA.count("GTG"), persona.CGA.count("CCT")
    body_hair = ""
    gen = percentage(amounts[0], amounts[1], amounts[2]), percentage(amounts[1], amounts[0], amounts[2]), \
        percentage(amounts[2], amounts[0], amounts[1])
    if gen[0] >= 0.2:
        body_hair += "Pecho, "
    if gen[1] >= 0.2:
        body_hair += "Axila, "
    if gen[2] >= 0.2:
        body_hair += "Espalda, "
    if len(body_hair) != 0:
        return body_hair[:-2]
    return body_hair


def get_vision_type(persona):
    if "Error" in persona.TAG:
        raise Ex.GenomeError("La persona {} posee un error en su genoma de vision".format(persona.complete_name),
                             persona.complete_name)
    amounts = persona.TAG.count("TTC"), persona.TAG.count("ATT")
    vision = ""
    if amounts[0] == amounts[1] == 0:
        return ""
    if round(percentage(amounts[0], amounts[1]), 3) >= 0.2:
        vision += "Daltonismo, "
    if round(percentage(amounts[1], amounts[0]), 3) >= 0.2:
        vision += "Miopia, "
    if len(vision) != 0:
        return vision[:-2]
    return vision


def percentage_agt_act(persona, char):
    if char == "height":
        amounts = persona.AAG.count("AGT"), persona.AAG.count("ACT")
    else:
        amounts = persona.TGG.count("AGT"), persona.TGG.count("ACT")
    return percentage(amounts[0], amounts[1]), percentage(amounts[1], amounts[0])


def percentage(x, y, z=0):
    if x + y + z == 0:
        return 0
    else:
        return x / (x + y + z)
