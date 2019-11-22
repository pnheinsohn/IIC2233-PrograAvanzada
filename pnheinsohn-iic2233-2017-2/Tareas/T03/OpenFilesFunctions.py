from collections import namedtuple
import Exceptions as Ex


def get_all_data(row, listas_dict):
    fnum = "".join(row[:2] if row[:2].isnumeric() else "".join(row[0]))
    name = row[len(fnum):int(fnum) + len(fnum)]
    snum = "".join(row[int(fnum) + len(fnum):int(fnum) + 4] if row[int(fnum) + len(fnum):int(fnum) + 4].isnumeric()
                   else "".join(row[int(fnum) + len(fnum):int(fnum) + 3]) if row[int(fnum) + len(fnum):int(fnum) + 3]
                   .isnumeric() else "".join(row[int(fnum) + len(fnum)]))

    last_name = row[int(fnum) + len(snum) + len(fnum):int(snum) + int(fnum) + len(snum) + len(fnum)]
    genotypes = get_genotypes(last_name, row, listas_dict)
    kwargs = {"complete_name": "{} {}".format(name, last_name)}
    kwargs.update(dict((genotypes[i][0], genotypes[i][1]) for i in range(len(genotypes))))
    return kwargs


def get_genotypes(last_name, row, listas_dict):
    ints = list(filter(str.isdigit, row))
    list_of_attributes = []
    if len(last_name) >= 10:
        char = row[row.rfind(last_name) + int(row[row.rfind(last_name) - 2:row.rfind(last_name)]):row.rfind(
            ints[-1]) + 1]
    else:
        char = row[row.rfind(last_name) + int(row[row.rfind(last_name) - 1]):row.rfind(ints[-1]) + 1]
    genome = row[row.find(char) + len(char):]
    slice_attributes(char, list_of_attributes, list(filter(str.isdigit, char)), listas_dict, genome)
    return list_of_attributes


def slice_attributes(char, list_of_attributes, ints, listas_dict, genome):
    if len(char) == 0 or len(ints) == 0:
        return
    if not char[char.find(ints[0]):char.find(ints[0]) + 2].isdigit():
        list_of_attributes.append((char[:3], assign_genomes(char[:4], listas_dict, genome)))
        char = char[4:]
        ints = ints[1:]
    else:
        list_of_attributes.append((char[:3], assign_genomes(char[:5], listas_dict, genome)))
        char = char[5:]
        ints = ints[2:]
    slice_attributes(char, list_of_attributes, ints, listas_dict, genome)


def assign_genomes(char, listas_dict, genome):
    id_to_search = ''.join(s for s in char if s.isdigit())
    list_of_id_positions = listas_dict.get(id_to_search).split(",")
    genotype = [genome[i * 3:i * 3 + 3] for i in range(len(genome)) if str(i) in list_of_id_positions]
    return [elem if check_string(elem) else "Error" for elem in genotype]


def check_string(string):
    search_genome_error = [string for s in string if s not in "ACTG" or s == " "]
    if len(search_genome_error) != 0:
        return False
    return True


def otras_personas(personas, *complete_name):
    return list(filter(lambda person: person.complete_name not in complete_name, personas))


def person(complete_name, personas):
    persona = list(filter(lambda persona: persona.complete_name == complete_name, personas))
    if len(persona) == 0:
        raise Ex.NotFound("Parámetro 'nombre' erroneo")
    return persona[0]

Persona = namedtuple("Persona", ["complete_name", "AAG", "GTC", "GGA", "TCT",
                                 "GTA", "CTC", "CGA", "TGG", "TAG"])
