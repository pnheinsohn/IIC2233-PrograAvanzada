import unittest
from random import choice
from Consultas import process_query, ascendencia, indice_de_tamano, pariente_de, gemelo_genetico, \
    valor_caracteristica, min, max, prom, check_amount_args, consultas
import Fenotypes as Fen
import Exceptions as Ex
from OpenFilesFunctions import get_all_data, Persona, person


class CheckExceptions(unittest.TestCase):

    def setUp(self):
        self.genomes = open("Testing/genomas.txt", "r", encoding="utf-8")
        self.wrong_genomes = open("Testing/wrong_genomas.txt", "r", encoding="utf-8")
        self.listas = open("Testing/listas.txt", "r", encoding="utf-8")
        self.listas_dict = dict(map(lambda row: (row[:row.index(";")], row[row.index(";") + 2:].strip('\n')),
                                    self.listas))
        self.personas = list(map(lambda row: Persona(**get_all_data(row.strip("\ufeff"), self.listas_dict)),
                                 self.genomes))
        self.wrong_personas = list(map(lambda row: Persona(**get_all_data(row.strip("\ufeff"), self.listas_dict)),
                                   self.wrong_genomes))
        self.correct_asks = [["ascendencia", "Henry Boys"], ["índice_tamaño", "Rick Sánchez"],
                             ["gemelo_genético", "Hakalamax Atalapastruka"], ["pariente_de", "0", "Stephanie Chau"],
                             ["valor_característica", "AAG", "Rick Sánchez"], ["min", "AAG"], ["max", "AAG"],
                             ["prom", "AAG"]]
        self.bad_request_asks = [["pariente de", choice(["-1", "0", "1", "2", "n"]), "Jesús De Nazaret"],
                                 ["valor_caracteristica", "AAG", "Tomas Salvadores"]]

        self.not_acceptable_asks = [["ascendencia", "Frodo Baggins"], ["pariente_de", "0", "Rick Sánchez"]]

        self.correct_one_param_asks = [["ascendencia", "Frodo Baggins"], ["indice_tamaño", "Rick Sánchez"],
                                       ["gemelo_genético", "Hakalamax Atalapastruka"], ["min", "AAG"],
                                       ["max", "AAG"], ["prom", "AAG"]]
        self.correct_two_param_asks = [["pariente_de", choice(["-1", "0", "1", "2", "n"]), "Rick Sánchez"],
                                       ["valor_característica", "AAG", "Tomas Salvadores"]]
        self.not_statistical_tags = ["TAG", "TGG", "CGA"]

    def tearDown(self):
        self.genomes.close()
        self.wrong_genomes.close()
        self.listas.close()

    # Bad Request
    def test_request_bad(self):  # Ask does not exists
        self.assertRaises(Ex.BadRequest, process_query, choice(self.bad_request_asks), self.personas)

    @unittest.expectedFailure
    def test_request_good(self):  # Ask exists
        self.assertRaises(Ex.BadRequest, process_query, choice(self.correct_asks), self.personas)

    # Not Found
    def test_not_found_parameters_exceeded(self):  # Wrong amount of parameters
        self.assertRaises(Ex.NotFound, check_amount_args, 2, choice(self.correct_one_param_asks)[1:])
        self.assertRaises(Ex.NotFound, check_amount_args, 1, choice(self.correct_two_param_asks)[1:])

    def test_not_found_parameters_correct(self):  # Correct amount of parameters
        chosen = choice([choice(self.correct_one_param_asks)[1:], choice(self.correct_two_param_asks)[1:]])
        self.assertIsNone(check_amount_args(len(chosen), chosen))

    def test_not_found_person_name(self):  # Name of person (parameter) does not exist
        self.assertRaises(Ex.NotFound, person, choice(["Hernan Valdivieso", "Rick Sanchez", "Jesús de Nazaret"]),
                          self.personas)

    def test_not_found_tag(self):  # Tag of characteristic (parameter) does not exist
        self.assertRaises(Ex.NotFound, min, self.personas, choice(self.not_statistical_tags))
        self.assertRaises(Ex.NotFound, max, self.personas, choice(self.not_statistical_tags))
        self.assertRaises(Ex.NotFound, prom, self.personas, choice(self.not_statistical_tags))

    # Not Acceptable
    def test_not_acceptable_empty_solution(self):  # Empty Solution
        chosen = choice(self.not_acceptable_asks)
        function = consultas.get(chosen[0])
        self.assertRaises(Ex.NotAcceptable, function, self.personas, *chosen[1:])

    @unittest.expectedFailure
    def test_not_acceptable_found_a_solution(self):  # Found a Solution
        chosen = choice(self.correct_asks)
        function = consultas.get(chosen[0])
        self.assertRaises(Ex.NotAcceptable, function, self.personas, *chosen[1:])

    # Genome Error
    def test_genome_error_space(self):  # Found a space in the genome
        persona = next(filter(lambda per: per.complete_name == "Paul Heinsohn", self.wrong_personas))
        self.assertRaises(Ex.GenomeError, Fen.get_feet_type, persona)

    def test_genome_error_char(self):  # Found a character different from "AGCT" in the genome
        persona = next(filter(lambda per: per.complete_name == "Felipe Dominguez", self.wrong_personas))
        self.assertRaises(Ex.GenomeError, Fen.get_height, persona)

    @unittest.expectedFailure
    def test_genome_error_not_founded(self):  # Found a person without Genome Error
        persona = next(filter(lambda per: per.complete_name == "Rick Sánchez", self.wrong_personas))
        self.assertRaises(Ex.GenomeError, Fen.get_vision_type, persona)

if __name__ == "__main__":

    unittest.main()
