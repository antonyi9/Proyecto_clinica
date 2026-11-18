
class Persona:
    def __init__(self, codigo, nombres, apellidos):
        self.__codigo = codigo
        self.__nombres = nombres
        self.__apellidos = apellidos

    def obtenerCodigo(self):
        return self.__codigo

    def obtenerNombres(self):
        return self.__nombres

    def obtenerApellidos(self):
        return self.__apellidos

    def actualizarDatos(self, nombres, apellidos):
        self.__nombres = nombres
        self.__apellidos = apellidos

    def mostrarDatos(self):
        return self.__nombres + " " + self.__apellidos

