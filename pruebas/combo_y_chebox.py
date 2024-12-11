import tkinter as tk
from tkinter import ttk

def toggle_selection(item):
    if selections[item].get():
        selected_items.add(item)
    else:
        selected_items.discard(item)
    update_combobox()

def update_combobox():
    combobox_var.set(", ".join(selected_items))

root = tk.Tk()
root.title("Combobox con tildes")

# Variable para almacenar las selecciones
combobox_var = tk.StringVar()
selections = {}
selected_items = set()

# Configuración del Combobox (simulado)
combobox = ttk.Entry(root, textvariable=combobox_var, state="readonly")
combobox.grid(row=0, column=0, padx=10, pady=10)

# Configuración del menú desplegable
menu = tk.Menu(root, tearoff=0)
items = ["Opción 1", "Opción 2", "Opción 3"]

for item in items:
    selections[item] = tk.BooleanVar(value=False)
    menu.add_checkbutton(label=item, variable=selections[item], 
                         command=lambda i=item: toggle_selection(i))

# Evento para abrir el menú
def open_menu(event):
    menu.post(event.x_root, event.y_root)

combobox.bind("<Button-1>", open_menu)

root.mainloop()
