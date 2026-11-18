
import tkinter as tk

from presentacion.interfaz_grafica import InterfazGrafica


def main():
    ventana = tk.Tk()

    aplicacion = InterfazGrafica(ventana)

    ventana.mainloop()


if __name__ == "__main__":
    main()

