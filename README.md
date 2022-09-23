# Interface grafica con base de datos para gestionar clientes. Python, Tkinter y SQlite3

Versión: 1.0
Fecha: 24/09/2022
Autor: Enrique Calvo Ordóñez
Email: enrique.calvoor@gmail.com

Lenguaje utilizado: Python 3
    - Módulos y Librerias: Tkinter, SQLite3

Sistema operativo utilizado: Windows 10
    
Introducción:
Este programa tiene la finalidad de ayudar a gestionar una cartera de clientes.
Tiene todas las instrucciones básicas para crear nuevos clientes, editarlos, visualizar 
y eliminar.

La finalidad de este proyecto es hacerlo crecer hasta crear una aplicación completa y funcional
en la que poder gestionar, aparte de clientes, listados de productos, ventas, ingresos y gastos.
También generar y visualizar estadísticas básicas y avanzadas.


Inicio del programa.
Módulo "ventana_nuevo_cliente.py"

El programa se inicia ejecutando el módulo "ventana_nuevo_cliente.py".
La interface gráfica aparece en pantalla y contiene todo lo necesario para empezar a crear y gestionar
la cartera de clientes.


Detalles de la interface gráfica.

DESCRIPCIÓN:

En la interface gráfica se albergan todos los "Label Entry" para introducir los datos del nuevo cliente. 
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
La interface gráfica tiene partes en las que utilizo .grid y en otras .place. Quizás no es una buena idea.
No sé como se va a ver en otras plataformas o pantallas.


MÓDULOS:
-----
ventana_nuevo_cliente.py 
(Este es el módulo principal)

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


------
ventana_ayuda.py

Clase Ayuda_Dialogo:
    Es una ventana TopLevel que detalla el uso del formulario de clientes.

Cuando el usuario pulsa el botón "AYUDA", se despliega y muestra las instrucciones de uso.


------
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

Clase Crud_Tabla_Clientes():
    Funciones:
        crear_tabla  ----------------  Crea la tabla "datos_clientes". 
        guardar_cliente_en_base -----  Guarda un nuevo cliente.
        ver_cliente    --------------  Retorna una tupla con los datos de un cliente.
        ver_todo        -------------  Retorna una lista de tuplas con todos los clientes.
        modificar_cliente  ----------  Modifica los datos del cliente.
        cliente_existe     ----------  Retorna True si el cliente existe, en caso contrario retorna False.
        resultado_consulta  ---------  Retorna el resultado exitoso o no de una consulta de guardar o actualizar datos. 
        identificador_existe  -------  Comprueba si el identificador de un cliente existe o no. Retorna True o False.
        extraer_campos    -----------  Estrae todos los campos de la tabla "datos_clientes".

------
funciones_especiales.py

Este módulo contiene cuatro funciones.
Son funciones de apoyo que, si bien no son indispensables para el buén funcionamiento del programa, 
ayudan al usuario a la hora de rellenar los datos de un nuevo cliente.

Funciones:
    creaClaveUser()    ------------ Crea un nuevo identificador de cliente.
    verifica_clave(clave)  -------- Verifica que la clave no existe en la BD.
    fechasDeRegistro()   ---------- Retorna la fecha en formato dd/mm/aa
    fecha_hoy()    ---------------- Retorna la fecha completa. "Jueves 12 de Mayo de 2022"

------

TODOS LOS MÓDULOS TIENEN LAS FUNCIONES Y CLASES DOCUMENTADAS CON MÁS DETALLE.

