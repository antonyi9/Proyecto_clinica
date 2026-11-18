
import csv
import os
import secrets
import re
from datetime import datetime

from logica_negocio.paciente import Paciente
from logica_negocio.cita import Cita


class SistemaGestion:
    """Gestiona pacientes y citas y conserva los datos en archivos CSV."""

    __instancia = None

    def __new__(cls):
        if cls.__instancia is None:
            cls.__instancia = super().__new__(cls)
        return cls.__instancia

    def __init__(self):
        if getattr(self, "_inicializado", False):
            return

        self._inicializado = True
        self.__pacientes = []
        self.__citas = []

        carpeta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        carpeta_datos = os.path.join(carpeta_proyecto, "datos")
        os.makedirs(carpeta_datos, exist_ok=True)

        self.__ruta_pacientes = os.path.join(carpeta_datos, "pacientes.csv")
        self.__ruta_citas = os.path.join(carpeta_datos, "citas.csv")

        self.cargarPacientes()
        self.cargarCitas()

    @staticmethod
    def normalizarTexto(valor):
        return " ".join(str(valor).strip().split())

    def generarCodigo(self, tipo="paciente"):
        existentes = (
            {p.obtenerCodigo() for p in self.__pacientes}
            if tipo == "paciente"
            else {c.obtenerCodigo() for c in self.__citas}
        )

        while True:
            codigo = str(secrets.randbelow(900000) + 100000)
            if codigo not in existentes:
                return codigo

    # PACIENTES

    def registrarPaciente(self, paciente):
        if self.buscarPaciente(paciente.obtenerDni()) is not None:
            return "Ya existe un paciente registrado con ese DNI."

        if any(p.obtenerCodigo() == paciente.obtenerCodigo()
               for p in self.__pacientes):
            return "El código generado ya existe. Intente nuevamente."

        self.__pacientes.append(paciente)
        self.guardarPacientes()

        return (
            "Paciente registrado correctamente.\nCódigo asignado: "
            + paciente.obtenerCodigo()
        )

    def buscarPaciente(self, dato):
        dato = str(dato).strip().casefold()

        for paciente in self.__pacientes:
            if (
                paciente.obtenerDni().casefold() == dato
                or paciente.obtenerCodigo().casefold() == dato
            ):
                return paciente

        return None

    def actualizarPaciente(self, dato, nombres, apellidos, dni=""):
        paciente = self.buscarPaciente(dato)

        if paciente is None:
            return "No se encontró al paciente."

        nuevo_dni = str(dni).strip() or paciente.obtenerDni()

        if not nuevo_dni.isdigit() or len(nuevo_dni) != 8:
            return "El DNI debe contener exactamente 8 dígitos."

        existente = self.buscarPaciente(nuevo_dni)

        if existente is not None and existente is not paciente:
            return "Ese DNI ya pertenece a otro paciente."

        paciente.actualizarDatos(
            self.normalizarTexto(nombres),
            self.normalizarTexto(apellidos),
            nuevo_dni
        )

        self.guardarPacientes()

        return "Datos del paciente actualizados correctamente."

    # CITAS

    def registrarCita(self, cita):
        estado = str(cita.obtenerEstado()).strip().casefold()

        estados_validos = {
            "pendiente": "Pendiente",
            "atendida": "Atendida",
            "cancelada": "Cancelada"
        }

        if estado not in estados_validos:
            return "Estado no válido. Seleccione Pendiente, Atendida o Cancelada."

        cita.actualizarEstado(estados_validos[estado])

        if any(c.obtenerCodigo() == cita.obtenerCodigo()
               for c in self.__citas):
            return "El código de cita ya existe. Genere otro código."

        for existente in self.__citas:
            if (
                existente.obtenerPaciente().obtenerCodigo()
                == cita.obtenerPaciente().obtenerCodigo()
                and existente.obtenerFecha() == cita.obtenerFecha()
                and existente.obtenerHora() == cita.obtenerHora()
                and existente.obtenerEstado() != "Cancelada"
            ):
                return "El paciente ya tiene una cita activa en esa fecha y hora."

        self.__citas.append(cita)
        self.guardarCitas()

        return (
            "Cita registrada correctamente.\nCódigo de cita: "
            + cita.obtenerCodigo()
        )

    def actualizarEstadoCita(self, codigo, nuevoEstado):
        codigo = str(codigo).strip()
        nuevoEstado = str(nuevoEstado).strip().casefold()

        estados_validos = {
            "pendiente": "Pendiente",
            "atendida": "Atendida",
            "cancelada": "Cancelada"
        }

        if nuevoEstado not in estados_validos:
            return "Estado no válido. Seleccione Pendiente, Atendida o Cancelada."

        for cita in self.__citas:
            if cita.obtenerCodigo() == codigo:
                cita.actualizarEstado(estados_validos[nuevoEstado])
                self.guardarCitas()
                return "Estado actualizado correctamente."

        return "No se encontró la cita seleccionada."

    def consultarCitas(self):
        return sorted(
            self.__citas,
            key=lambda c: (c.obtenerFecha(), c.obtenerHora())
        )

    def buscarCitas(self, dato):
        dato = str(dato).strip().casefold()

        if not dato:
            return self.consultarCitas()

        citas_ordenadas = self.consultarCitas()

        citas_filtradas = filter(
            lambda c: (
                c.obtenerCodigo().casefold() == dato
                or c.obtenerPaciente().obtenerCodigo().casefold() == dato
                or c.obtenerPaciente().obtenerDni().casefold() == dato
            ),
            citas_ordenadas
        )

        return list(citas_filtradas)

    def obtenerPacientes(self):
        return self.__pacientes

    def obtenerCitas(self):
        return self.__citas

    # CSV

    def guardarPacientes(self):
        with open(
            self.__ruta_pacientes,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:

            escritor = csv.writer(archivo)
            escritor.writerow(["codigo", "nombres", "apellidos", "dni"])

            for p in self.__pacientes:
                escritor.writerow([
                    p.obtenerCodigo(),
                    p.obtenerNombres(),
                    p.obtenerApellidos(),
                    p.obtenerDni()
                ])

    def cargarPacientes(self):
        if (
            not os.path.exists(self.__ruta_pacientes)
            or os.path.getsize(self.__ruta_pacientes) == 0
        ):
            return

        with open(
            self.__ruta_pacientes,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:

            muestra = archivo.read(2048)
            archivo.seek(0)

            separador = (
                ";"
                if muestra.splitlines()
                and muestra.splitlines()[0].count(";")
                > muestra.splitlines()[0].count(",")
                else ","
            )

            lector = csv.DictReader(archivo, delimiter=separador)

            if not lector.fieldnames:
                return

            lector.fieldnames = [
                x.strip().lstrip("\ufeff").lower()
                for x in lector.fieldnames
            ]

            requeridas = {"codigo", "nombres", "apellidos", "dni"}

            if not requeridas.issubset(set(lector.fieldnames)):
                raise ValueError(
                    "pacientes.csv debe contener: codigo,nombres,apellidos,dni"
                )

            for fila in lector:
                if not fila.get("dni"):
                    continue

                codigo = (
                    (fila.get("codigo") or "").strip()
                    or self.generarCodigo("paciente")
                )

                paciente = Paciente(
                    codigo,
                    (fila.get("nombres") or "").strip(),
                    (fila.get("apellidos") or "").strip(),
                    (fila.get("dni") or "").strip()
                )

                if self.buscarPaciente(paciente.obtenerDni()) is None:
                    self.__pacientes.append(paciente)

    def guardarCitas(self):
        with open(
            self.__ruta_citas,
            "w",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:

            escritor = csv.writer(archivo)
            escritor.writerow([
                "codigo",
                "paciente_codigo",
                "fecha",
                "hora",
                "estado"
            ])

            for c in self.__citas:
                escritor.writerow([
                    c.obtenerCodigo(),
                    c.obtenerPaciente().obtenerCodigo(),
                    c.obtenerFecha(),
                    c.obtenerHora(),
                    c.obtenerEstado()
                ])

    def cargarCitas(self):
        if (
            not os.path.exists(self.__ruta_citas)
            or os.path.getsize(self.__ruta_citas) == 0
        ):
            return

        with open(
            self.__ruta_citas,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as archivo:

            muestra = archivo.read(2048)
            archivo.seek(0)

            separador = (
                ";"
                if muestra.splitlines()
                and muestra.splitlines()[0].count(";")
                > muestra.splitlines()[0].count(",")
                else ","
            )

            lector = csv.DictReader(archivo, delimiter=separador)

            if not lector.fieldnames:
                return

            lector.fieldnames = [
                x.strip().lstrip("\ufeff").lower()
                for x in lector.fieldnames
            ]

            requeridas = {
                "codigo",
                "paciente_codigo",
                "fecha",
                "hora",
                "estado"
            }

            if not requeridas.issubset(set(lector.fieldnames)):
                raise ValueError(
                    "citas.csv debe contener: codigo,paciente_codigo,fecha,hora,estado"
                )

            for fila in lector:
                paciente = self.buscarPaciente(
                    (fila.get("paciente_codigo") or "").strip()
                )

                if paciente is None or not fila.get("codigo"):
                    continue

                estado = (
                    fila.get("estado") or "Pendiente"
                ).strip().capitalize()

                if estado not in ("Pendiente", "Atendida", "Cancelada"):
                    estado = "Pendiente"

                self.__citas.append(
                    Cita(
                        (fila.get("codigo") or "").strip(),
                        paciente,
                        (fila.get("fecha") or "").strip(),
                        (fila.get("hora") or "").strip(),
                        estado
                    )
                )
