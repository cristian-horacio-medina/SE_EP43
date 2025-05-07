import os
import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
from main import FormularioCarga  # Importa el formulario de carga desde main.py

DB_PATH = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")  # Ruta de tu base de datos
print("Ruta de la base de datos:", os.path.abspath(DB_PATH))
# --- FUNCIONES DE BACKEND ---

def verificar_login(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            hashed_guardado = resultado[0]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_guardado.encode('utf-8')):
                return True, username
        return False
    except Exception as e:
        print("Error en verificación:", e)
        return False, none

def registrar_usuario(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed.decode('utf-8')))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception as e:
        print("Error al registrar usuario:", e)
        return False

# --- FUNCIONES DE INTERFAZ ---

def login():
    username = entry_usuario.get()
    password = entry_contrasena.get()

    if verificar_login(username, password):
        messagebox.showinfo("Login exitoso", f"Bienvenido, {username}")
        root.destroy()  # Cierra la ventana de login

        # Crea la nueva ventana con el formulario
        nueva_ventana = tk.Tk()
        nueva_ventana.title("Formulario de Carga")
        nueva_ventana.geometry("960x600")
        app = FormularioCarga(nueva_ventana)
        app.grid(row=0, column=0, sticky="nsew")
        nueva_ventana.grid_rowconfigure(0, weight=1)
        nueva_ventana.grid_columnconfigure(0, weight=1)
        nueva_ventana.mainloop()  # Inicia el bucle de eventos de la nueva ventana
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")

def mostrar_ventana_registro():
    ventana_registro = tk.Toplevel(root)
    ventana_registro.title("Registrar nuevo usuario")
    ventana_registro.geometry("300x200")

    tk.Label(ventana_registro, text="Nuevo usuario").pack(pady=5)
    nuevo_usuario = tk.Entry(ventana_registro)
    nuevo_usuario.pack()

    tk.Label(ventana_registro, text="Nueva contraseña").pack(pady=5)
    nueva_contrasena = tk.Entry(ventana_registro, show="*")
    nueva_contrasena.pack()

    def registrar():
        username = nuevo_usuario.get()
        password = nueva_contrasena.get()
        if username and password:
            if registrar_usuario(username, password):
                messagebox.showinfo("Éxito", f"Usuario '{username}' registrado correctamente.")
                ventana_registro.destroy()
            else:
                messagebox.showerror("Error", f"El usuario '{username}' ya existe o hubo un problema.")
        else:
            messagebox.showwarning("Advertencia", "Completa ambos campos.")

    tk.Button(ventana_registro, text="Registrar", command=registrar).pack(pady=15)

# --- INTERFAZ PRINCIPAL ---

root = tk.Tk()
root.title("Login - Excursion")
root.geometry("300x220")

# Etiquetas y campos de entrada
tk.Label(root, text="Usuario").pack(pady=(20, 5))
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Contraseña").pack(pady=5)
entry_contrasena = tk.Entry(root, show="*")
entry_contrasena.pack()

# Botones
tk.Button(root, text="Ingresar", command=login).pack(pady=(15, 5))
#tk.Button(root, text="Registrar nuevo usuario", command=mostrar_ventana_registro).pack()

# Botón para registrar usuarios (solo lo activará admin al loguearse)
boton_registrar = tk.Button(root, text="Registrar nuevo usuario", command=mostrar_ventana_registro)
boton_registrar.pack()

# Deshabilitar el botón al inicio
boton_registrar.config(state="disabled")

# Habilitar el botón si el usuario escrito es 'admin'
def habilitar_si_admin(event):
    if entry_usuario.get().strip().lower() == "admin":
        boton_registrar.config(state="normal")
    else:
        boton_registrar.config(state="disabled")

entry_usuario.bind("<KeyRelease>", habilitar_si_admin)

root.mainloop()
