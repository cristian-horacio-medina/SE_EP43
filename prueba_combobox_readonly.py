import tkinter as tk
from tkinter import ttk

# Crear ventana
root = tk.Tk()
root.title("Ejemplo Combobox Bloqueado")

# Crear Combobox
combobox_grado = ttk.Combobox(root, values=["Primero", "Segundo", "Tercero"])
combobox_grado.set("Primero")  # Valor por defecto
combobox_grado.config(state="readonly")  # Bloquea edición pero permite seleccionar

# Función para obtener y guardar el dato
def guardar_dato():
    valor = combobox_grado.get()
    print(f"Guardando en la BD: {valor}")  # Simula el guardado

# Botón para probar la lectura del dato
btn_guardar = tk.Button(root, text="Guardar", command=guardar_dato)

# Ubicar elementos en la ventana
combobox_grado.pack(pady=10)
btn_guardar.pack()

# Ejecutar ventana
root.mainloop()
