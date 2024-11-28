from tkinter import *
from tkinter.ttk import Combobox

def miFuncion():
    print("Este mensaje es del botón")

ventana = Tk()
ventana.title("Hola mundo!!!")
ventana.geometry("400x400")

lbl=Label(ventana, text="Este es un label")
lbl.pack()

lbl=Label(ventana, text="Para correr esta aplicación dándole doble click tengo que colocarle por extensión pyw")
lbl.pack()

btn=Button(ventana, text="Presionar", fg = "yellow", bg = "blue", command = miFuncion)
#puedo cambiar el aspecto del botón desde:
#fg (foreground) = "red" o bg (background) = "green"
#btn.config(fg="red", bg="black")
#o puede ser btn["fg"]="red" y btn["bg"]="white"
btn.pack()

ventana.opciones = ["Marketing","Administración de empresas","Comercio Exterior"]
ventana.cmbOpciones = Combobox(ventana, width = "40", values=ventana.opciones, state="readonly")
ventana.cmbOpciones.place(x=100, y=90)
ventana.cmbOpciones.current(0)


ventana.mainloop()
