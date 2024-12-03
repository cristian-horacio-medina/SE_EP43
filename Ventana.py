# Importar Bibliotecas
from tkinter import *
from tkinter import ttk, messagebox
from Mensaje import *
from Gestor import *

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
    miId.set("")
    miNombre.set("")
    miCargo.set("")
    miSalario.set("")


def mostrar():
    Gestor.mostrar(tree)


def salirAplicacion():
    valor = messagebox.askquestion("Salir", Mensaje.SALIR)
    root.destroy() if valor == "yes" else None

################################ Invocar Métodos CRUD ##############################


def crear():
    Gestor.crear(miNombre.get(), miCargo.get(), miSalario.get())
    limpiarMostrar()


def actualizar():
    Gestor.actualizar(miNombre.get(), miCargo.get(),
                      miSalario.get(), miId.get())
    limpiarMostrar()


def borrar():
    Gestor.borrar(miId.get())
    limpiarMostrar()


def buscar():
    Gestor.buscar(tree, miNombre.get())


def seleccionarUsandoClick(event):
    item = tree.identify('item', event.x, event.y)
    miId.set(tree.item(item, "text"))
    miNombre.set(tree.item(item, "values")[0])
    miCargo.set(tree.item(item, "values")[1])
    miSalario.set(tree.item(item, "values")[2])


################ Desarrollo de la Interfaz Grafica #############################
################################################################################
root = Tk()
root.title("APLICACION CRUD CON BASE DE DATOS")
root.configure(background='lightblue')
root.geometry("950x600")

# iconos
# Cargar imágenes
imagen_buscar = PhotoImage(file="imagenes/buscar.png")
imagen_crear = PhotoImage(file="imagenes/crear.png")
imagen_mostrar = PhotoImage(file="imagenes/mostrar.png")
imagen_actualizar = PhotoImage(file="imagenes/actualizar.png")
imagen_eliminar = PhotoImage(file="imagenes/eliminar.png")

miId = StringVar()
miNombre = StringVar()
miCargo = StringVar()
miSalario = StringVar()

################################## Tabla ################################
cabecera = ["Apellido y Nombre", "Documento", "Estudiante"]

tree = ttk.Treeview(height=10, columns=('#0', '#1', '#2'))
tree.place(x=0, y=130)
tree.column('#0', width=300)
tree.heading('#0', text=cabecera[0], anchor=CENTER)
tree.heading('#1', text=cabecera[1], anchor=CENTER)
tree.heading('#2', text=cabecera[2], anchor=CENTER)
#tree.column('#3', width=100)
#tree.heading('#3', text=cabecera[3], anchor=CENTER)
#tree.heading('#4', text=cabecera[4], anchor=CENTER)
#tree.bind("<Button-1>", seleccionarUsandoClick)
mostrar()

###################### Colocar widgets en la VISTA ######################
menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(
    label="Crear/Conectar Base de Datos", command=conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command=eliminarBBDD)
menubasedat.add_command(label="Salir", command=salirAplicacion)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Resetear Campos", command=limpiarCampos)
ayudamenu.add_command(label="Acerca", command=Gestor.mensaje)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

############## Creando etiquetas y cajas de texto ###########################
e1 = Entry(root, textvariable=miId)

l2 = Label(root, text="Nombre", background='lightblue').place(x=50, y=10)
e2 = Entry(root, textvariable=miNombre, width=50).place(x=100, y=10)

l3 = Label(root, text="Cargo", background='lightblue').place(x=50, y=40)
e3 = Entry(root, textvariable=miCargo).place(x=100, y=40)

l4 = Label(root, text="Salario", background='lightblue').place(x=280, y=40)
e4 = Entry(root, textvariable=miSalario, width=10).place(x=320, y=40)

l5 = Label(root, text="USD", background='lightblue').place(x=380, y=40)

################# Creando botones #########################################
b0 = Button(root, text="Buscar Registro", image=imagen_buscar,
            bg="orange", command=buscar).place(x=450, y=10)
b1 = Button(root, text="Crear Registro",  image=imagen_crear,
            bg="green", command=crear).place(x=50, y=85)
b2 = Button(root, text="Actualizar Registro", image=imagen_actualizar,
            bg="orange", command=actualizar).place(x=180, y=85)
b3 = Button(root, text="Mostrar Lista", image=imagen_mostrar,
            bg="orange", command=mostrar).place(x=320, y=85)
b4 = Button(root, text="Eliminar Registro", image=imagen_eliminar,
            bg="red", command=borrar).place(x=450, y=85)

root.config(menu=menubar)
root.mainloop()
