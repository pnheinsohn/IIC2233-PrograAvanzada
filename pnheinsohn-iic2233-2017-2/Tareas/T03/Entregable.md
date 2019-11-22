################
## Entregable ##
################

## Asignar tags a personas: ##

- Esta seguidilla de métodos ya está implementada a su cabalidad mediante una lista de namedtuples del tipo de persona, cuyos atributos son: "nombre", "apellido", "altura", 
  "color de cabello", "color de ojos", "color de piel", "tipo nariz", "tipo de pies", "vello corporal", "tamaño estomago" y "vision", en donde las últimas 9 características
  son listas con los genes respectivos.
- Para lograr lo anterior, se realiza lo siguiente: personas = [Persona(*OpenFilesFunctions.get_all_data(row)) for row in file], siendo file el archivo genomas.txt. 
  "OpenFilesFunctions" es un módulo de python que contiene el método get_all_data(string), cuya mision es entregar una tupla de la forma (nombre, apellido, *genotypos).
- Para el nombre, simplemente se verificó si los primeros 2 substrings son digitos para obtener el nombre, o bien, si solo el primer substring cumplía lo anterior. Lo mismo
  para el apellido. Cabe destacar que no fue necesario el uso de funciones generadoras ni nada por el estilo, solo slicing de strings con "len" y "rfind".
- Sin embargo, para el caso de los genomas fue distinto, si bien para obtener lo restante del "header" también se empleó slicing, se procedió al uso de una funcion recursiva
  para ir agregando el tipo de dato + su id en una lista de la siguiente forma: [AAT3, CCT4, etc] obtenida a través de a otro metodo que obtiene los substrings numéricos 
  (list_of_id_positions) que servirá para encontrar los tags del "data" mediante una lista compresiva: 
  				
					genotype: [genome[i * 3: i * 3 + 3] for i in range(len(genome)) if str(i) in list_of_id_positions]

  siendo genome el string del "data", y así (recursivamente) se va agregando en una lista ordenada ([genoma_altura, genoma_pelo, etc]) que será parte del return de
  "get_all_data".
- Mas o menos es eso, principalmente uso de slicing y generadores/listas compresivas para "recorrer" listas y tuplas, y el pequeño uso de filter para obtener los números 
  dentro de strings ('list(filter(str.isdigit, second_part_of_header))').
- Adjuntaré parte del módulo de estas funciones (No fijarse en el uso de excepciones, esta en trabajo aun):
###########################################################################################################
def get_all_data(row):
    if row[:2].isdigit():  # Si el nombre tiene un len >= 10
        name = row[2:int(row[:2]) + 2]
    elif row[0].isdigit():  # Si el nombre tiene un len < 10
        name = row[1:int(row[0]) + 1]
    else:
        raise TypeError 
    last_name = get_last_name(name, row)
    genotypes = get_genotypes(last_name, row)
    return (name, last_name, *genotypes)


def get_last_name(name, row):
    if len(name) >= 10:
        if row[int(row[:2]) + 2:int(row[:2]) + 4].isdigit():  # Si el apellido tiene un len >= 10
            last_name = row[int(row[:2]) + 4:int(row[:2]) + 4 + int(row[int(row[:2]) + 2:int(row[:2]) + 4])]
        elif row[int(row[:2]) + 2].isdigit():  # Si el apellido tiene un len < 10
            last_name = row[int(row[:2]) + 3:int(row[:2]) + 3 + int(row[int(row[:2]) + 2])]
        else:
            raise ex.TypeError("No Int Value For Last Name")
    else:
        if row[int(row[0]) + 1:int(row[0]) + 3].isdigit():  # Si el apellido tiene un len >= 10
            last_name = row[int(row[0]) + 3:int(row[0]) + 3 + int(row[int(row[0]) + 1:int(row[0]) + 3])]
        elif row[int(row[0]) + 1].isdigit():  # Si el apellido tiene un len < 10
            last_name = row[int(row[0]) + 2:int(row[0]) + 2 + int(row[int(row[0]) + 1])]
        else:
            raise ex.TypeError("No Int Value For Last Name")
    return last_name


def get_genotypes(last_name, row):
    ints = list(filter(str.isdigit, row))
    list_of_attributes = []
    if len(last_name) >= 10:
        char = row[row.rfind(last_name) + int(row[row.rfind(last_name) - 2:row.rfind(last_name)]):row.rfind(
            ints[len(ints) - 1]) + 1]
    else:
        char = row[row.rfind(last_name) + int(row[row.rfind(last_name) - 1]):row.rfind(ints[len(ints) - 1]) + 1]
    genome = row[row.find(char) + len(char):]
    slice_attributes(char, list_of_attributes, list(filter(str.isdigit, char)), genome)
    return list_of_attributes


def slice_attributes(char, list_of_attributes, ints, genome):
    if len(char) == 0 or len(ints) == 0:
        return
    if not char[char.find(ints[0]):char.find(ints[0]) + 2].isdigit():
        list_of_attributes.append(assign_genomes(char[:4], genome))
        char = char[4:]
        ints = ints[1:]
    else:
        list_of_attributes.append(assign_genomes(char[:5], genome))
        char = char[5:]
        ints = ints[2:]
    slice_attributes(char, list_of_attributes, ints, genome)


def assign_genomes(char, genome):
    id_to_search = ''.join(s for s in char if s.isdigit())
    list_of_id_positions = listas_dict.get(id_to_search).split(",")
    genotype = [genome[i * 3:i * 3 + 3] for i in range(len(genome)) if str(i) in list_of_id_positions]
    return genotype
######################################################################################################
## Sobre el uso de 'built-ins' ##
- listas compresivas: cada vez que requiera guardar elementos en alguna lista, o bien, cuando requiera de su uso para emplementar el booleano "in" para un generador.
- funciones generadoras: llamese a estas aquellas que usan el comando "yield", aun no le veo un correcto uso, por lo que no están consideradas por el momento.
- filter: practicamente para todas las consultas, cada vez que quiera realizar alguna consulta respecto a una persona se usara filter acompañado de lambda.
- map: lo mismo que filter, pero la diferencia es que será usado cuando quiera generar un iterable de algun atributo del namedtuple Persona.
- reduce: para todas las estadísitcas a realizar en las consultas.

## Sobre las consultas ##
- resulta imposible que defina todas las funciones atomizadas para ambas consultas dado el enfoque que le he otorgado a la tarea hasta el minuto (relacionar los archivos
  para asignar correctamente los datos, el manejo de excepciones y un poco de testing para lo anterior). Luego solo entregaré una idea general de lo pedido, nombrando
  las siguientes funciones que ya de por su nombre explican lo que hacen:
  1. Para ascendencia(persona):
     ascendencias = []
     ascendencias.append("Albino") if check_if_is_albino(persona)
     ascendecias.append(check_other_ascendencia(persona)) if check_other_ascendencia(persona) != None
     if ascendencias:
         go_to_string = '-'.join(ascendencia for ascendencia in ascendencias)
         return go_to_string
     else:
         return "No hay ascendencia reconocible"
  
  2. Para pariente_de(grado, persona): producto al tiempo, no me será posible hacer más alla que explicar lo siguiente:
     - Dado el tipo de grado, tener un metodo que retorne las restricciones necesarias a cumplir para que se cumpla dicho grado, luego para cada persona distinta a la
       persona a evaluar, verificar mediante filters y maps si las condiciones para cada característica, en donde si se llegaran a cumplir, dicha persona se va agregando a
       una lista compresiva que almacenará dicha persona. Finalmente, imprimir todas las personas que cumplen las condiciones en caso de que la lista no sea nula.
