"""
bd_clientes.py
Contiene una clase con sentencias CRUD para el manejo de una base de datos de clientes.
Nombre de la base: "base_clientes.db" 
Nombre de la tabla: "datos_clientes"

Este módulo aún está algo verde, y se necesita depurar mejor el código.
En la clase CRUD también he definido funciones que no son CRUD, pero que 
están relacionadas con el funcionamiento del programa.
Quizás sea buena idea separarlas de la clase CRUD si el programa crece.
Incluso no veo de gran utilizad en este momento tener un constructor __init__()
con tantas propiedades. Pero si en el futuro se añaden nuevas funciones es muy 
probable que se necesiten.

He creado una lista llamada "datos_prueba" para hacer tests con más rapidez 
cuando se modifica algún script.
"""


from dataclasses import dataclass
import sqlite3

datos_prueba = ['14321838', 'EMPRESA XX', 'Sociedad', 'Marcos Lopez', 'Compras', 
'España', 'VIGO', '36640', 'Calle xxx, nº 72', 
'986457176', '664099023', '986123123', 'empresaxx@gmail.com', 
'12345678W', '29-08-2022', 'Nuevo cliente.\nVisitar una vez al mes.\n']



@dataclass
class Datos_formulario(): 
    # Trabajando en esta clase. No se utiliza por ahora.
    # Fué creada para hacer algunas pruebas...
    N_cliente: str 
    Nombre: str 
    Tipo_emp: str
    Contacto: str
    Puesto: str
    Pais: str
    Ciudad: str
    C_postal: str
    Direccion: str
    Tel_fijo: str
    Tel_movil: str
    Fax: str
    Email: str
    Id_fiscal: str
    Fecha_registro: str
    Anotaciones: str



class Crud_Tabla_Clientes():
    def __init__(self, 
    n_cliente=None, cliente=None, tipo_emp=None, contacto=None, puesto=None,
    pais=None, ciudad=None, c_postal=None, direccion=None, 
    telefono1=None, telefono2=None, fax=None, email=None,
    id_fiscal=None, fecha=None, anotaciones=None
    ):
        
        self.n_cliente = n_cliente
        self.cliente = cliente
        self.tipo_emp = tipo_emp
        self.contacto = contacto
        self.puesto = puesto
        self.pais = pais
        self.ciudad = ciudad
        self.c_postal = c_postal
        self.direccion =direccion
        self.telefono1 = telefono1
        self.telefono2 = telefono2
        self.fax = fax
        self.email = email
        self.id_fiscal = id_fiscal      
        self.fecha = fecha
        self.anotaciones = anotaciones             

        self.retorno = True # Resultado de la consulta SQL
        self.lista = [] # Lista que almacena los datos de un cliente.
        self.dicc_clientes = {} # Almacena el nº cliente y nombre como clave / valor. 


        self.retorno = True
        self.lista = []
        self.dicc_clientes = {}

        
        self.crear_tabla()
    
    
    def crear_tabla(self):
        # crea la tabla "datos_clientes"
        con = sqlite3.connect("base_clientes.db")
        cursor = con.cursor()
        
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS datos_clientes( 
                N_cliente TEXT PRIMARY KEY,
                Nombre TEXT,
                Tipo_emp TEXT,
                Contacto TEXT,
                Puesto TEXT,
                Pais TEXT,
                Ciudad TEXT,
                C_postal TEXT,
                Direccion TEXT,
                Tel_fijo TEXT,
                Tel_movil TEXT,
                Fax TEXT,
                Email TEXT,
                Id_fiscal TEXT,
                Fecha_registro TEXT,
                Anotaciones TEXT
                )''')
        except:
            pass  

        finally:
            con.commit()
            con.close()


    def guardar_cliente_en_base(self, lista=None):
        # Guarda un nuevo cliente en la BD.
        con = sqlite3.connect("base_clientes.db")
        cursor = con.cursor()
        try:                                        
            query ="""INSERT INTO datos_clientes(
                N_cliente,
                Nombre,
                Tipo_emp,
                Contacto,
                Puesto,
                Pais,
                Ciudad,
                C_postal,
                Direccion,
                Tel_fijo,
                Tel_movil,
                Fax,
                Email,
                Id_fiscal,
                Fecha_registro,
                Anotaciones
                )
                values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" # Hay 16 campos.
            
            cursor.execute(query,(lista))
                
            self.retorno = True  
        except:
            self.retorno = False
        finally:
            con.commit()
            con.close()
    
    def ver_cliente(self):
        # Selecciona un cliente y retorna una tupla con los valores de ese cliente.
        with sqlite3.connect("base_clientes.db") as conn:
            cursor=conn.cursor()
            query = "SELECT * FROM datos_clientes WHERE N_cliente=?"
                        
            cursor.execute(query,(self.n_cliente,))
            self.lista = cursor.fetchall()

            for row in self.lista:
                self.n_cliente, self.cliente, self.tipo_emp, self.contacto, self.puesto, self.pais, self.ciudad, self.c_postal, self.direccion, self.telefono1, self.telefono2, self.fax, self.email,self.id_fiscal, self.fecha, self.anotaciones=row

    def ver_todo(self):
        # Selecciona todos los clientes de la tabla y los pasa 
        # a un diccionario que contiene como clave el nº de cliente y
        # como valor el nombre del cliente.
        # {"65448722": cliente 1, "12000346": cliente 2}
        with sqlite3.connect("base_clientes.db") as conn:
            cursor=conn.cursor()
            query = "SELECT * FROM datos_clientes"
                        
            cursor.execute(query,)
            self.lista = cursor.fetchall()
            for row in self.lista:
                self.dicc_clientes[row[0]]=row[1]



    def modificar_cliente(self, lista=None):
        # Modifica los datos del cliente.
        # Recibe una lista con todos los valores de esa fila(cliente).

        lista+=[lista.pop(0)] # Pasa el nº de cliente al final de la lista.
        cadena_set = "=?, ".join(self.extraer_campos()[1:16]) # Concatena los campos de la tabla de clientes
        cadena_set+="=?"                                      # para crear la consulta. 

        try:
            with sqlite3.connect("base_clientes.db") as conn:
                cursor=conn.cursor()
                query = f"UPDATE datos_clientes SET {cadena_set} WHERE N_cliente=?"                                
                cursor.execute(query, lista)
                self.retorno = True
        except:
            self.retorno = False

    def cliente_existe(self,cliente):
        # Retorna True si el cliente existe.
        # Junto con el valor booleano, se retorna el nombre del cliente que se 
        # ha buscado en la BD.
        valida = None
        with sqlite3.connect("base_clientes.db") as conn:
            cursor=conn.cursor()
            query = "SELECT Nombre FROM datos_clientes WHERE Nombre=?"
                        
            cursor.execute(query,(cliente,))
            resultado = cursor.fetchall()
            if resultado:
                valida = (True, cliente) # (True, cliente xx)
            else:
                valida = (False, cliente) # (False, cliente xx)
        #print(f"cliente = {cliente} -- cl_existe = {valida}")
        return valida


    def resultado_consulta(self):
        # Retorna una tupla con el resultado de la consulta "INSERT" 0 "UPDATE" SQL.
        # Si la consulta falla se retorna False y el formulario de clientes no se 
        # borra. Esto permite volver a realizar la operación sin la posibilidad de 
        # perder los datos.
        # Un mensaje "string" se retorna junto con el resultado para ser imprimido
        # en la ventana emergente que muestra el resultado de la consulta.
        if self.retorno == True:
            return (self.retorno, f'Datos guardados con éxito.')
        else:
            return (self.retorno, f'Ha ocurrido un error. Los datos no se han guardado!')
        # Ejemplo: (False, 'Ha ocurrido un error. Los datos no se han guardado!')


    def identificador_existe(self, id):
    # Selecciona el nº de cliente de un cliente registrado en la bd.
    # Retorna True si el nº cliente ya existe.
    # En la base de datos no he implementado el auto incremento, por eso
    # veo necesario comprobar que el número de cliente no existe,
        
        valida = None
        with sqlite3.connect('base_clientes.db') as conn:
            cursor=conn.cursor()
            query = "SELECT N_cliente FROM datos_clientes WHERE N_cliente=?"
                            
            cursor.execute(query,(id,))
            resultado = cursor.fetchall()
            if resultado:
                valida = (True)
            else:
                valida = (False)
        return valida


    def extraer_campos(self):
    # Retorna una lista con los nombres de los campos que contiene la tabla.
        with sqlite3.connect('base_clientes.db') as conn:
            cursor=conn.execute('SELECT * FROM datos_clientes')
            campos = list(map(lambda x: x[0], cursor.description))
            
        return campos


def guardar_nuevo_cliente(datos=None):
    # NO SE UTILIZA. ESTO ES ILEGIBLE Y CONFUSO. 
    cliente=Crud_Tabla_Clientes(
        n_cliente=datos[0], cliente=datos[1], tipo_emp=datos[2], contacto=datos[3], puesto=datos[4],
        pais=datos[5], ciudad=datos[6], c_postal=datos[7], direccion=datos[8], 
        telefono1=datos[9], telefono2=datos[10], fax=datos[11], email=datos[12],
        id_fiscal=datos[13], fecha=datos[14], anotaciones=datos[15]
        )
    cliente.guardar_cliente_en_base(datos)
    return cliente.resultado_consulta()

#print(crud_tabla_clientes(n_cliente="2343241").identificador_existe("dsaf"))
print()