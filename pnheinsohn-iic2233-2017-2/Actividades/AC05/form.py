import os.path


class FormRegister:
    def __init__(self):
        """
        NO TOCAR el init
        """
        self.courses = {
            "IIC1103": [0, 0, 0],  # IIC1103 tiene 2 secciones
            "IIC2233": [0, 0, 0, 0],  # IIC2233 tiene 3 secciones
            "IIC2115": [0, 0],  # IIC2115 tiene 1 seccion
            "IIE3115": [0, 0],  # IIC2115 tiene 1 seccion
            "IIC2332": [0, 0],  # IIC2115 tiene 1 seccion
            "IIC2515": [0, 0]  # IIC2115 tiene 1 seccion
        }

        self.register_list = []  # Almacena los alumnos que se inscribieron con exito

    def check_rut(self, rut):
            if rut.find(".") != -1 or rut.find(" ") != -1:
                raise ValueError("Se ha encontrado un caracter invalido en el input")
            elif rut.find("-") != -1:
                digits, checker = rut.split("-")
                if not digits.isdigit():
                    raise TypeError("No se ingresaron digitos antes del guion")
                digits = list(digits)

                for i in range(len(digits)):
                    digits[i] = int(digits[i])

                list_number = [2, 3, 4, 5, 6, 7, 2, 3, 4, 5]

                digits.reverse()
                total = 0
                for i in range(len(digits)):
                    total += digits[i] * list_number[i]

                rest = 11 - total % 11
                if rest == 11:
                    rest = "0"
                elif rest == 10:
                    rest = "k"
                else:
                    rest = str(rest)
                return rest == checker
            else:
                raise ValueError("No hay 'guion' en el rut")

    def add_course(self, course, section):
        if course.find(" ") != -1:
            raise TypeError("Se ha encontrado un caracter invalido en el input")
        elif course not in self.courses.keys():
            raise KeyError("Sigla ingresada no encontrada")
        if not section.isdigit():
            raise TypeError("Seccion no es un digito valido")
        elif int(section) >= len(self.courses[course]):
            raise IndexError("Seccion no encontrada")
        self.courses[course][int(section)] += 1

    def register_people_info(self, student_name, gender, comment):
        self.register_list.append([student_name, gender, comment])

    def save_data(self, path):
        if os.path.isfile(path):
            raise IOError("Archivo ya existe")
        with open(path, "w") as file:
            for register in self.register_list:
                text = "Student: {}\nGender: {}\nComment: {}\n".format(*register)
                file.write(text + "#"*40 + "\n")

            print("Informacion guardada con exito")
