import csv, random
from collections import deque


class Alumno:

    lista_de_alumnos = []

    def __init__(self, num, unidad):
        self.num = num
        self.unidad = unidad
        self.registro_cupos = []
        self.lista_de_alumnos.append(self)
        Alumno.lista_de_alumnos = self.lista_de_alumnos

    def __repr__(self):
        return "Numero de alumno: {}".format(self.num)


class Curso:

    lista_cursos = []
    lista_de_alumnos = []

    def __init__(self, sigla, horario, cupos, cupos2):
        self.sigla = sigla
        self.horario = horario
        self.cupos = cupos
        self.cupos2 = cupos2
        self.stack_cupos = deque([])
        self.get_cupos()
        self.lista_cursos.append(self)
        Curso.lista_cursos = self.lista_cursos

    def get_cupos(self):
        for i in range(int(self.cupos)):
            new_cupo = Cupo(self.sigla, i + 1, self.horario)
            self.stack_cupos.append(new_cupo)

    def get_more_cupos(self):
        stack_cupos = []
        for i in range(self.cupos2):
            new_cupo = Cupo(self.sigla, self.cupos + i + 1, self.horario)
            stack_cupos.append(new_cupo)
        self.stack_cupos.extend(stack_cupos)

    def __repr__(self):
        return self.stack_cupos


class Cupo:

    def __init__(self, sigla, num_cupo, horario):
        self.sigla = sigla
        self.num_cupo = num_cupo
        self.horario = horario

    def __repr__(self):
        return self.sigla + " | " + str(self.num_cupo) + " | " + self.horario


class PrograBanner:

    def __init__(self):
        self.generate_csv('alumnos.txt')
        self.generate_csv('cursos.txt')
        self.unidades = self.generate_csv('unidades.txt')

    def generate_csv(self, string):
        unidades = {}
        with open(string, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=",")
            for row in spamreader:
                if string == "alumnos.txt":
                    Alumno(row[0], row[1])
                elif string == "cursos.txt":
                    Curso(row[0], row[3], row[1], row[2])
                else:
                    unidades[row[0]] = row[1]
        return unidades

    def primera_toma(self):
        random.shuffle(Alumno.lista_de_alumnos)
        for alumno in Alumno.lista_de_alumnos:
            random.shuffle(Curso.lista_cursos)
            for curso in Curso.lista_cursos[:3]:
                if len(curso.stack_cupos) > 0:
                    alumno.registro_cupos.append(curso.stack_cupos.popleft())

    def segunda_toma(self):
        random.shuffle(Alumno.lista_de_alumnos)
        for alumno in Alumno.lista_de_alumnos:
            random.shuffle(Curso.lista_cursos)
            for curso in Curso.lista_cursos:
                verify = len(curso.stack_cupos) > 0 and len(alumno.registro_cupos) < 5
                for cupo in alumno.registro_cupos:
                    if cupo.sigla == curso.sigla:
                        verify = False
                        break
                if verify:
                    alumno.registro_cupos.append(curso.stack_cupos.pop())

    def revision(self):
        for unidad in self.unidades:
            if self.unidades[unidad] == 0:
                continue
            else:
                for alumno in Alumno.lista_de_alumnos:
                    repetidos = []
                    for cupo in alumno.registro_cupos:
                        for otro_cupo in alumno.registro_cupos:
                            if cupo.horario == otro_cupo.horario and cupo not in repetidos and cupo != otro_cupo:
                                repetidos.append(cupo)
                    for ramo in repetidos:
                        if ramo in alumno.registro_cupos:
                            del alumno.registro_cupos[alumno.registro_cupos.index(ramo)]

    def alumno_en_curso(self, num_alumno, sigla):
        for alumno in Alumno.lista_de_alumnos:
            if alumno.num == str(num_alumno):
                for cupo in alumno.registro_cupos:
                    if cupo.sigla == sigla:
                        print(alumno, ", Sigla {}, Cupo {}".format(cupo.sigla, cupo.num_cupo))
                        return
        print("El alumno no esta en este curso")

    def alumnos_en_curso(self, sigla):
        print("En este curso estan:")
        for curso in Curso.lista_cursos:
            if curso.sigla == sigla:
                for alumno in Alumno.lista_de_alumnos:
                    for cupo in alumno.registro_cupos:
                        if cupo.sigla == sigla:
                            print(alumno, ", Cupo {}".format(cupo.num_cupo))

    def cursos_comunes(self, alumno1, alumno2):
        cursos_compartidos = []
        for alumno in Alumno.lista_de_alumnos:
            if alumno.num == str(alumno1):
                for otro_alumno in Alumno.lista_de_alumnos:
                    if otro_alumno == str(alumno2):
                        for cupo in alumno.registro_cupos:
                            for otro_cupo in otro_alumno:
                                if cupo.sigla == otro_cupo.sigla and cupo.sigla not in cursos_compartidos:
                                    cursos_compartidos.append(cupo.sigla)
                                    print("Alumno {} y Alumno {} comparten {} en horarios {} y {} respectivamente"
                                          .format(alumno1, alumno2, cupo.sigla, cupo.horario, otro_cupo.horario))


menu = PrograBanner()
menu.primera_toma()
menu.segunda_toma()
menu.revision()
menu.alumno_en_curso(14631681, "ICS4948")
menu.alumnos_en_curso("ICS4948")
menu.cursos_comunes(14631681, 14631681)
