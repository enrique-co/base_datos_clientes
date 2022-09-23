"""
ventana_ayuda.py
Script que contiene el código de la ventana de ayuda.
En esta ventana se detalla el uso del formulario de clientes.
"""

import tkinter as tk
from tkinter import ttk, Tk, Toplevel, Text, Button, Scrollbar, Frame


class Ayuda_Dialogo:
    def __init__(self, parent=None):
        text = ("Rellenar el formulario:\n"
                        "\t· El único campo obligatorio es el campo Cliente / Nombre.\n"
                        "\t· El código que identifica al cliente se asigna automáticamente.\n"
                        "\t· La fecha se asigna automáticamente.\n\n"
                "Botón GUARDAR:\n"
                        "\t· Envía los datos a la base de datos.\n"
                        "\t· Después del guardado, tiene la opción de añadir otro cliente.\n\n"
                "Botón BORRAR:\n"
                        "\t· Limpia el formulario. Debe rellenar de nuevo el formulario.\n"
                        "\t· ¿El botón borrar no funciona...?\n"
                        "\t· ...El formulario está en modo 'Lectura' o 'Edición'\n\n"
                "Botón EDITAR:\n"
                        "\t· Abre una nueva ventana para seleccionar el cliente que desea modificar.\n"
                        "\t· Si ya tiene un cliente cargado en modo 'Lectura', se activa el modo 'Edición' directamente.\n\n"
                "Botón VER CLIENTE:\n"
                        "\t· Abre una nueva ventana para seleccionar el cliente que desea visualizar.\n"
                        "\t· El formulario no se puede editar mientra está en modo lectura. Debe pulsar el botón EDITAR.\n"
                "Errores:\n"
                        "\t· El cliente ya existe.\n"
                                "\t\t· Debe cambiar el nombre del cliente.\n\n"
                        "\t· No se han guardado los datos.\n"
                                "\t\t· Ha ocurrido un error en el proceso de guardado.\n"
                                "\t\t· Debe rellenar de nuevo el formulario.\n\n"
                        "\t· No se puede guardar, debe añadir un cliente.\n"
                                "\t\t· Es necesario añadir un nombre de cliente antes de guardar.\n\n"

                "Actualizado el 12-08-2022")

                
        # VENTANA NIVEL SUPERIOR.
        self.top = Toplevel(parent)
        self.top.title("Ayuda")

        # Ventana que alberga todos los widgets de "self.top".
        contenido = Frame(self.top, width=300, height=200, padx=10, pady=10)
        contenido.grid(column=0, row=0, columnspan=3, rowspan=3)

        # Widget de texto que contiene el texto de ayuda.
        texto = Text(contenido)
        texto.grid(column=0, row=0, columnspan=2, rowspan=2)
        texto.insert(tk.INSERT, text)
        texto.config(state=tk.DISABLED, width=120, height=30, font="helvetica")

        # Ventana que alberga el botón de cerrar. 
        # Lo he puesto en una ventana diferente porque se quedaba situado encima del texto.
        ventana_boton = Frame(contenido)
        ventana_boton.grid(column=0, row=2, columnspan=3)

        # Botón "CERRAR".
        b = Button(ventana_boton, text="Cerrar", width=15,command=self.cerrar, relief="raised")
        b.grid(column=2, row=1)
        b.configure(background="white",fg="red")

        # Barra de desplazamiento para visualizar la parte oculta del texto.
        s = Scrollbar(contenido, width=20, orient=tk.VERTICAL, command=texto.yview)
        s.grid(column=2, row=0, rowspan=2, sticky=("N,S"))
        texto.configure(yscrollcommand=s.set)
        texto['yscrollcommand'] = s.set


    def cerrar(self):
        self.top.destroy()



def ayuda(parent=None):
    Ayuda_Dialogo(parent)


if __name__ == "__main__":            
    ayuda()
    #root = Tk()
    #Ayuda_Dialogo(root)
    #root.mainloop()