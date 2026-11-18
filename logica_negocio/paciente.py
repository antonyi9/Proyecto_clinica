
from logica_negocio.persona import Persona


class Paciente(Persona):
    def __init__(self, codigo, nombres, apellidos, dni):
        super().__init__(codigo, nombres, apellidos)
        self.__dni = dni

    def obtenerDni(self):
        return self.__dni

    def actualizarDatos(self, nombres, apellidos, dni):
        super().actualizarDatos(nombres, apellidos)
        self.__dni = dni

    def consultarDatos(self):
        return (
            "Código: " + self.obtenerCodigo()
            + "\nNombres: " + self.obtenerNombres()
            + "\nApellidos: " + self.obtenerApellidos()
            + "\nDNI: " + self.__dni
        )
