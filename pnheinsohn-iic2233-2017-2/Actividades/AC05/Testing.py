import unittest
import form


class Testing(unittest.TestCase):

    def SetUp(self):
        self.lista_rut_invalidos = ["19567195-7"]
        self.lista_formato_invalidos = ["19567195 8", "19.567.195-8"]

    def test_verificar_rut(self):
        for rut_invalido in self.lista_rut_invalidos:
            self.assertNotEqual(True, form.register_form.check_rut(rut_invalido))

    def test_formato_rut(self):
        for formato_invalido in self.lista_formato_invalidos:
            self.assertRaises(ValueError, form.register_form.check_rut(formato_invalido))

    @unittest.skip
    def test_datos_guardados(self):
        pass

    @unittest.skip
    def test_registrar_people(self):
        pass

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Testing)
    unittest.TextTestRunner().run(suite)
