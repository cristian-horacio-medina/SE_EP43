import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class LoginScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")
        self.master.geometry("300x200")

        # Etiquetas y campos de entrada
        tk.Label(master, text="Usuario:").pack(pady=5)
        self.username_entry = tk.Entry(master)
        self.username_entry.pack(pady=5)

        tk.Label(master, text="Contraseña:").pack(pady=5)
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack(pady=5)

        # Botón de login
        tk.Button(master, text="Iniciar sesión", command=self.login).pack(pady=10)

        # Crear base de datos si no existe
        self.create_user_table()

    def create_user_table(self):
        db_path = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE,
                            password TEXT,
                            role TEXT)''')
        # Insertar un usuario administrador por defecto si no existe
        cursor.execute('''INSERT OR IGNORE INTO usuarios (username, password, role)
                           VALUES ('admin', 'admin123', 'admin')''')
        conn.commit()
        conn.close()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db_path = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar credenciales
        cursor.execute("SELECT role FROM usuarios WHERE username = ? AND password = ?", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            if role == "admin":
                messagebox.showinfo("Login exitoso", "Bienvenido, Administrador.")
                self.master.destroy()
                self.open_main_app(role)
            elif role == "operador":
                messagebox.showinfo("Login exitoso", "Bienvenido, Operador.")
                self.master.destroy()
                self.open_main_app(role)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def open_main_app(self, role):
        root = tk.Tk()
        root.geometry("930x600")
        app = FormularioCarga(root)
        if role == "operator":
            # Deshabilitar funciones específicas para operadores
            app.guardar_btn.config(state="disabled")
            app.borrar_btn.config(state="disabled")
        root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
