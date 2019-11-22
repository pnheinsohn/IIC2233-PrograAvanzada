class BadRequest(TypeError):

    def __init__(self, comando):

        self.comando = comando
        self.nombre = 'Error de Consulta'
        super().__init__()

    def __str__(self):
        return "{}: {}".format(self.nombre, self.comando)


class NotFound(TypeError):

    def __init__(self, comando):

        self.comando = comando
        self.nombre = 'Error de Parámetros'
        super().__init__()

    def __str__(self):
        return "{}: {}".format(self.nombre, self.comando)


class NotAcceptable(ReferenceError):

    def __init__(self, comando):
        self.comando = comando
        self.nombre = 'Error de Resultado'
        super().__init__()

    def __str__(self):
        return "{}: {}".format(self.nombre, self.comando)


class GenomeError(SyntaxError):

    def __init__(self, comando, persona_errada):
        self.comando = comando
        self.nombre = 'Error de Genoma'
        self.persona_errada = persona_errada
        super().__init__()

    def __str__(self):
        return "{}: {}".format(self.nombre, self.comando)
