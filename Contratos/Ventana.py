# Importar Bibliotecas
import pyodbc
import os
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from Gestor import Gestor
from Mensaje import Mensaje

# Obtener el año actual
anio_actual = datetime.now().year

print("El año actual es:", anio_actual)

#################### Gestionar la Base de Datos ##############################


def conexionBBDD():
    Gestor.conexionBBDD()


def eliminarBBDD():
    Gestor.eliminarBBDD()
    limpiarMostrar()


def limpiarMostrar():
    limpiarCampos()
    mostrar()


def limpiarCampos():
    miNombre = set("")
    miAnio = set("")
    miDivision = set("")
    miDia = set("")
    miTurno = set("")
    miContratado = set("")


def mostrar():
    modulo = int(combobox_modulo.get())  # Convertir a entero
    #carrera = int(combobox_carrera.get())  # Convertir a entero
    # Obtiene el texto del combobox y divide en espacios
    carrera_texto = combobox_carrera.get()
    
    # Dividir el texto en base a ':' y extraer el primer elemento (id)
    carrera_id = carrera_texto.split(":")[0].strip()
    
    # Convertir a entero
    carrera = int(carrera_id)
    Gestor.mostrar(tree, anio_actual, modulo, carrera)


def salirAplicacion():
    valor = messagebox.askquestion("Salir", Mensaje.SALIR)
    root.destroy() if valor == "yes" else None

################################ Invocar Métodos CRUD ##############################


def crear():
    Gestor.crear(miNombre.get(), miCargo.get(), miSalario.get())
    limpiarMostrar()


def actualizar():
    if isinstance(miDivision, StringVar) and isinstance(miComisionId, StringVar):
        division = miDivision.get()
        comision_id = miComisionId.get()

        if division and comision_id:
            try:
                # Asegúrate de pasar ambos parámetros
                Gestor.actualizar(comision_id, division)
                limpiarMostrar()
            except Exception as e:
                messagebox.showerror("Error al actualizar", str(e))
        else:
            messagebox.showwarning("Advertencia", "La división y la comisión no pueden estar vacías.")
    else:
        messagebox.showerror("Error", "La división o la comisión no están definidas correctamente.")


def borrar():
    Gestor.borrar(miId.get())
    limpiarMostrar()


def buscar():
    criterio = miNombre.get()  # Obtener el criterio de búsqueda
    modulo = int(combobox_modulo.get())  # Convertir a entero
    #carrera = int(combobox_carrera.get())  # Convertir a entero
    # Obtiene el texto del combobox y divide en espacios
    carrera_texto = combobox_carrera.get()
    
    # Dividir el texto en base a ':' y extraer el primer elemento (id)
    carrera_id = carrera_texto.split(":")[0].strip()
    
    # Convertir a entero
    carrera = int(carrera_id)
    print(f"Seleccionaste Módulo: {modulo} y Carrera: {carrera}")
    if criterio:  # Comprobar que no esté vacío
        Gestor.buscar(anio_actual, modulo, carrera, criterio, tree)
    else:
        messagebox.showwarning("Advertencia", "El nombre no puede estar vacío.")

# def buscar_carreras():
    
#     modulo = int(combobox_modulo.get())  # Convertir a entero
    
#     print(f"Seleccionaste Módulo: {modulo}")
#     if modulo:  # Comprobar que no esté vacío
#         Gestor.obtener_carreras(anio_actual, modulo)
#     else:
#         messagebox.showwarning("Advertencia", "El modulo no puede estar vacío.")



def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    midocente_id.set(tree.item(item, "values")[0])
    miNombre.set(tree.item(item, "values")[1])
    miAnio.set(tree.item(item, "values")[4])
    miDivision.set(tree.item(item, "values")[5])
    miDia.set(tree.item(item, "values")[8])
    miTurno.set(tree.item(item, "values")[6])
    miContratado.set(tree.item(item, "values")[9])
    miComisionId.set(tree.item(item, "values")[3])


################ Desarrollo de la Interfaz Grafica #############################
################################################################################
root = Tk()
root.title("Contratos docentes")
root.configure(background='lightblue')
root.geometry("1250x600")

# iconos
# Cargar imágenes
imagen_buscar = PhotoImage(file="imagenes/buscar.png")
imagen_crear = PhotoImage(file="imagenes/crear.png")
imagen_mostrar = PhotoImage(file="imagenes/mostrar.png")
imagen_actualizar = PhotoImage(file="imagenes/actualizar.png")
imagen_eliminar = PhotoImage(file="imagenes/eliminar.png")

midocente_id = StringVar()
miNombre = StringVar()
miAnio = StringVar()
miDivision = StringVar()
miDia = StringVar()
miTurno = StringVar()
miContratado = StringVar()
miComisionId = StringVar()


# Definir los valores posibles para modulo y carrera
modulos = [1, 2]  # Agrega más si es necesario

#carreras = [1, 2, 3, 5, 6, 8, 9, 11, 13, 18, 27]  # Agrega las carreras disponibles aquí

# Crear Combobox para Modulo_ID
l11 = Label(root, text="Módulo", background='lightblue')
l11.place(x=700, y=10)
combobox_modulo = ttk.Combobox(root, values=modulos, state='readonly')
combobox_modulo.place(x=750, y=10)
combobox_modulo.current(0)  # Selecciona el primer módulo por defecto
# Lógica para enlazar el evento de selección
combobox_modulo.bind("<<ComboboxSelected>>", lambda e: mostrar())
# Crear Combobox para Carrera_ID
l12 = Label(root, text="Carrera", background='lightblue')
l12.place(x=700, y=40)

#Obtener las carreras desde la base de datos
carreras = Gestor.obtener_carreras(anio_actual, int(combobox_modulo.get()))
#Formatear los valores para que incluyan el ID y el nombre
combo_values = [f"{carrera[0]}: {carrera[1]}" for carrera in carreras]

combobox_carrera = ttk.Combobox(root, values=combo_values, state='readonly')
combobox_carrera.place(x=750, y=40)
combobox_carrera.current(0)  # Selecciona la primera carrera por defecto
combobox_carrera.bind("<<ComboboxSelected>>", lambda e: mostrar())


# combobox_carrera = ttk.Combobox(root, values=carreras, state='readonly')
# combobox_carrera.place(x=750, y=40)
# combobox_carrera.current(0)  # Selecciona la primera carrera por defecto
# combobox_carrera.bind("<<ComboboxSelected>>", lambda e: mostrar())

################################## Tabla ################################

# Crear scrollbar vertical
scrollbar_v = Scrollbar(root, orient=VERTICAL)
scrollbar_v.place(x=1230, y=150, height=400)  # Ajusta según sea necesario

# Crear scrollbar horizontal
# scrollbar_h = Scrollbar(root, orient=HORIZONTAL)
# scrollbar_h.place(x=20, y=550, width=1210)  # Ajusta según sea necesario

# Crear Treeview con scrollbars
tree = ttk.Treeview(height=20, columns=('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', '#10'),
                    yscrollcommand=scrollbar_v.set)  # , xscrollcommand=scrollbar_h.set
tree.place(x=20, y=150)

# Configurar scrollbars
scrollbar_v.config(command=tree.yview)
# scrollbar_h.config(command=tree.xview)

# Definir las columnas y cabeceras
cabecera = ["docente_id", "docente", "carrera", "comision_id",
            "año", "division", "turno", "materia", "dia", "contratado"]

tree.column('#0', width=0)
tree.heading('#1', text=cabecera[0], anchor=CENTER)
tree.column('#1', width=50)
tree.heading('#2', text=cabecera[1], anchor=CENTER)
tree.column('#2', width=250)
tree.heading('#3', text=cabecera[2], anchor=CENTER)
tree.column('#3', width=250)
tree.heading('#4', text=cabecera[3], anchor=CENTER)
tree.column('#4', width=0)
tree.heading('#5', text=cabecera[4], anchor=CENTER)
tree.column('#5', width=10)
tree.heading('#6', text=cabecera[5], anchor=CENTER)
tree.column('#6', width=50)
tree.heading('#7', text=cabecera[6], anchor=CENTER)
tree.column('#7', width=50)
tree.heading('#8', text=cabecera[7], anchor=CENTER)
tree.column('#8', width=350)
tree.heading('#9', text=cabecera[8], anchor=CENTER)
tree.column('#9', width=80)
tree.heading('#10', text=cabecera[9], anchor=CENTER)
tree.column('#10', width=100)

# Bind para seleccionar con click
tree.bind("<Button-1>", seleccionarUsandoClick)

# Mostrar datos en la tabla
mostrar()

###################### Colocar widgets en la VISTA ######################
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(
    label="Crear/Conectar Base de Datos", command=conexionBBDD)
# menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=Gestor.mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

############## Creando etiquetas y cajas de texto ###########################
e1 = Entry(root, textvariable=miComisionId)


l2 = Label(root, text="Nombre", background='lightblue')
l2.place(x=50, y=10)

e2 = Entry(root, textvariable=miNombre, width=50)
e2.place(x=100, y=10)

l3 = Label(root, text="docente_id", background='lightblue')
l3.place(x=50, y=40)

e3 = Entry(root, textvariable=midocente_id, width=5)
e3.place(x=100, y=40)

l4 = Label(root, text="año", background='lightblue')
l4.place(x=150, y=40)

e4 = Entry(root, textvariable=miAnio, width=10)
e4.place(x=190, y=40)

l6 = Label(root, text=f"Año: {anio_actual}", background='lightblue')
l6.place(x=620, y=10)

l7 = Label(root, text="Division", background='lightblue')
l7.place(x=220, y=40)

e7 = Entry(root, textvariable=miDivision, width=6)
e7.place(x=280, y=40)

l8 = Label(root, text="turno", background='lightblue')
l8.place(x=450, y=40)

e8 = Entry(root, textvariable=miTurno, width=15)
e8.place(x=485, y=40)

l9 = Label(root, text="día", background='lightblue')
l9.place(x=350, y=40)

e9 = Entry(root, textvariable=miDia, width=10)
e9.place(x=380, y=40)

l10 = Label(root, text="contratado", background='lightblue')
l10.place(x=540, y=40)

e10 = Entry(root, textvariable=miContratado, width=5)
e10.place(x=620, y=40)

################# Creando botones #########################################
b0 = Button(root, text="Buscar Registro", image=imagen_buscar,
            bg="orange", command=buscar).place(x=450, y=5)
#b1 = Button(root, text="Crear Registro",  image=imagen_crear,
#            bg="green", command=crear).place(x=50, y=85)
b2 = Button(root, text="Actualizar Registro", image=imagen_actualizar,
            bg="orange", command=actualizar).place(x=180, y=85)
b3 = Button(root, text="Mostrar Lista", image=imagen_mostrar,
            bg="orange", command=mostrar).place(x=320, y=85)
#b4 = Button(root, text="Eliminar Registro", image=imagen_eliminar,
#            bg="red", command=borrar).place(x=450, y=85)

root.config(menu=menubar)
root.mainloop()
