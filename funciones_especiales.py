"""
funciones_especiales.py
Este módulo contiene cuatro funciones.
Son funciones de apoyo que, si bien no son indispensables para el buén
funcionamiento del programa, ayudan al usuario a la hora de rellenar los
datos de un nuevo cliente.

"""


import sqlite3
import string
import secrets
from datetime import date
import datetime
import locale
from bd_clientes import Crud_Tabla_Clientes


def creaClaveUser():
    # Crea una clave o nº de cliente.
    numeros = string.digits
    clave=''.join(secrets.choice(numeros) for i in range(8))
    clave = verifica_clave(clave)
    
    return clave


def verifica_clave(clave):
    # Verifica que la clave proporcionada no está asignada a ningún
    # cliente registrado en la bd.
    v_clave = Crud_Tabla_Clientes()
    valida = v_clave.identificador_existe(clave)
    while valida:
        clave = creaClaveUser()
        valida = v_clave.identificador_existe(clave)
    else:
        return clave
    

def fechasDeRegistro():        
    #Día actual
    hoy=date.today()
    hoy=hoy.strftime('%d-%m-%Y')    
    #Fecha actual
    fechaYHora=datetime.datetime.utcnow()
    return hoy

def fecha_hoy():
    locale.setlocale(locale.LC_ALL, 'es_ES') 
    fecha = datetime.datetime.now()
    f_iso = fecha.isoformat()
    f_completa = fecha.strftime("%A %d %B %Y %I:%M")
    return fecha.strftime("%A %d %B de %Y")


