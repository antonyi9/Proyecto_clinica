from logica_negocio.paciente import Paciente
from logica_negocio.cita import Cita


class FabricaRegistros:

    def crearPaciente(self, codigo, nombres, apellidos, dni):
        return Paciente(codigo, nombres, apellidos, dni)

    def crearCita(self, codigo, paciente, fecha, hora, estado):
        return Cita(codigo, paciente, fecha, hora, estado)