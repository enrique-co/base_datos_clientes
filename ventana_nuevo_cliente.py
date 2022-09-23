"""
ventana_nuevo_cliente.py
Interface gráfica para el manejo de una base de datos de clientes.

Este módulo contiene dos clases:

Clase Gestion_Clientes:
    Funciones:
        nuevo_cliente  ----------  Crear un nuevo cliente a través del formulario.
        editar_cliente ----------  Editar un cliente que ya existe.
        ver_cliente    ----------  Visualizar los datos de un cliente que ya existe.
        guardar        ----------  Guardar los datos de un nuevo cliente.
        borrar         ----------  Borrar todos los campos del formulario.
        ayuda          ----------  Ventana de ayuda.


Clase TOPlevel_Selec_Cliente:
    Funciones:
        seleccionar_cliente -----  Selecciona un cliente de la lista
        cargar_cliente      -----  Recupera los datos del cliente seleccionado.
        info                -----  Muestra un detalle de la información del cliente seleccionado.

El programa se inicia con la interface gráfica.
En ella se albergan todos los "Label Entry" para introducir los datos del nuevo cliente. 
También tiene una paleta de botones con las funciones detalladas en la clase "Gestion_Clientes".
En la parte superior se muestra, a modo informativo, la fecha y el número de cliente.

La misma interface cumple la función de editar datos y de visualizar datos, ya que cada vez que 
se realiza una de estas funciones, los datos del cliente se cargan en los mismos "Label Entry" que 
se utilizan para un nuevo cliente. La única diferencia es que en el modo "VER CLIENTE" se bloquea 
la escritura. 

Para seleccionar un cliente, se abre una ventana de nivel superior, escrita en la clase 
"TOPlevel_Selec_Cliente".
El usuario selecciona un cliente, luego pulsa el botón "ACEPTAR", y la ventana se cierra sola.
Los datos se cargan automáticamente en la interface principal.

Al principio, este módulo estaba escrito sin utilizar clases. Cuando casi estaba finalizado decidí
estructurarlo en clases y tube que realizar cambios bastante importantes, aunque reconozco que queda 
mejor de esta manera. 

Todavía habrá algunos errores eventuales que puedan ocurrir.
También hay partes del código que pueden ser un poco confusas (intento mejoarlo). Aunque todas las funciones
y métodos están explicados.

Funcionamiento de los botonoes:
Botón "GUARDAR":
Guarda un nuevo cliente en la base de datos. La BD está en el módulo "bd_clientes.py"
Este botón cambia su nombre de "GUARDAR" a "ACTUALIZAR" cuando el usuario está en modo "EDITAR". 
Pensé que era una forma más clara de especificar lo que hace este botón en cada momento.

Botón "VER CLIENTE":
Una vez pulsado, se abre la ventana de nivel superior para seleccionar un cliente de la base de datos. Una vez 
seleccionado, el usuario debe preisonar el botón "ACEPTAR" para pasar los datos al formulario. La ventana 
se cerrará automáticamente.
Mientras la ventana de nivel superior de selección de cliente está abierta, el botón "VER CLIENTE" permanece en 
estado inactivo. Esto impide que, si el usuario vuelve a presionar el botón, no se abrirá una nueva ventana.
Los datos del cliente NO se pueden modificar mientras está en modo "VER CLIENTE".

Botón "EDITAR":
Si el usuario lo pulsa, el programa evalúa lo siguiente:
    Si ya hay un cliente cargado en el formulario, y éste está en modo "VER CLIENTE", el formulario se desbloquea 
para que el usuario pueda modificar los datos de ese cliente,
    Si el formulario está vacío se abre la ventana de nivel superior para seleccionar un cliente de la base de datos.
    Una vez seleccionado, el usuario debe preisonar el botón "ACEPTAR" para pasar los datos al formulario. 
    La ventana se cerrará automáticamente.

Mientras la ventana de nivel superior de selección de cliente está abierta, el botón "EDITAR" permanece en 
estado inactivo. Esto impide que, si el usuario vuelve a presionar el botón, no se abrirá una nueva ventana.

Botón "NUEVO":
Limpia el formulario para introducir los datos de un nuevo cliente.
Este botón también actúa cuando el formulario está en modo "EDITAR" o "VER CLIENTE", pero no realiza ningún cambio
en los datos del cliente que estaba cargado.

Botón "BORRAR":
Borra todos los datos del formulario cuando el usuario está creando un nuevo cliente. Es útil si el usuario ha 
escrito varios datos incorrectos. Borra todo y listo.
El botón "BORRAR" está desactivado mientras el formulario está en modo "EDITAR" o "VER CLIENTE".

Botón "AYUDA":
Abre una ventana de nivel superior que muestra una descripción textual de como utilizar el formulario y sus 
funciones.

Ventana nivel superior de selección de cliente:
Combobox:
Muestra el nombre de todos los clientes de la base de datos.

Botón "ACEPTAR" Ventana nivel superior:
Confirma el cliente seleccionado y lo almacena en la variable "datos=[]", que se utiliza para rellenar el 
formulario.

* Esta ventana no tiene botón de cierre. Siempre se cierra sola. (o en la X)


REVISAR:
El número de usuario se crea automáticamente al iniciar el programa.
No me gusta eso...

"""

from tkinter import *
from tkinter import ttk, messagebox, Button, Entry, Label, Frame
from funciones_especiales import creaClaveUser as clave, fechasDeRegistro as fecha, fecha_hoy
from bd_clientes import Crud_Tabla_Clientes as CRUD
from ventana_ayuda import ayuda as help


class Gestion_Clientes():
    lista = [] # Se utiliza para enviar los datos a la BD.
    ncliente = clave() # Nº cliente. Se asigna automáticamente. No es editable.
    Fecha = fecha() # Fecha hoy. Se pasa automáticamente. No es editable.
    edicion_bloqueada = False # Autoriza o no la edición del formulario.
    solo_lectura = False # Controla el modo de solo lectura. NO DEJA LIMPIAR LOS DATOS DEL FORMULARIO!!
    cliente_ya_cargado = False # Verifica si un cliente está o no está cargado en el formulario.
    modo_editar = False
    tipo_cliente = ["Particular", "Autónomo", "Sociedad"]
    puesto = ["Director", "Jefe ventas", "Compras", "RRHH"]   
    
    def __init__(self, master):
        self.master = master
        self.cl = CRUD() # Instancia de la clase "Crud_tabla_clientes"
                                # Módulo bd_clientes.py

        # Estilos de los botones.
        self.style = ttk.Style()
        self.style.map("C.TButton", # Todos los botones llevan este estilo.
            foreground=[('pressed', 'red'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'red'), ('active', 'black')]
            )
        
        self.style.configure("CC.TButton", # En pruebas para señalar el siguiente botón a pulsar.
            foreground=('red'),
            background=('red')              
            )

        self.style.configure('TSeparator', background='grey') # Barra separadora justo antes del campo "anotaciones"
        #----------------                       


        # Variables para los campos editables.
        self.ent_nombre=StringVar()
        self.ent_tipo_cliente = StringVar()
        self.ent_contacto=StringVar()
        self.ent_puesto=StringVar()
        self.ent_pais=StringVar()
        self.ent_tel_1=StringVar()
        self.ent_tel_2=StringVar()
        self.ent_fax=StringVar()
        self.ent_ciudad=StringVar()
        self.ent_postal=StringVar()
        self.ent_direccion=StringVar()
        self.ent_email=StringVar()
        self.ent_nif_cif=StringVar()
        self.entry_anotaciones=StringVar()
        #------------------------------


        #----FRAME QUE CONTIENE LOS Labels y Entrys----------------
        # ---Frame contenedor--------------------------------------
        self.contenido=ttk.Frame(root, borderwidth=5, padding=(5,5,5,5), width=670, height=600)
        self.contenido.pack(anchor="w")
        self.contenido.grid_propagate(0)
        # Todos los widgets de abajo se albergan en esta ventana.

        self.Labels_Entrys(self.contenido)

 
        

        #----BLOQUE DE BOTONES DE CONTROL A LA DERECHA--------
        # GUARDAR / ACTUALIZAR, BORRAR, NUEVO, CARGAR, EDITAR.
        # Se albergan en una nueva ventana "ventana_botones" que está colocada a la derecha
        # y pertenece a la ventana "contenido".
        # Para colocar los botones he utilizado .place() en lugar de .grid()

        self.ventana_botones=ttk.Frame(self.contenido, relief="solid", width=100, height=235)
        self.ventana_botones.grid(column=3, row=15, rowspan=3, sticky=(S))

        # Botón "VER CLIENTE".
        self.cargar_cliente=ttk.Button(self.ventana_botones, width=12, text='VER CLIENTE', style="C.TButton", command=lambda: [self.Abre_selec_cliente(), self.bloquear_edicion()])
        self.cargar_cliente.place(x=9, y=126)

        # Botón "NUEVO" cliente.
        self.nuevo=ttk.Button(self.ventana_botones, width=12, text='NUEVO',style="C.TButton", command=lambda: [self.nuevo_cliente(), self.borrar_datos_cliente(), self.habilitar_edicion()])
        self.nuevo.place(x=9, y=86)
        

        # Botón "EDITAR" cliente.
        self.editar_cliente=ttk.Button(self.ventana_botones, width=12, text='EDITAR', style="C.TButton", command=lambda: [self.autoriza_selec_cliente(), self.edita_cliente()])
        self.editar_cliente.place(x=9, y=166)

        # Botón "AYUDA".
        ayuda = ttk.Button(self.ventana_botones, width=12, text="AYUDA", style="C.TButton", command=help)
        ayuda.place(x=9, y=204)

        self.guardar_o_actualizar(True) # "GUARDAR" se inicia siempre activado.
        self.act_des_borrar(True) # "BORRAR" se inicia siempre activado.

    
    # Botón "GUARDAR" o "ACTUALIZAR".
    def guardar_o_actualizar(self, valor = None):
            # El nombre del botón cambia entre "GUARDAR" y "ACTUALIZAR".
            # Está en modo "GUARDAR" cuando:
                # Se inicia el programa.
                # Se introduce un nuevo cliente.
                # Después de realizar cualquier consulta.
            # Está en modo "ACTUALIZAR" cuando:
                # Se edita un cliente ya existente.
            
        self.guardar=ttk.Button(self.ventana_botones, width=12, style="C.TButton", command=self.lista_entradas)
        self.guardar.place(x=9, y=7)
        if valor:
            self.modo_editar = False
            self.guardar.configure(text='GUARDAR')
        elif not valor:
            self.modo_editar = True
            self.guardar.configure(text='ACTUALIZAR')

        

    # Botón "BORRAR".
    def act_des_borrar(self, valor = None): # Activa o desctiva el botón "borrar".
        # El botón borrar NO puede estar activo en determinados casos, por ejemplo:
            # El formulario está en modo "solo lectura", para cosultar los datos del cliente.
            # El formulario está en modo "edición", para modificar uno o varios datos del cliente. 
            # ¿Porqué el usuario querría limpiar todo el formulario en estos dos casos?

        self.borrar=ttk.Button(self.ventana_botones, width=12, text='BORRAR', style="C.TButton")
        self.borrar.place(x=9, y=46)
        if valor == True: # Activa el botón "BORRAR".     
            self.borrar.configure(command=self.borrar_datos_cliente)

        elif valor == False: # Desactiva el botón "BORRAR".
            self.borrar.configure(command=None)
    

        #---------------------------------------------
        #---------------------------------------------

    def Labels_Entrys(self, contenido = None):
        #-----------LABELS Y ENTRYS-----------------------
        # Todos están en orden de arriba hacia abajo.
        # Para colocarlos he utilizado .grid()
        # Tengo dudas de si .grid() sea la mejor opción.

        #centro
        self.info_fecha = ttk.Label(contenido, text=f"Hoy es {fecha_hoy()}", font=("Arial", 10, "bold"))
        self.info_fecha.place(x=250, y=0)

        # Derecha
        self.numero_cliente = ttk.Label(contenido, text=f"Nº Cliente: {self.ncliente}", font=("Arial", 10))
        self.numero_cliente.grid(column=3, row=0, sticky=W)

        # izquierda
        self.nombre_cliente=ttk.Label(contenido, text='Cliente / Empresa', font=("Arial", 10, "bold"))
        self.nombre_cliente.grid(column=0, row=1, sticky=W)
        self.entry_cliente=ttk.Entry(contenido, width=40, font=("arial", 12), textvariable=self.ent_nombre)
        self.entry_cliente.grid(column=0, row=2, columnspan=2, sticky=W)

        # derecha
        self.tipo_de_cliente=ttk.Combobox(contenido, width=10, values=self.tipo_cliente, textvariable=self.ent_tipo_cliente, font=("Arial", 8))
        self.tipo_de_cliente.grid(column=2, row=2, sticky=W)

        # izquierda
        self.contacto=ttk.Label(contenido, text='Contacto', font=("Arial", 10, "bold"))
        self.contacto.grid(column=0, row=3, sticky=W)
        self.entry_contacto=ttk.Entry(contenido, width=40, font=("arial", 12), textvariable=self.ent_contacto)
        self.entry_contacto.grid(column=0, row=4, columnspan=2, sticky=(W,N))

        # derecha
        self.puesto_del_contacto=ttk.Combobox(contenido, font=("Arial", 8), width=10, values=self.puesto, textvariable=self.ent_puesto)
        self.puesto_del_contacto.grid(column=2, row=4, sticky=(W,N))

        # izquierda
        self.pais=ttk.Label(contenido, text='Pais', font=("Arial", 10, "bold"))
        self.pais.grid(column=0, row=5, sticky=W)
        self.entry_pais=ttk.Entry(contenido, width=20, font=("arial", 12), textvariable=self.ent_pais)
        self.entry_pais.grid(column=0, row=6, sticky=W)

        # derecha
        self.ciudad=ttk.Label(contenido, text='Ciudad', font=("Arial", 10, "bold"))
        self.ciudad.grid(column=1, row=5, padx=25, sticky=W)
        self.entry_ciudad=ttk.Entry(contenido, width=20, font=("arial", 12), textvariable=self.ent_ciudad)
        self.entry_ciudad.grid(column=1, row=6, sticky=E, padx=25)

        # izquierda
        self.c_postal = ttk.Label(contenido, text="Código postal", font=("Arial", 10, "bold"))
        self.c_postal.grid(column=2, row=5, sticky=W)
        self.entry_c_postal = ttk.Entry(contenido, width=10, font=("arial", 12), textvariable=self.ent_postal)
        self.entry_c_postal.grid(column=2, row=6, sticky=W)

        # izquierda
        self.direccion = ttk.Label(contenido, text='Dirección',font=("Arial", 10, "bold"))
        self.direccion.grid(column=0, row=7,sticky=W)
        self.entry_direccion = ttk.Entry(contenido, width=57,font=("arial", 12), textvariable=self.ent_direccion)
        self.entry_direccion.grid(column=0, row=8, sticky=W, columnspan=4)

        # izquierda
        self.tel_1=ttk.Label(contenido, text='Tel. fijo',font=("Arial", 10, "bold"))
        self.tel_1.grid(column=0, row=9, sticky=W)
        self.entry_tel_1=ttk.Entry(contenido, width=15,font=("arial", 12), textvariable=self.ent_tel_1)
        self.entry_tel_1.grid(column=0, row=10, sticky=W)

        # derecha
        self.tel_2=ttk.Label(contenido, text='Tel. Móvil',font=("Arial", 10, "bold"))
        self.tel_2.grid(column=1, columnspan=2,row=9, sticky=W)
        self.entry_tel_2=ttk.Entry(contenido, width=15, font=("arial", 12), textvariable=self.ent_tel_2)
        self.entry_tel_2.grid(column=1, row=10, columnspan=2, sticky=W)

        # derecha
        self.fax=ttk.Label(contenido, text='Fax',font=("Arial", 10, "bold"))
        self.fax.grid(column=1, row=9, columnspan=2, padx=110, sticky=(E))
        self.entry_fax=ttk.Entry(contenido, width=15, font=("arial", 12), textvariable=self.ent_fax)
        self.entry_fax.grid(column=1, row=10, columnspan=2, sticky=E)

        # izquierda
        self.email=ttk.Label(contenido, text="Email", font=("Arial", 10, "bold"))
        self.email.grid(column=0, row=11, sticky=W)
        self.entry_email=ttk.Entry(contenido, width=57, font=("arial", 12), textvariable=self.ent_email)
        self.entry_email.grid(column=0, row=12, columnspan=4, sticky=W)

        #derecha
        self.nif_cif = ttk.Label(contenido, text="NIF / CIF o Número de registro", font=("Arial", 10, "bold"))
        self.nif_cif.grid(column=0, row=13, columnspan=3, sticky=W)
        self.entry_nif_cif = ttk.Entry(contenido, width=22, font=("Arial", 12), textvariable=self.ent_nif_cif)
        self.entry_nif_cif.grid(column=0, row=14, columnspan=3, sticky=W)

        # izquierda
        ttk.Separator(contenido,style="TSeparator"
            ).grid(row=15, column=0, columnspan=3, sticky="EW", pady=15)

        # izquierda
        self.anotaciones=ttk.LabelFrame(contenido, text='Anotaciones', padding=(0,10, 0, 5))
        self.anotaciones.grid(column=0, row=16, columnspan=4, sticky=W)
        self.entry_anotaciones=Text(self.anotaciones, width=57, height=10, relief="solid", background=("white"), font=("arial", 12), wrap="word")
        self.entry_anotaciones.grid(column=0, row=0, columnspan=4, rowspan=3, sticky=W)

        #-----------------------------------FIN LABELS Y ENTRY------------------------------------------------------
        #-------------------------------------------------------------------------------------------------------



        

    # Estas funciones de abajo sirven para controlar diferentes variables o funciones que
    # reciben o almacenan valores True o False.
    # He pensado que es una buena manera de tener estas variables bajo control, 
    # en lugar de estar esparcidas por todo el código.
    def nuevo_cliente(self):
        self.edicion_bloqueada = False
        self.guardar_o_actualizar(True)
        self.act_des_borrar(True)

    def edita_cliente(self):
        self.modo_editar = True
        self.guardar_o_actualizar(False)
        self.act_des_borrar(False)

    def carga_de_cliente(self):
        self.act_des_borrar(False)



    def bloquear_edicion(self): # (PENDIENTE DE REVISAR)
        # Bloquea la edición de los datos del formulario.
        # Se activa el bloqueo cuando se carga un cliente para visualizar los datos.
        # Estoy seguro de que existe una forma más fácil y legible que esta. 
        self.entry_cliente.configure(state='disabled')
        self.entry_c_postal.configure(state='disabled')
        self.entry_anotaciones.configure(state='disabled')
        self.entry_ciudad.configure(state='disabled')
        self.entry_contacto.configure(state='disabled')
        self.entry_email.configure(state='disabled')
        self.entry_fax.configure(state='disabled')
        self.entry_nif_cif.configure(state='disabled')
        self.entry_pais.configure(state='disabled')
        self.entry_tel_1.configure(state='disabled')
        self.entry_tel_2.configure(state='disabled')
        self.puesto_del_contacto.configure(state='disabled')
        self.tipo_de_cliente.configure(state='disabled')
        self.entry_direccion.configure(state='disabled')

    def habilitar_edicion(self): # (PENDIENTE DE REVISAR)
        # Se habilita la edición de datos cuando:
        # se introduce un nuevo cliente o
        # se pulsa el botón "editar"
        # Estoy seguro de que existe una forma más fácil y legible que esta. 
        self.entry_cliente.configure(state='normal')
        self.entry_c_postal.configure(state='normal')
        self.entry_anotaciones.configure(state='normal')
        self.entry_ciudad.configure(state='normal')
        self.entry_contacto.configure(state='normal')
        self.entry_email.configure(state='normal')
        self.entry_fax.configure(state='normal')
        self.entry_nif_cif.configure(state='normal')
        self.entry_pais.configure(state='normal')
        self.entry_tel_1.configure(state='normal')
        self.entry_tel_2.configure(state='normal')
        self.puesto_del_contacto.configure(state='normal')
        self.tipo_de_cliente.configure(state='normal')
        self.entry_direccion.configure(state='normal')





    def cargar_datos_cliente(self, id = None): 
        # recibe como parámetro el nº de cliente.
        # Se busca el "id" en la base de datos.
        # Se cargan los datos en el formulario.

        self.solo_lectura = True
        self.edicion_bloqueada = True

        if not id:
        # Si el usuario no selecciona un cliente, salta un mensaje de error.
            messagebox.showerror(message=f"""Debes seleccionar un cliente de la lista.""", title='ERROR')
            #self.act_des_verCliente(True)
        else:
            
            self.cliente_ya_cargado = True
            self.ncliente = id
            # Se busca el cliente en la base de datos.
            self.cl.n_cliente = self.ncliente # Instancia de la clase "Crud_tabla_clientes"
                                        # Módulo bd_clientes.py
            self.cl.ver_cliente()

            # Se cargan los datos en el formulario.
            self.ent_nombre.set(self.cl.cliente)
            self.ent_tipo_cliente.set(self.cl.tipo_emp)
            self.ent_contacto.set(self.cl.contacto)
            self.ent_puesto.set(self.cl.puesto)
            self.ent_pais.set(self.cl.pais)
            self.ent_ciudad.set(self.cl.ciudad)
            self.ent_postal.set(self.cl.c_postal)
            self.ent_direccion.set(self.cl.direccion)
            self.ent_email.set(self.cl.email)
            self.ent_tel_1.set(self.cl.telefono1)
            self.ent_tel_2.set(self.cl.telefono2)
            self.ent_fax.set(self.cl.fax)
            self.ent_nif_cif.set(self.cl.id_fiscal)   
            self.numero_cliente['text'] = f"Nº Cliente: {self.cl.n_cliente}"
            self.entry_anotaciones.delete("1.0","end")
            self.entry_anotaciones.insert(1.0, self.cl.anotaciones)
            if self.solo_lectura:
                self.act_des_borrar(False)
            #self.act_des_verCliente(True)


    def borrar_datos_cliente(self):
    # Limpia el formulario cuando: 
        # El usuario decide pulsar el botón de "BORRAAR".
        # El usuario decide añadir un nuevo cliente.
        # Ocurre un error en el guardado de datos.

        if self.edicion_bloqueada == True:
            messagebox.showerror(message=f"""No se pueden eliminar todos los datos\nen modo edición.""", title='ERROR')
        
        else:
            self.ent_nombre.set('')
            self.ent_tipo_cliente.set('')
            self.ent_contacto.set('')
            self.ent_puesto.set('')
            self.ent_pais.set('')
            self.ent_ciudad.set('')
            self.ent_postal.set('')
            self.ent_direccion.set('')
            self.ent_email.set('')
            self.ent_tel_1.set('')
            self.ent_tel_2.set('')
            self.ent_fax.set('')
            self.ent_nif_cif.set('')
            self.entry_anotaciones.delete("1.0","end")
            self.ncliente=clave()
            self.numero_cliente['text'] = f"Nº Cliente: {self.ncliente}"

            self.cliente_ya_cargado = False

    def lista_entradas(self):
    # Se obtienen los datos de los campos del formulario y los añade a una lista.
    # Antes de obtener los datos, se comprueba que el campo obligatorio "Cliente" ha sido introducido.
    # Si no es así, salta una alerta y el usuario debe introducir un nombre de cliente.
    # Solo cuando se introduce un nombre de cliente, el condicional salta al "else" y se ejecuta el... 
    # ...resto de la función.

        nom = self.ent_nombre.get().upper()

        if not nom:
            messagebox.showerror(message=f"""El campo cliente es obligatorio!""", title='ERROR')
        
        else:
            tip = self.ent_tipo_cliente.get()
            cont = self.ent_contacto.get().capitalize()
            puest = self.ent_puesto.get()
            pa = self.ent_pais.get().capitalize()
            ciud = self.ent_ciudad.get().capitalize()
            postal = self.ent_postal.get().capitalize()
            direc = self.ent_direccion.get().capitalize()
            tel1 = self.ent_tel_1.get()
            tel2 = self.ent_tel_2.get()
            fax1 = self.ent_fax.get()
            email1 = self.ent_email.get()
            nifCif = self.ent_nif_cif.get()
            nota = self.entry_anotaciones.get("1.0","end")
            self.lista=[self.ncliente, nom, tip, cont, puest, pa, ciud, postal, direc, tel1, tel2, fax1, email1, nifCif, self.Fecha, nota]
            #print(self.lista)

            self.guardado_de_datos() # Pasa los datos a la función de guardado.


    
    def guardado_de_datos(self):
    # Primero se evalúa que el cliente no existe. Si existe salta una alerta.
    # resultado_guardado = carga(lista) --> Guarda los datos en la base de datos
    # carga(lista) --> Retorna el resultado de la consulta SQL.
    # Si el resultado es True = (Datos guardados correctamente.)
        # Opción de añadir más clientes o cerrar el programa.
    # Si el resultado es False = (Ha ocurrido un error al guardar los datos.)
        # Se borran los datos del formulario para iniciar el proceso otra vez.
        # **No estoy seguro de si limpiar todo el formulario es buena opción**



        self.cl.lista = self.lista # Instancia de la clase "Crud_tabla_clientes"
                        # Módulo bd_clientes.py
        self.cl.cliente = self.lista[1]                                                         # NO ESTÁ COMPROBANDO BIEN SI EL CLIENTE EXISTE. DA ERROR CLIENTE NO EXISTE

        if self.cl.cliente_existe(self.cl.cliente)[0] == True and self.modo_editar == False: # Alerta, el cliente ya existe.           
            messagebox.showerror(message=f"""El cliente <{self.lista[1]}> ya existe!""", title='ERROR')
            
            self.ent_nombre.set('') # Se limpia el campo "Cliente" para volver a insertar un nuevo nombre.

        else:            
            if self.modo_editar == False: # Entra en el método CRUD de guardar nuevo cliente.
                self.cl.guardar_cliente_en_base(self.lista) # Se envían los datos a la bd.

                if self.cl.resultado_consulta()[0] == True:
                    messagebox.showinfo(message=self.cl.resultado_consulta()[1], title='Información') # Datos guardados correctamente.
                    pregunta = messagebox.askyesno(message="¿Deseas añadir otro cliente?", title="Pregunta")
                        
                    if pregunta:
                        self.borrar_datos_cliente() # Limpia el formulario para añadir nuevo cliente.
                        self.guardar_o_actualizar(True)
                        self.act_des_borrar(True) 
                    
                    else:
                        root.destroy() # Cierra el programa.

                else:
                    messagebox.showerror(message=self.cl.resultado_consulta()[1], title='ERROR') # Error durante el guardado de datos.
                    self.guardar_o_actualizar(True)
                    self.act_des_borrar(True)
            
            
            elif self.modo_editar == True:
                self.cl.modificar_cliente(self.lista) # Se envían los datos a la bd.
                
                if self.cl.resultado_consulta()[0] == True:
                    messagebox.showinfo(message=self.cl.resultado_consulta()[1], title='Información') # Datos guardados correctamente.
                    pregunta = messagebox.askyesno(message="¿Deseas realizar otra consulta?", title="Pregunta")
                        
                    if pregunta:
                        self.edicion_bloqueada = False # desbloquea el modo edicion para AUTORIZAR limpiar todo el formulario
                        self.borrar_datos_cliente() # Limpia el formulario para añadir nuevo cliente.
                        self.guardar_o_actualizar(True)
                        self.act_des_borrar(True) 
                    
                    else:
                        root.destroy() # Cierra el programa.

                else:
                    messagebox.showerror(message=self.cl.resultado_consulta()[1], title='ERROR') # Error durante el guardado de datos.
                    self.guardar_o_actualizar(True)
                    self.act_des_borrar(False)

    def autoriza_selec_cliente(self):
        # Esta función se activa con el botón 'EDITAR'.
        # Hace una evaluación de los datos cargados en el formulario y, si ya existen datos cargados
        # no se abre la ventana de selección de cliente. Simplemente se habilita directamente
        # la edición del cliente que ya está cargado. 

        if self.cliente_ya_cargado: # Permite evaluar si un cliente ya está cargado en el formulario.
            self.habilitar_edicion()
            self.guardar_o_actualizar(False)
                
        else:
            self.Abre_selec_cliente()
            

    def Abre_selec_cliente(self):

        app = TOPlevel_Selec_Cliente(root, id=self.ncliente, cl_cargado=self.cliente_ya_cargado) # Toplevel seleccionar cliente.
        



#-----------------------------------------------------------------------------
#-------- INICIO DE LA CLASE "TOPlevel_Selec_Cliente" ------------------------

class TOPlevel_Selec_Cliente:
    # Ventana emergente de selección de clientes.
    # Se abre para seleccionar un cliente que el usuario desea editar
    # o visualizar.

    datos = [] # Almacena los nombres de los clientes.
    def __init__(self, master, id, cl_cargado):
        self.master = master
        self.id = id
        self.cl_cargado = cl_cargado
    
        self.identificador = CRUD() # Instancia de la clase "Crud_tabla_clientes"
                                    # ... Módulo bd_clientes.py
        self.top = Toplevel()
        self.top.title("Seleccionar cliente")
        self.top.grid_propagate(0)

        self.valor_cliente = StringVar() # Nombre del cliente seleccionado en el Combobox.
        
        #----Frame que contiene los widgets definidos abajo---------------
        ventana=ttk.Frame(self.top, relief="solid")
        ventana.configure(width=400, height=250)
        ventana.pack()
        #---------------
        
        #--------Widgets que se albergan en el Frame "ventana"--------------------

        etiqueta_selecciona = ttk.Label(ventana, text="Selecciona un cliente:", font=("arial", 12))
        etiqueta_selecciona.place(x=50, y=10)

        listado_clientes = ttk.Combobox(ventana, values=self.carga_id(), width=30, height=10, textvariable=self.valor_cliente)
        listado_clientes.place(x=50, y=30)
        # Combobox recibe una lista[] con los nombres de los clientes registrados en la base de datos.

        b_cargar = ttk.Button(ventana, text="Aceptar", style="C.TButton",command=lambda: [V_CLIENTE.cargar_datos_cliente(self.sel_id(dato=self.valor_cliente.get())),self.on_close()])
        b_cargar.place(x=260, y=28)
        # b_cargar envía el nombre del cliente seleccionado a la función que carga los datos del cliente en el formulario.

        info_cliente = ttk.Label(ventana, text="")
        info_cliente.place(x=50, y=100)
        listado_clientes.bind("<<ComboboxSelected>>", lambda _ : info_cliente.config(text=f"Info:\r '{listado_clientes.get()}'"))
        # info_cliente muestra una pequeña información del cliente seleccionado.
        # Puede ser útil para que el usuario pueda saber si es el cliente que está buscando. **Hay que afinarla un poco más.

        V_CLIENTE.cargar_cliente.config(state='disable')  # Deshabilita el botón "VER CLIENTE"
        V_CLIENTE.editar_cliente.config(state='disable')  # Deshabilita el botón "EDITAR"

        self.top.protocol("WM_DELETE_WINDOW", self.on_close)
    

    
    def carga_id(self):
    # Retorna los nombres de los clientes que están registrados en la BD.
    # Se almacenan en una lista que será utilizada en el Combobox "listado_clientes".
    # Ejemplo: ['Cliente 1', 'Cliente 2', 'Cliente 3',...]
        self.datos = []
        self.identificador.ver_todo() # Genera un diccionario con el nombre y nº cliente.
        # {'14321839': 'cliente 1', '14321838': 'cliente 2', '54773359': 'cliente 3',...}
        for v in self.identificador.dicc_clientes.values():
            self.datos.append(v)     
        return self.datos # Retorna solo los nombres de los clientes.
    
    def sel_id(self, dato):
    # Esta función se pasa como argumento de la función "cargar_datos_cliente" que se 
    # activa al pulsar el botón "Cargar" tras seleccionar un cliente.
    # Retorna el número del cliente seleccionado.
        
        for k, v in self.identificador.dicc_clientes.items():
            if dato == v:
                return k  # '14321839' -> nº de cliente

    def cerrar_ventana(self):
    # La ventana se destruye tras seleccionar un cliente.
        self.top.destroy()
        V_CLIENTE.cargar_cliente.config(state='normal')  # Habilita el botón "VER CLIENTE" de la ventana principal.
        V_CLIENTE.editar_cliente.config(state='normal')  # Habilita el botón "EDITAR" de la ventana principal.
    
    def on_close(self):  
        # Función que se llama cuando se pulsa el botón de cierre
        # del gestor de ventanas 
                
        self.top.destroy()  # Destruye la ventana Toplevel de selección cliente
        V_CLIENTE.cargar_cliente.config(state='normal')  # Habilita el botón "VER CLIENTE" de la ventana principal.
        V_CLIENTE.editar_cliente.config(state='normal')  # Habilita el botón "EDITAR" de la ventana principal.

#-------- FIN DE LA CLASE "TOPlevel_Selec_Cliente" ---------------------------
#-----------------------------------------------------------------------------

    

if __name__=="__main__":
    root = Tk()
    root.title('Nuevo cliente.')
    root.resizable(1,1)
    V_CLIENTE = Gestion_Clientes(root)

    root.mainloop()