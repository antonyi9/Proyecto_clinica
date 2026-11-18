
class Cita:
    def __init__(self, codigo, paciente, fecha, hora, estado):
        self.__codigo = codigo
        self.__paciente = paciente
        self.__fecha = fecha
        self.__hora = hora
        self.__estado = estado

    def obtenerCodigo(self):
        return self.__codigo

    def obtenerPaciente(self):
        return self.__paciente

    def obtenerFecha(self):
        return self.__fecha

    def obtenerHora(self):
        return self.__hora

    def obtenerEstado(self):
        return self.__estado

    def actualizarEstado(self, nuevoEstado):
        self.__estado = nuevoEstado

    def consultarCita(self):
        return (
            "Código de cita: " + self.__codigo
            + "\nPaciente: " + self.__paciente.mostrarDatos()
            + "\nFecha: " + self.__fecha
            + "\nHora: " + self.__hora
            + "\nEstado: " + self.__estado
        )
