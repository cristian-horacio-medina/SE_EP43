import tkinter as tk
import json
import os
import locale
import sys
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk
from tkinter import filedialog
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF4 import PdfFileWriter, PdfFileReader

# Establecer la localización a español (España)
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # Para sistemas UNIX
# locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')  # Para Windows


class FormularioCarga(tk.Frame):
    def __init__(self, master):
        super().__init__(master)  # Llama al constructor de tk.Frame
        self.master = master
        self.IdEXCURSION = None
        self.IdGRADO = None
        self.accion_actual = "mostrar"
        # self.rol_seleccionado = tk.StringVar()
        master.title("Formulario de Carga")

        # Inicializa los componentes
        self.crear_tabs()  # Aquí lo llamas desde la instancia, usando `self`
        # Inicializa el contador de registros
        self.contador = 1

        # Variable para insertar datos a tabla excursion
        var_tipo = tk.StringVar(value="docente")

        # Configuración de la cuadrícula principal
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.columnconfigure(3, weight=1)

    def crear_tabs(self):
        # Creamos un tab control, para ello usamos la clase Notebook
        control_tabulador = ttk.Notebook(self.master)
        # Agregamos un marco (frame) para agregar dentro del tab y organizar elementos
        tabulador1 = tk.Frame(control_tabulador)
        # Agregamos el tabulador al control de tabuladores
        control_tabulador.add(tabulador1, text='Datos Anexo V')
        # Creamos los componentes del tabulador1 (mueve los elementos aquí)
        self.crear_componentes_tabulador1(tabulador1)
        # Creamos un segundo tabulador
        tabulador2 = tk.LabelFrame(control_tabulador, text='Contenido')
        control_tabulador.add(tabulador2, text='Datos Anexo VI')
        self.crear_componentes_tabulador2(tabulador2)
        # Colocamos el control de tabuladores en el contenedor principal
        control_tabulador.grid(row=0, column=0, columnspan=2)

    def crear_componentes_tabulador1(self, tabulador):
        # Agregar una etiqueta y un campo de entrada para 'Lugar'
        tk.Label(tabulador, text="Lugar:").grid(
            row=1, column=0, sticky='w', padx=5, pady=5)
        self.lugar_entry = tk.Entry(tabulador, width=33)
        self.lugar_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.lugar_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.lugar_entry, 33, tabulador))

        # Agregar una etiqueta y un campo de entrada para 'Localidad'
        tk.Label(tabulador, text="Localidad:").grid(
            row=1, column=2, sticky='w', padx=(5, 0), pady=5)
        self.localidad_entry = tk.Entry(tabulador, width=23)
        self.localidad_entry.grid(row=1, column=2, sticky='e', padx=(0, 5), pady=5)
        self.localidad_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.localidad_entry, 33, tabulador))

        
        
        tk.Label(tabulador, text="Grado:").grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.combobox_grado = ttk.Combobox(
            tabulador, state="readonly", width=10)
        self.combobox_grado.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.combobox_excursion = ttk.Combobox(
            tabulador, state="readonly", width=40)
        # Cambia la fila y columna según sea necesario
        self.combobox_excursion.grid(
            row=5, column=3, sticky="e", padx=2, pady=2)
        self.combobox_excursiones()
        # Asociar el evento de selección al método cargar_desde_sqlite
        self.combobox_excursion.bind("<<ComboboxSelected>>", self.cargar_desde_sqlite)

        # Cargar datos en el Combobox
        self.cargar_grados()

        # Agregar una etiqueta y un campo de entrada para 'Fecha'
        tk.Label(tabulador, text="Fecha de salida:").grid(
            row=0, column=1, sticky='e', padx=5, pady=5)
        self.fecha_entry = tk.Entry(tabulador, width=15)
        self.fecha_entry.grid(row=0, column=2, sticky='w', padx=5, pady=5)

        # Añadido: Evento para formatear la fecha
        self.fecha_entry.bind("<KeyRelease>", self.formatear_fecha)

        # Agregar una etiqueta y un campo de entrada para 'Apellido'
        tk.Label(tabulador, text="Apellido:").grid(
            row=2, column=0, sticky='w', padx=5, pady=2)
        self.apellido_entry = tk.Entry(tabulador, width=40)
        self.apellido_entry.grid(row=2, column=1, sticky='w', padx=5, pady=2)

        # Agregar una etiqueta y un campo de entrada para 'Nombre'
        tk.Label(tabulador, text="Nombre:").grid(
            row=2, column=1, sticky='e', padx=5, pady=2)
        self.nombre_entry = tk.Entry(tabulador, width=40)
        self.nombre_entry.grid(row=2, column=2, sticky='w', padx=5, pady=2)

        # Agregar una etiqueta y un campo de entrada para 'Documento'
        tk.Label(tabulador, text="Documento:").grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        self.documento_entry = tk.Entry(tabulador, width=20)
        self.documento_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)

        # Variable para el rol seleccionado
        self.rol_seleccionado = tk.StringVar(value="Estudiante")

        # Radiobuttons para seleccionar rol
        tk.Radiobutton(tabulador, text="Estudiante", variable=self.rol_seleccionado,
                       value="Estudiante").grid(row=4, column=0)

        tk.Radiobutton(tabulador, text="Docente", variable=self.rol_seleccionado,
                       value="Docente", command=self.mostrar_combobox).grid(row=4, column=1)
        tk.Radiobutton(tabulador, text="No Docente", variable=self.rol_seleccionado,
                       value="No Docente").grid(row=4, column=2) 
        tk.Label(tabulador, text="Seleccione una excursión").grid(row=4, column=3, sticky='ew', padx=5, pady=5)

        # Crear el Combobox para "Responsable" o "Reemplazante"
        self.combobox_docente = ttk.Combobox(
            tabulador, values=["Responsable", "Reemplazante"])
        self.combobox_docente.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        self.combobox_docente.config(state="disabled")

        # Botón para nueva excursión
        self.agregar_btn = tk.Button(
            tabulador, text="Nueva excursión", command=self.guardar_y_reiniciar)
        self.agregar_btn.grid(row=0, column=3, sticky='ew')
        self.agregar_btn.config(bg="green", fg="white", font=("Arial", 10, "bold"))
        
        #Botón eliminar excursión
        self.eliminar_excursion_btn = tk.Button(
            tabulador, text="Eliminar excursión", command=self.eliminar_excursion)
        self.eliminar_excursion_btn.grid(row=2, column=3, sticky='ew')
        self.eliminar_excursion_btn.config(bg="red", fg="white", font=("Arial", 10, "bold"))

        # Botón para agregar registro
        self.agregar_btn = tk.Button(
            tabulador, text="Agregar", command=self.agregar, bg="green", fg="white", font=("Arial", 10, "bold"))
        self.agregar_btn.grid(row=6, column=0, sticky='ew')

        

        # Botón para mostrar o actualizar
        self.mostrar_button = tk.Button(
            tabulador, text="Modificar seleccionado", command=self.mostrar_o_actualizar, bg="blue", fg="white", font=("Arial", 10, "bold"))
        self.mostrar_button.grid(row=6, column=2, sticky='ew')
        
        # Botón para modificar grado
        self.modificar_grado_button = tk.Button(
            tabulador, text="Modificar grado", command=self.modificar_grado, bg="grey", fg="white", font=("Arial", 10, "bold"))
        self.modificar_grado_button.grid(row=6, column=3, sticky='ew')


        # Botones para borrar, guardar, cargar, generar PDF y salir
        self.borrar_btn = tk.Button(
            tabulador, text="Borrar seleccionado", command=self.borrar, borderwidth=2, relief="solid")
        self.borrar_btn.grid(row=6, column=1, sticky='ew')
        self.borrar_btn.config(fg="red", font=("Arial", 10, "bold"), highlightbackground="red", highlightthickness=2)

        self.guardar_btn = tk.Button(
            tabulador, text="Guardar excursión", command=self.guardar_sqlite)
        self.guardar_btn.grid(row=9, column=1, sticky='ew')

        # self.cargar_btn = tk.Button(
        #     tabulador, text="Cargar excursión", command=self.cargar_desde_sqlite)
        # self.cargar_btn.grid(row=9, column=2, sticky='ew')

        self.generar_pdf_btn = tk.Button(
            tabulador, text="Generar Anexo V", command=self.generar_pdf_Anexo_V)
        self.generar_pdf_btn.grid(row=9, column=2, sticky='ew')

        self.salir_btn = tk.Button(tabulador, text="Salir", command=quit)
        self.salir_btn.grid(row=10, column=2, columnspan=2, sticky='ew')

        # Botón para generar los PDFs individuales
        self.generar_pdfs_btn = tk.Button(
            tabulador, text="Generar Anexo VI", command=self.generar_pdf_Anexo_VI)
        self.generar_pdfs_btn.grid(row=9, column=3, sticky='ew')

        tabulador.grid_rowconfigure(6, weight=1)  # Fila del Treeview
        tabulador.grid_columnconfigure(0, weight=1)  # Primera columna
        tabulador.grid_columnconfigure(1, weight=1)  # Segunda columna
        tabulador.grid_columnconfigure(2, weight=1)  # Tercera columna
        tabulador.grid_columnconfigure(3, weight=1)  # Cuarta columna

        # Listado (Treeview)
        self.tree = ttk.Treeview(tabulador, columns=(
            "Nº", "Apellido y Nombre", "Documento", "Estudiante", "Docente", "No Docente"), show='headings')
        self.tree.heading("Nº", text="Nº")
        self.tree.heading("Apellido y Nombre", text="Apellido y Nombre")
        self.tree.heading("Documento", text="Documento")
        self.tree.heading("Estudiante", text="Estudiante")
        self.tree.heading("Docente", text="Docente")
        self.tree.heading("No Docente", text="No Docente")

        # Ajustar ancho de columnas
        self.tree.column("Nº", width=50)
        self.tree.column("Apellido y Nombre", width=200)
        self.tree.column("Documento", width=100)
        self.tree.column("Estudiante", width=50)
        self.tree.column("Docente", width=50)
        self.tree.column("No Docente", width=50)
        self.tree.grid(row=8, column=0, columnspan=4, sticky='nsew')

        # Colocar el Treeview en una Scrollbar para cuando se expanden los datos
        tree_scroll = tk.Scrollbar(
            tabulador, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.grid(row=8, column=0, columnspan=4, sticky='nsew')
        tree_scroll.grid(row=8, column=4, sticky='ns')

    def limitar_texto(self, texto):
        return len(texto) <= 33

    def cargar_grados(self):
        try:
            db_path = os.path.join(os.path.expanduser(
                "~"), "Documents", "Excursion.db")
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT idgrado, grado || ' ' || seccion || ' ' || turno AS grado_completo FROM grado;")
            resultados = cursor.fetchall()

            self.grados = {fila[1]: fila[0]
                           for fila in resultados}  # Diccionario de grados
            self.combobox_grado["values"] = list(self.grados.keys())
            conexion.close()
        except Exception as e:
            print(f"Error al cargar los grados: {e}")

    def combobox_excursiones(self):
        try:
            # Conectar a la base de datos SQLite
            db_path = os.path.join(os.path.expanduser(
                "~"), "Documents", "Excursion.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Obtener las excursiones con su ID, lugar, fecha y grado
            cursor.execute("""
                SELECT IdEXCURSION, lugar, fecha, 
                    (SELECT grado || seccion || turno FROM grado WHERE grado.IdGRADO = excursion.IdGRADO) AS grado
                FROM excursion ORDER BY fecha
            """)
            excursiones = cursor.fetchall()

            # Crear un diccionario para mapear las opciones del Combobox al ID de la excursión
            self.excursiones = {f"{fecha}-{grado}-{lugar}": IdEXCURSION
                                for IdEXCURSION, lugar, fecha, grado in excursiones}

            # Asignar las opciones al Combobox
            self.combobox_excursion["values"] = list(self.excursiones.keys())
        except Exception as e:
            print(f"Error al cargar las excursiones: {e}")
        finally:
            # Cerrar la conexión a la base de datos
            conn.close()

    def mostrar_combobox(self):
        # Ocultar ambos Combobox
        self.combobox_docente.grid_remove()
        #self.combobox_no_docente.grid_remove()

        # Mostrar y activar el Combobox correspondiente
        if self.rol_seleccionado.get() == "Docente":
            self.combobox_docente.grid()
            self.combobox_docente.config(state="normal")
        elif self.rol_seleccionado.get() == "No Docente":
            #self.combobox_no_docente.grid()
            #self.combobox_no_docente.config(state="normal")
            pass
            
    def crear_componentes_tabulador2(self, tabulador):
        # Agregar una etiqueta y un campo de entrada para 'Lugar'
        tk.Label(tabulador, text="Nombre del Proyecto:").grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.proyecto_entry = tk.Entry(tabulador, width=50)
        self.proyecto_entry.grid(
            row=0, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.proyecto_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.proyecto_entry, 50, tabulador))

        # Agregar una etiqueta a Lugar de salida
        tk.Label(tabulador, text="Lugar de salida: E.P. Nº 43").grid(
            row=1, column=0, sticky='w', padx=5, pady=2)

        # Agregar una etiqueta y un campo de entrada para 'Fecha'
        tk.Label(tabulador, text="Fecha de salida:").grid(
            row=1, column=1, sticky='w', padx=5, pady=5)
        self.fechasalida_entry = tk.Entry(tabulador, width=15)
        self.fechasalida_entry.grid(
            row=1, column=1, sticky='w', padx=125, pady=5)
        self.fechasalida_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.fechasalida_entry, 15, tabulador))

        tk.Label(tabulador, text="Hora de salida:").grid(
            row=1, column=2, sticky='w', padx=5, pady=2)
        self.horasalida_entry = tk.Entry(tabulador, width=10)
        self.horasalida_entry.grid(
            row=1, column=2, sticky='W', padx=105, pady=2)
        self.horasalida_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.horasalida_entry, 10, tabulador))

        # Agregar una etiqueta a Lugar de salida
        tk.Label(tabulador, text="Lugar de regreso: E.P. Nº 43").grid(
            row=2, column=0, sticky='w', padx=5, pady=2)

        # Agregar una etiqueta y un campo de entrada para 'Fecha'
        tk.Label(tabulador, text="Fecha de regreso:").grid(
            row=2, column=1, sticky='w', padx=5, pady=5)
        self.fecharegreso_entry = tk.Entry(tabulador, width=15)
        self.fecharegreso_entry.grid(
            row=2, column=1, sticky='w', padx=125, pady=5)
        self.fecharegreso_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.fecharegreso_entry, 15, tabulador))

        tk.Label(tabulador, text="Hora de regreso:").grid(
            row=2, column=2, sticky='w', padx=5, pady=2)
        self.horaregreso_entry = tk.Entry(tabulador, width=10)
        self.horaregreso_entry.grid(
            row=2, column=2, sticky='W', padx=105, pady=2)
        self.horaregreso_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.horaregreso_entry, 10, tabulador))
        # Lugares de estadía
        tk.Label(tabulador, text="Lugar de estadía\n(domicilios y tel.):").grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        self.lugarestadia_entry = tk.Entry(tabulador, width=44)
        self.lugarestadia_entry.grid(
            row=3, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.lugarestadia_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.lugarestadia_entry, 44, tabulador))

        # Nombre y tel. de los acompañantes
        tk.Label(tabulador, text="Nombres y tel.\nde acompañantes:").grid(
            row=4, column=0, sticky='w', padx=5, pady=5)
        self.datosacompañantes_entry = tk.Entry(tabulador, width=43)
        self.datosacompañantes_entry.grid(
            row=4, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.datosacompañantes_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.datosacompañantes_entry, 43, tabulador))
        # Empresa y/o empresas contratadas
        tk.Label(tabulador, text="Empresa/s contratada/s\n(nombre, dirección, tel.:").grid(
            row=5, column=0, sticky='w', padx=5, pady=5)
        self.empresacontratada_entry = tk.Entry(tabulador, width=102)
        self.empresacontratada_entry.grid(
            row=5, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.empresacontratada_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.empresacontratada_entry, 102, tabulador))

        # Otros datos de la infraestructura disponible
        tk.Label(tabulador, text="Otros datos de la\ninfraestructura disponible:").grid(
            row=6, column=0, sticky='w', padx=5, pady=5)
        self.datosinfraestructura_entry = tk.Entry(tabulador, width=124)
        self.datosinfraestructura_entry.grid(
            row=6, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.datosinfraestructura_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.datosinfraestructura_entry, 124, tabulador))

        # Hospitales y centros asistenciales cercanos\n(direcciones y teléfonos)
        tk.Label(tabulador, text="Hospitales y centros asist.\ncercanos(direcciones y tel.:").grid(
            row=7, column=0, sticky='w', padx=5, pady=5)
        self.hospitales_entry = tk.Entry(tabulador, width=98)
        self.hospitales_entry.grid(
            row=7, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.hospitales_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.hospitales_entry, 98, tabulador))

        # Otros datos de la interés
        tk.Label(tabulador, text="Otros datos de interés:").grid(
            row=8, column=0, sticky='w', padx=5, pady=5)
        self.otrosdatos_entry = tk.Entry(tabulador, width=124)
        self.otrosdatos_entry.grid(
            row=8, column=1, columnspan=2, sticky='w', padx=5, pady=5)
        self.otrosdatos_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.otrosdatos_entry, 137, tabulador))

        # Botón para actualizar el Label con el dato ingresado en Entry
        self.btn_actualizar = tk.Button(
            tabulador, text="Guardar", command=self.guardar_sqlite)
        self.btn_actualizar.grid(row=10, column=1, sticky='e', padx=5, pady=5)

    def mostrar_advertencia(self, texto):

        messagebox.showwarning("Advertencia", texto)

    def limitar_caracteres(self, entry, limite, tabulador):
        texto = entry.get()
        if len(texto) > limite:
            entry.delete(limite, tk.END)
            self.mostrar_advertencia(
                f"El límite de {limite} caracteres ha sido superado.")

    def formatear_fecha(self, event):  # Nuevo método para formatear la fecha
        fecha = self.fecha_entry.get().replace("/", "")
        if len(fecha) >= 2:
            fecha = fecha[:2] + "/" + fecha[2:]
        if len(fecha) >= 5:
            fecha = fecha[:5] + "/" + fecha[5:]
        self.fecha_entry.delete(0, tk.END)
        self.fecha_entry.insert(0, fecha)

    def agregar(self):
        apellido = self.apellido_entry.get()
        nombre = self.nombre_entry.get()
        documento = self.documento_entry.get()
        rol = self.rol_seleccionado.get()

        # Determina el Combobox adecuado basado en el rol
        if rol == "Docente":
            if not self.combobox_docente.get():  # Si no se seleccionó un valor en el combobox
                messagebox.showwarning(
                    "Advertencia", "Por favor, seleccione 'Responsable' o 'Reemplazante' para Docente.")
                return
            rol_seleccionado = self.combobox_docente.get()  # Obtener el valor seleccionado
        elif rol == "No Docente":
            pass
            # if not self.combobox_no_docente.get():  # Si no se seleccionó un valor en el combobox
            #     messagebox.showwarning(
            #         "Advertencia", "Por favor, seleccione 'Responsable' o 'Reemplazante' para No Docente.")
            #     return
            # rol_seleccionado = self.combobox_no_docente.get()  # Obtener el valor seleccionado
        else:
            pass
            rol_seleccionado = rol  # Para Estudiante, usamos directamente el valor del Radiobutton

        # Verifica que los campos requeridos estén completos
        if apellido and nombre and documento:
            apellido_nombre = f"{apellido}, {nombre}"
            estudiante = "X" if rol == "Estudiante" else ""
            docente = rol_seleccionado if rol == "Docente" else ""
            no_docente = "X"  if rol == "No Docente" else ""  #rol_seleccionado

            # Inserta los datos en el Treeview
            self.tree.insert("", "end", values=(
                self.contador, apellido_nombre, documento, estudiante, docente, no_docente))
            self.contador += 1
            self.limpiar()
        else:
            messagebox.showwarning(
                "Advertencia", "Por favor, complete todos los campos.")

    def limpiar(self):
        # Limpiar los campos de entrada
        self.combobox_grado.set("")
        self.localidad_entry.delete(0, tk.END)
        self.apellido_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.documento_entry.delete(0, tk.END)
        self.rol_seleccionado.set("")
        # Ensure no undefined combobox is referenced
        if hasattr(self, 'combobox_rol'):
            self.combobox_rol.set("")
            self.combobox_rol.grid_remove()  # Ocultar el combobox después de agregar

    

    def borrar(self):
        """
        Deletes the selected item from the Treeview and the database.
        """
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            values = item['values']
            documento = values[2]

            # Delete from Treeview
            self.tree.delete(selected_item)

            # Delete from database
            db_path = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM alumnos WHERE DNI = ?", (documento,))
                cursor.execute("DELETE FROM acompanantes WHERE DNI = ?", (documento,))
                conn.commit()
                messagebox.showinfo("Éxito", "Registro borrado correctamente.")
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"No se pudo borrar el registro: {e}")
            finally:
                conn.close()
        else:
            messagebox.showwarning("Advertencia", "No se ha seleccionado ningún elemento para borrar.")
    def mostrar_o_actualizar(self):
        """
        Handles the modification or update of a selected item in the Treeview.
        """
        item_id = self.tree.selection()
        if item_id:
            if self.accion_actual == "mostrar":
                # Obtener los valores del Treeview
                info = self.tree.item(item_id, 'values')
                apellido_nombre = info[1]
                documento = info[2]
                docente = info[4]
                no_docente = info[5]

                # Desconcatenar Apellido y Nombre
                apellido, nombre = apellido_nombre.split(', ')

                # Cargar los valores en los Entry
                self.apellido_entry.delete(0, tk.END)
                self.apellido_entry.insert(0, apellido)

                self.nombre_entry.delete(0, tk.END)
                self.nombre_entry.insert(0, nombre)

                self.documento_entry.delete(0, tk.END)
                self.documento_entry.insert(0, documento)

                # Cargar los valores en los Combobox si aplican
                if docente:
                    self.rol_seleccionado.set("Docente")
                    self.combobox_docente.set(docente)
                    self.combobox_docente.config(state="normal")  # Habilitar el combobox
                elif no_docente:
                    self.rol_seleccionado.set("No Docente")
                else:
                    self.rol_seleccionado.set("Estudiante")

                # Cambiar el texto del botón a "Actualizar"
                self.mostrar_button.config(
                    text="Actualizar", bg="green", fg="white", font=("Arial", 10, "bold"))
                self.accion_actual = "actualizar"  # Cambiar estado a actualizar
            else:
                # Obtener los nuevos valores de los Entry
                nuevo_apellido = self.apellido_entry.get()
                nuevo_nombre = self.nombre_entry.get()
                nuevo_documento = self.documento_entry.get()
                nuevo_rol = self.rol_seleccionado.get()

                # Concatenar Apellido y Nombre
                nuevo_apellido_nombre = f"{nuevo_apellido}, {nuevo_nombre}"

                # Determinar el valor correspondiente según el rol
                nuevo_docente = self.combobox_docente.get() if nuevo_rol == "Docente" else ""
                nuevo_no_docente = "X" if nuevo_rol == "No Docente" else ""
                nuevo_estudiante = "X" if nuevo_rol == "Estudiante" else ""

                # Actualizar el registro en el Treeview si se seleccionó un elemento
                self.tree.item(item_id, values=(
                    self.tree.index(item_id) + 1,
                    nuevo_apellido_nombre,
                    nuevo_documento,
                    nuevo_estudiante,
                    nuevo_docente,
                    nuevo_no_docente,
                ))

                # Limpiar los Entry y Combobox
                self.limpiar()

                # Cambiar texto del botón de vuelta a "Modificar"
                self.mostrar_button.config(
                    text="Modificar seleccionado", bg="blue", fg="white", font=("Arial", 10, "bold"))
                self.accion_actual = "mostrar"

                # Guardar cambios
                self.guardar_sqlite()
        else:
            messagebox.showwarning(
                "Advertencia", "No se ha seleccionado ningún elemento del listado para modificar.")

    def modificar_grado(self):
        # Desbloquear el combobox_grado para permitir la selección
        self.combobox_grado.config(state="normal")
        if self.IdEXCURSION:
            # Obtener el grado actualmente seleccionado en la base de datos
            grado_actual = self.combobox_grado.get()
            if not grado_actual:
                messagebox.showwarning("Advertencia", "Por favor, selecciona un grado válido.")
                return

            # Confirmar si desea modificar el grado
            confirmacion = messagebox.askyesno("Confirmación", f"El grado actual es '{grado_actual}'. ¿Deseas modificarlo?")
            if not confirmacion:
                # Si no desea modificar, bloquear nuevamente el combobox y salir
                self.combobox_grado.config(state="disabled")
                return

            # Permitir al usuario seleccionar un nuevo grado
            messagebox.showinfo("Información", "Selecciona un nuevo grado en el Combo y se guardará en la base de datos")
            
            # Asociar evento para guardar el nuevo grado seleccionado
            self.combobox_grado.bind("<<ComboboxSelected>>", self.actualizar_grado)
        else:
            messagebox.showwarning("Advertencia", "No se ha cargado ninguna excursión para modificar el grado.")

    def actualizar_grado(self, event=None):
        # Obtener el nuevo grado seleccionado
        nuevo_grado = self.combobox_grado.get()
        if not nuevo_grado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un grado válido.")
            return

        # Obtener el ID del nuevo grado
        nuevo_IdGRADO = self.grados.get(nuevo_grado)
        if not nuevo_IdGRADO:
            messagebox.showerror("Error", "No se pudo obtener el ID del grado seleccionado.")
            return

        # Actualizar el grado en la base de datos
        try:
            db_path = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE excursion SET IdGRADO = ? WHERE IdEXCURSION = ?", (nuevo_IdGRADO, self.IdEXCURSION))
            conn.commit()
            self.IdGRADO = nuevo_IdGRADO  # Actualizar el ID del grado en la instancia
            messagebox.showinfo("Éxito", "El grado se actualizó correctamente.")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo actualizar el grado: {e}")
        finally:
            conn.close()

        # Bloquear nuevamente el combobox_grado
        self.combobox_grado.config(state="disabled")
        # Desvincular el evento para evitar múltiples actualizaciones
        self.combobox_grado.unbind("<<ComboboxSelected>>")

        # Actualizar la lista de excursiones en el combobox
        self.actualizar_lista_excursiones()
    def guardar_sqlite(self):
        # Obtén los registros desde el Treeview
        registros = [self.tree.item(child)["values"]
                     for child in self.tree.get_children()]
        print("Contenido de registros:", registros)

        # Obtener valores de los campos de entrada (TextBox)
        lugar = self.lugar_entry.get()
        localidad = self.localidad_entry.get()
        fecha = self.fecha_entry.get()
        nombre_proyecto = self.proyecto_entry.get()
        fecha_salida = self.fechasalida_entry.get()
        hora_salida = self.horasalida_entry.get()
        fecha_regreso = self.fecharegreso_entry.get()
        hora_regreso = self.horaregreso_entry.get()
        lugar_estadia = self.lugarestadia_entry.get()
        datos_acompanantes = self.datosacompañantes_entry.get()
        empresa_contratada = self.empresacontratada_entry.get()
        datos_infraestructura = self.datosinfraestructura_entry.get()
        hospitales = self.hospitales_entry.get()
        otros_datos = self.otrosdatos_entry.get()

        # Conectar a la base de datos SQLite
        db_path = os.path.join(os.path.expanduser(
            "~"), "Documents", "Excursion.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Crear las tablas si no existen
            cursor.execute('''CREATE TABLE IF NOT EXISTS excursion (
                                IdEXCURSION INTEGER PRIMARY KEY AUTOINCREMENT,
                                lugar TEXT,
                                localidadad TEXT,
                                fecha TEXT,
                                nombre_proyecto TEXT,
                                fecha_salida TEXT,
                                hora_salida TEXT,
                                fecha_regreso TEXT,
                                hora_regreso TEXT,
                                lugar_estadia TEXT,
                                datos_acompanantes TEXT,
                                empresa_contratada TEXT,
                                datos_infraestructura TEXT,
                                hospitales TEXT,
                                otros_datos TEXT,
                                idgrado INTEGER,
                                FOREIGN KEY(idgrado) REFERENCES grado(IdGRADO))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS alumnos (
                                IdALUMNO INTEGER PRIMARY KEY AUTOINCREMENT,
                                IdEXCURSION INTEGER,
                                apellido TEXT,
                                nombre TEXT,
                                DNI TEXT,
                                ALUMNO TEXT,
                                IdGRADO INTEGER,
                                FOREIGN KEY(IdEXCURSION) REFERENCES excursion(IdEXCURSION),
                                FOREIGN KEY(IdGRADO) REFERENCES grado(IdGRADO))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS acompanantes (
                                IdACOMPANANTES INTEGER PRIMARY KEY AUTOINCREMENT,
                                IdEXCURSION INTEGER,
                                apellido TEXT,
                                nombre TEXT,
                                DNI TEXT,
                                DOCENTE TEXT,
                                NO_DOCENTE TEXT,
                                IdGRADO INTEGER,
                                FOREIGN KEY(IdEXCURSION) REFERENCES excursion(IdEXCURSION),
                                FOREIGN KEY(IdGRADO) REFERENCES grado(IdGRADO))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS grado (
                                IdGRADO INTEGER PRIMARY KEY AUTOINCREMENT,
                                grado TEXT)''')

            if self.IdEXCURSION:
                # Actualizar los datos en la tabla excursion
                cursor.execute('''UPDATE excursion SET lugar = ?, localidad = ?, fecha = ?, nombre_proyecto = ?, fecha_salida = ?, hora_salida = ?,
                                    fecha_regreso = ?, hora_regreso = ?, lugar_estadia = ?, datos_acompanantes = ?, empresa_contratada = ?,
                                    datos_infraestructura = ?, hospitales = ?, otros_datos = ?, idgrado = ?
                                    WHERE IdEXCURSION = ?''',
                               (lugar, localidad, fecha, nombre_proyecto, fecha_salida, hora_salida, fecha_regreso,
                                hora_regreso, lugar_estadia, datos_acompanantes, empresa_contratada,
                                datos_infraestructura, hospitales, otros_datos, self.IdGRADO, self.IdEXCURSION))
            else:
                # Insertar los datos en la tabla excursion
                cursor.execute('''INSERT INTO excursion (lugar, localidad, fecha, nombre_proyecto, fecha_salida, hora_salida,
                                    fecha_regreso, hora_regreso, lugar_estadia, datos_acompanantes, empresa_contratada,
                                    datos_infraestructura, hospitales, otros_datos, idgrado)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (lugar, localidad, fecha, nombre_proyecto, fecha_salida, hora_salida, fecha_regreso,
                                hora_regreso, lugar_estadia, datos_acompanantes, empresa_contratada,
                                datos_infraestructura, hospitales, otros_datos, self.IdGRADO))

                # Obtener el ID de la excursión recién insertada
                self.IdEXCURSION = cursor.lastrowid

            # Insertar o actualizar los registros de alumnos y acompañantes
            for registro in registros:
                apellido_nombre = str(registro[1]).strip()
                apellido_nombre = apellido_nombre.replace(',', '')
                partes = apellido_nombre.split(' ', 1)
                apellido = partes[0]
                nombre = partes[1] if len(partes) > 1 else ""
                dni = registro[2]
                es_estudiante = str(registro[3]).strip()
                docente = str(registro[4]).strip() if registro[4] else ""
                no_docente = str(registro[5]).strip() if registro[5] else ""

                if es_estudiante == "X":
                    cursor.execute("""
                        INSERT OR REPLACE INTO alumnos (IdALUMNO, apellido, nombre, DNI, ALUMNO, IdEXCURSION, IdGRADO)
                        VALUES ((SELECT IdALUMNO FROM alumnos WHERE DNI = ? AND IdEXCURSION = ?), ?, ?, ?, ?, ?, ?)
                    """, (dni, self.IdEXCURSION, apellido, nombre, dni, 'X', self.IdEXCURSION, self.IdGRADO))

                if docente:
                    cursor.execute("""
                        INSERT OR REPLACE INTO acompanantes (IdACOMPANANTES, apellido, nombre, DNI, DOCENTE, IdEXCURSION)
                        VALUES ((SELECT IdACOMPANANTES FROM acompanantes WHERE DNI = ? AND IdEXCURSION = ?), ?, ?, ?, ?, ?)
                    """, (dni, self.IdEXCURSION, apellido, nombre, dni, docente, self.IdEXCURSION))

                if no_docente:
                    cursor.execute("""
                        INSERT OR REPLACE INTO acompanantes (IdACOMPANANTES, apellido, nombre, DNI, NO_DOCENTE, IdEXCURSION)
                        VALUES ((SELECT IdACOMPANANTES FROM acompanantes WHERE DNI = ? AND IdEXCURSION = ?), ?, ?, ?, ?, ?)
                    """, (dni, self.IdEXCURSION, apellido, nombre, dni, no_docente, self.IdEXCURSION))

            print(self.IdEXCURSION)
            conn.commit()
            messagebox.showinfo(
                "Éxito", "Datos guardados correctamente en la base de datos.")
            self.combobox_grado.config(state="disabled")
            #self.combobox_grado.set("")
        except Exception as e:
            conn.rollback()
            messagebox.showerror(
                "Error", f"No se pudo guardar en la base de datos: {e}")
        finally:
            conn.close()

    def eliminar_excursion(self):
        # Verificar si hay una excursión seleccionada
        excursion_seleccionada = self.combobox_excursion.get()
        if not excursion_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una excursión.")
            return

        # Obtener el ID de la excursión seleccionada
        IdEXCURSION = self.excursiones.get(excursion_seleccionada)

        # Confirmar la eliminación
        confirmacion = messagebox.askyesno(
            "Confirmación", "¿Estás seguro de que deseas eliminar esta excursión?")
        if not confirmacion:
            return

        # Eliminar la excursión de la base de datos
        try:
            db_path = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM excursion WHERE IdEXCURSION = ?", (IdEXCURSION,))
            conn.commit()
            messagebox.showinfo("Éxito", "Excursión eliminada correctamente.")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo eliminar la excursión: {e}")
        finally:
            conn.close()
        
        # Actualizar la lista de excursiones
        self.actualizar_lista_excursiones()

        # Limpiar el formulario
        self.reiniciar_formulario()

    def actualizar_lista_excursiones(self):
        try:
            # Recargar las excursiones desde la base de datos
            self.combobox_excursiones()
            # Limpiar el Combobox
            self.combobox_excursion.set("")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la lista de excursiones: {e}")


    def guardar_y_reiniciar(self):
        #self.guardar_sqlite()
        self.reiniciar_formulario()
        self.combobox_grado.focus()  # Ubica el cursor en el campo Lugar

    def cargar_desde_sqlite(self, event=None):
        # Verificar si hay una excursión seleccionada
        excursion_seleccionada = self.combobox_excursion.get()

        if not excursion_seleccionada:
            messagebox.showwarning(
                "Advertencia", "Por favor, selecciona una excursión.")
            return

        # Guardar el ID de la excursión en la instancia
        self.IdEXCURSION = self.excursiones.get(
            excursion_seleccionada)  # Ahora sí se guarda bien
        print(f"IdEXCURSION cargado: {self.IdEXCURSION}")  # Debug

        # Ruta fija de la base de datos
        db_path = os.path.join(os.path.expanduser(
            "~"), "Documents", "Excursion.db")

        try:
            # Conexión a la base de datos
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Obtener los datos de la excursión seleccionada
            cursor.execute("""
                SELECT lugar, localidad, fecha, nombre_proyecto, fecha_salida, hora_salida,
                    fecha_regreso, hora_regreso, lugar_estadia, datos_acompanantes,
                    empresa_contratada, datos_infraestructura, hospitales, otros_datos, IdGRADO
                FROM excursion
                WHERE IdEXCURSION = ?
            """, (self.IdEXCURSION,))
            excursion = cursor.fetchone()

            if not excursion:
                messagebox.showerror(
                    "Error", "No se encontraron datos en la tabla principal.")
                return

            # Cargar datos en los Entry
            entries = [
                self.lugar_entry,  self.localidad_entry,  self.fecha_entry,  self.proyecto_entry,
                self.fechasalida_entry, self.horasalida_entry,
                self.fecharegreso_entry, self.horaregreso_entry,
                self.lugarestadia_entry, self.datosacompañantes_entry,
                self.empresacontratada_entry, self.datosinfraestructura_entry,
                self.hospitales_entry, self.otrosdatos_entry
            ]

            # Excluimos el valor 'IdGRADO' que está al final
            for i, value in enumerate(excursion[:-1]):
                entries[i].delete(0, tk.END)
                entries[i].insert(0, value if value is not None else "")

            # Obtener la descripción del grado usando IdGRADO
            IdGRADO = excursion[-1]  # El último valor en la tupla es 'IdGRADO'
            print(f"IdGRADO obtenido: {IdGRADO}")
            self.IdGRADO = IdGRADO  # Guardar IdGRADO en la instancia
            cursor.execute("""
                SELECT grado || seccion || turno 
                FROM grado 
                WHERE IdGRADO = ?
            """, (IdGRADO,))
            grado_desc = cursor.fetchone()

            if grado_desc:
                # Cargar la descripción del grado en el combo_grado
                self.combobox_grado.set(
                    grado_desc[0] if grado_desc[0] is not None else "")
            else:
                self.combobox_grado.set("")

            # Bloquear el ComboBox para evitar cambios accidentales
            self.combobox_grado.config(state="disabled")

            # Limpiar Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Consulta para Treeview
            cursor.execute("""
                SELECT 
                    alumnos.apellido || ', ' || alumnos.nombre AS Apellido_Nombre,
                    alumnos.DNI AS DNI, 
                    "X" AS Alumno, 
                    "" AS Docente, 
                    "" AS NoDocente
                FROM 
                    alumnos
                INNER JOIN 
                    excursion ON alumnos.IdEXCURSION = excursion.IdEXCURSION
                WHERE 
                    excursion.IdEXCURSION = ?
                
                UNION ALL
                
                SELECT 
                    acompanantes.apellido || ', ' || acompanantes.nombre AS Apellido_Nombre, 
                    acompanantes.DNI AS DNI, 
                    "" AS Alumno, 
                    CASE WHEN acompanantes.DOCENTE IS NOT NULL THEN acompanantes.DOCENTE ELSE '' END AS Docente,
                    CASE WHEN acompanantes.NO_DOCENTE IS NOT NULL THEN acompanantes.NO_DOCENTE ELSE '' END AS NoDocente
                FROM 
                    acompanantes
                INNER JOIN 
                    excursion ON acompanantes.IdEXCURSION = excursion.IdEXCURSION
                WHERE 
                    excursion.IdEXCURSION = ?
                ORDER BY 
                    Alumno DESC, 
                    Apellido_Nombre ASC
            """, (self.IdEXCURSION, self.IdEXCURSION))
            registros = cursor.fetchall()

            for registro in registros:
                # Agregar un valor vacío al inicio de cada registro
                registro_desplazado = ("",) + registro
                self.tree.insert("", "end", values=registro_desplazado)

            messagebox.showinfo("Éxito", "Registros cargados correctamente.")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error al cargar los datos desde {db_path}: {e}")
        finally:
            if conn:
                conn.close()

    def get_resource_path(self, relative_path):
        # Resuelve la ruta de los recursos en modo empaquetado o en desarrollo
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    
    def generar_pdf_Anexo_V(self):
        fecha = self.fecha_entry.get()

        db_path = os.path.join(os.path.expanduser(
            "~"), "Documents", "Excursion.db")

        # Conexión a la base de datos
        conexion = sqlite3.connect(db_path)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()

        # La consulta SQL que proporcionaste
        consulta = """
        SELECT DISTINCT
            alumnos.apellido || ' ' || alumnos.nombre AS Apellido_Nombre,
            alumnos.DNI AS DNI,
            'X' AS Alumno,
            '' AS Docente,
            '' AS NoDocente
        FROM
            alumnos
        INNER JOIN
            excursion ON alumnos.IdEXCURSION = excursion.IdEXCURSION
        WHERE
            excursion.fecha = ?

        UNION ALL

        SELECT DISTINCT
            acompanantes.apellido || ' ' || acompanantes.nombre AS Apellido_Nombre,
            acompanantes.DNI AS DNI,
            '' AS Alumno,
            IFNULL(acompanantes.DOCENTE, '') AS Docente,
            IFNULL(acompanantes.NO_DOCENTE, '') AS NoDocente
        FROM
            acompanantes
        INNER JOIN
            excursion ON acompanantes.IdEXCURSION = excursion.IdEXCURSION
        WHERE
            excursion.fecha = ?
        ORDER BY 
                    Alumno DESC, 
                    Apellido_Nombre ASC    
        """

        # Ejecuta la consulta
        cursor.execute(consulta, (fecha, fecha))

        # Recupera todos los resultados de la consulta
        registros = []
        for row in cursor.fetchall():
            registro = {
                'Apellido_Nombre': row['Apellido_Nombre'],
                'DNI': row['DNI'],
                'Alumno': row['Alumno'],
                'Docente': row['Docente'],
                'NoDocente': row['NoDocente']
            }
            registros.append(registro)

        # Ordenar en tres grupos: Estudiantes, Docentes, No Docentes, y luego alfabéticamente en cada grupo
        estudiantes = sorted(
            [r for r in registros if r['Alumno'] == "X"], key=lambda x: x['Apellido_Nombre'])
        docentes = sorted([r for r in registros if r['Docente']
                          != ""], key=lambda x: x['Apellido_Nombre'])
        no_docentes = sorted(
            [r for r in registros if r['NoDocente'] != ""], key=lambda x: x['Apellido_Nombre'])

        # Concatenar los tres grupos en el orden solicitado
        registros_ordenados = estudiantes + docentes + no_docentes
        # print(registros_ordenados)

        # Enumerar secuencialmente
        for i, registro in enumerate(registros_ordenados, start=1):
            registro['Numero'] = i

        # Generar múltiples PDFs en memoria y combinar
        self.generar_pdfs_en_memoria(registros_ordenados)

        # Cierra la conexión
        cursor.close()
        conexion.close()

    def crear_pdf_memoria(self, registros, imagen_fondo, mostrar_encabezado, posicion_inicial):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.drawImage(imagen_fondo, 0, 0,
                    width=A4[0], height=A4[1], preserveAspectRatio=True, anchor='c')

        y = posicion_inicial

        # Mostrar encabezado solo si mostrar_encabezado es True
        if mostrar_encabezado:
            Institucion_educativa = "ESCUELA PRIMARIA"
            Nº = "43"
            Distrito = "ESTEBAN ECHEVERRÍA"
            c.drawString(240, y, Institucion_educativa)
            c.drawString(480, y, Nº)
            y -= 26
            c.drawString(160, y, Distrito)
            y -= 28
            c.drawString(200, y, self.lugar_entry.get())
            y -= 1
            c.drawString(453.6, y, self.fecha_entry.get())
            y -= 80

        # Ajustar la fuente para la tabla
        c.setFont("Helvetica", 7)

        for i, registro in enumerate(registros):
            # Dibujar registros en la página
            c.drawString(90, y, str(registro['Numero']))
            c.drawString(115, y, str(registro['Apellido_Nombre']))
            c.drawString(285, y, str(registro['DNI']))
            c.drawString(350, y, "X" if registro['Alumno'] == "X" else "")
            c.drawString(390, y, str(registro['Docente']))
            c.drawString(460, y, str(registro['NoDocente']))
            y -= 23

            # Si se alcanza el límite de 18 registros por página, crear nueva página
            if (i + 1) % 18 == 0 and (i + 1) < len(registros):
                c.showPage()
                c.drawImage(
                    imagen_fondo, 0, 0, width=A4[0], height=A4[1], preserveAspectRatio=True, anchor='c')
                y = posicion_inicial

        c.save()
        # Poner el buffer en la posición inicial para su lectura posterior
        buffer.seek(0)
        return buffer

    def generar_pdfs_en_memoria(self, registros_ordenados):
        fondo_impar = self.get_resource_path("resources/Anexo_V_1.png")
        fondo_par = self.get_resource_path("resources/Anexo_V_2.png")

        posicion_impar = 632
        posicion_par = 686

        buffers = []
        archivo_num = 1

        # Generar formularios de 18 registros mientras haya más de 9 registros
        while len(registros_ordenados) > 9:
            registros_a_incluir = registros_ordenados[:18]
            buffer = self.crear_pdf_memoria(
                registros_a_incluir,
                fondo_impar,
                mostrar_encabezado=True,
                posicion_inicial=posicion_impar
            )
            buffers.append(buffer)

            # Remover los registros procesados
            registros_ordenados = registros_ordenados[18:]
            archivo_num += 1

        # Siempre generar el formulario par (9 registros o menos, o vacío)
        registros_a_incluir = registros_ordenados[:9] if registros_ordenados else []  # Puede estar vacío
        buffer = self.crear_pdf_memoria(
            registros_a_incluir,
            fondo_par,
            mostrar_encabezado=False,
            posicion_inicial=posicion_par
        )
        buffers.append(buffer)

        # Combinar los PDFs en memoria y guardar en un único archivo
        archivo_salida = os.path.join(
            os.environ["USERPROFILE"], "Documents", "Anexos_PDFs", "Anexo_V.pdf")
        self.combinar_pdfs_memoria(buffers, archivo_salida)

        messagebox.showinfo("Éxito", "El PDF combinado fue creado exitosamente en la carpeta Documentos\\Anexos_PDFs.")

        
    def combinar_pdfs_memoria(self, buffers, archivo_salida):
        escritor_pdf = PdfFileWriter()

        # Iterar sobre cada buffer en memoria y añadir sus páginas al PDF final
        for buffer in buffers:
            lector_pdf = PdfFileReader(buffer)
            for pagina in range(lector_pdf.getNumPages()):
                escritor_pdf.addPage(lector_pdf.getPage(pagina))

        # Obtener lugar y fecha de las entradas
        # Reemplazar espacios por guiones bajos
        lugar = self.lugar_entry.get().replace(" ", "_")
        # Reemplazar caracteres de fecha si es necesario
        fecha = self.fecha_entry.get().replace("/", "-")

        # Crear un nombre de archivo dinámico
        nombre_archivo = f"Anexo_V_{lugar}_{fecha}.pdf"
        # Ruta de salida en la carpeta PDFs
        pdf_path = os.path.join(
            os.environ["USERPROFILE"], "Documents", "Anexos_PDFs")
        archivo_salida = os.path.join(pdf_path, nombre_archivo)

        # Guardar el PDF combinado en el archivo de salida
        with open(archivo_salida, "wb") as archivo_final:
            escritor_pdf.write(archivo_final)

        messagebox.showinfo(
            "Éxito", f"El PDF combinado fue creado exitosamente como {nombre_archivo} en la carpeta Documentos\\Anexos_PDFs.")

    def reiniciar_formulario(self):
        self.combobox_grado.set("")
        self.localidad_entry.delete(0, tk.END)
        self.lugar_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.proyecto_entry.delete(0, tk.END)
        self.fechasalida_entry.delete(0, tk.END)
        self.horasalida_entry.delete(0, tk.END)
        self.fecharegreso_entry.delete(0, tk.END)
        self.horaregreso_entry.delete(0, tk.END)
        self.lugarestadia_entry.delete(0, tk.END)
        self.datosacompañantes_entry.delete(0, tk.END)
        self.empresacontratada_entry.delete(0, tk.END)
        self.datosinfraestructura_entry.delete(0, tk.END)
        self.hospitales_entry.delete(0, tk.END)
        self.otrosdatos_entry.delete(0, tk.END)
                    
        # Eliminar todos los registros del Treeview
        self.tree.delete(*self.tree.get_children())
        self.contador = 1  # Reiniciar contador

    # Método para obtener el nombre del mes en letras

    def obtener_mes_letras(self, fecha_str):
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        # Obtener el día, mes y día de la semana en formato texto
        dia_semana = fecha.strftime("%A")  # Día de la semana completo
        dia = fecha.day  # Día del mes
        mes = fecha.strftime("%B").capitalize()  # Mes en letras

        # Diccionarios para reemplazar los nombres en inglés por español
        dias_semana = {
            "Monday": "Lunes",
            "Tuesday": "Martes",
            "Wednesday": "Miércoles",
            "Thursday": "Jueves",
            "Friday": "Viernes",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        meses = {
            "January": "Enero",
            "February": "Febrero",
            "March": "Marzo",
            "April": "Abril",
            "May": "Mayo",
            "June": "Junio",
            "July": "Julio",
            "August": "Agosto",
            "September": "Septiembre",
            "October": "Octubre",
            "November": "Noviembre",
            "December": "Diciembre"
        }

        # Reemplazar los nombres en inglés por español
        dia_semana = dias_semana.get(dia_semana, dia_semana)
        mes = meses.get(mes, mes)
        
        # Formatear la fecha completa
        fecha_formateada = f"{dia} de {mes} de {fecha.year}"
        #messagebox.showinfo("Información", f"Fecha: {fecha_formateada}\nDía de la semana: {dia_semana}")

        return dia, mes, fecha_formateada

    def get_resource_path(self, relative_path):
        # Resuelve la ruta de los recursos en modo empaquetado o en desarrollo
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def dividir_texto(self, texto, limite_primera_linea, limite_segunda_linea):
        primera_linea = texto[:limite_primera_linea]
        segunda_linea = texto[limite_primera_linea:
                              limite_primera_linea + limite_segunda_linea]
        return primera_linea, segunda_linea

    def generar_pdf_Anexo_VI(self):
        # Crear PDFs en memoria
        pdf_buffers = []
        registros = [self.tree.item(child)["values"]
                     for child in self.tree.get_children()]
        
        # Filtrar solo los estudiantes
        registros_estudiantes = [registro for registro in registros if registro[3] == "X"]
        
        for registro in registros_estudiantes:
            buffer = self.crear_pdf_por_alumno_en_memoria(registro)
            pdf_buffers.append(buffer)

        # Combinar todos los PDFs en uno solo
        self.combinar_pdfs_en_memoria(pdf_buffers)

    def crear_pdf_por_alumno_en_memoria(self, registro):
        # Crear un objeto BytesIO para el PDF en memoria
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)

        # Definir los fondos para cada página utilizando `get_resource_path`
        fondo_hoja_1 = self.get_resource_path("resources/Anexo VI_001.png")
        fondo_hoja_2 = self.get_resource_path("resources/Anexo VI_002.png")
        # fondo_hoja_3 = self.get_resource_path("resources/Anexo VI_003.png") --> no lo necesito

        # Obtener la fecha desglosada del TextBox del formulario
        dia, mes, fecha_formateada = self.obtener_mes_letras(self.fecha_entry.get())

        # Datos del alumno desde el registro del TreeView
        nombre = registro[1]
        dni = registro[2]

        # Datos generales desde los TextBox
        establecimiento = "E.P."
        numero_establecimiento = "43"
        distrito = "ESTEBAN ECHEVERRÍA"
        lugar = self.lugar_entry.get()  # Lugar tomado directamente del TextBox

        proyecto = self.proyecto_entry.get()
        fecha_salida = self.fechasalida_entry.get()
        hora_salida = self.horasalida_entry.get()
        fecha_regreso = self.fecharegreso_entry.get()
        hora_regreso = self.horaregreso_entry.get()
        lugar_estadia = self.lugarestadia_entry.get()
        datos_acompanantes = self.datosacompañantes_entry.get()
        empresa_contratada = self.empresacontratada_entry.get()
        datos_infraestructura = self.datosinfraestructura_entry.get()
        hospitales = self.hospitales_entry.get()
        otros_datos = self.otrosdatos_entry.get()

        # Divido los textos, que rebasan el primer renglón y tienen dos entry
        primera_linea_empresa_contratada, segunda_linea_proyecto_empresa_contratada = self.dividir_texto(
            empresa_contratada, 24, 78)
        primera_linea_datos_infraestructura, segunda_linea_datos_infraestructura = self.dividir_texto(
            datos_infraestructura, 46, 78)
        primera_linea_datos_hospitales, segunda_linea_datos_hospitales = self.dividir_texto(
            hospitales, 20, 78)
        primera_linea_otros_datos, segunda_linea_otros_datos = self.dividir_texto(
            otros_datos, 58, 78)

        # Primera página - datos completos del alumno y encabezado
        c.drawImage(fondo_hoja_1, 0, 0, width=A4[0], height=A4[1])
        c.setFont("Helvetica", 10)

        # Encabezado y datos generales
        c.drawString(167.24, 162, establecimiento)
        c.drawString(385.51, 162, numero_establecimiento)
        c.drawString(99.21, 145, distrito)
        c.drawString(99.21, 105, lugar)
        c.drawString(453.6, 105, f"{dia}")
        c.drawString(140, 86, f"{mes}")
        # Datos del alumno
        c.drawString(340, 202, nombre)
        c.drawString(283.46, 182, str(dni))

        # Datos generales de la excursión
        # colocar datos

        c.drawString(255.15, 591, proyecto)
        c.drawString(85, 540, establecimiento)
        c.drawString(120, 540, numero_establecimiento)
        c.drawString(144, 540, f",{fecha_formateada}, ")
        #c.drawString(180, 540, f"{dia},")
        c.drawString(290, 540, hora_salida + " hs.")
        c.drawString(227, 514, establecimiento)
        c.drawString(260, 514, numero_establecimiento)
        c.drawString(280, 514, f",{fecha_formateada}, ")
        #c.drawString(320, 514, f"{dia},")
        c.drawString(420, 514, hora_regreso + " hs.")
        c.drawString(294, 491, lugar_estadia)
        c.drawString(294, 466, datos_acompanantes)
        c.drawString(406, 440, primera_linea_empresa_contratada)
        c.drawString(82, 415, segunda_linea_proyecto_empresa_contratada)
        c.drawString(296, 391, primera_linea_datos_infraestructura)
        c.drawString(82, 363, segunda_linea_datos_infraestructura)
        c.drawString(420, 339, primera_linea_datos_hospitales)
        c.drawString(82, 315, segunda_linea_datos_hospitales)
        c.drawString(194, 290, primera_linea_otros_datos)
        c.drawString(81, 264, segunda_linea_otros_datos)

        # Guardar la primera página y pasar a la segunda
        c.showPage()

        # Segunda página - solo el fondo
        c.drawImage(fondo_hoja_2, 0, 0, width=A4[0], height=A4[1])
        c.showPage()

        # Tercera página - solo el fondo ---> no la necesito
        # c.drawImage(fondo_hoja_3, 0, 0, width=A4[0], height=A4[1])
        # c.showPage()

        # Finalizar el PDF en memoria
        c.save()
        buffer.seek(0)  # Volver al inicio del buffer
        return buffer

    def combinar_pdfs_en_memoria(self, pdf_buffers):
        # Crear un objeto PdfFileWriter
        writer = PdfFileWriter()

        # Agregar cada PDF del buffer al writer
        for buffer in pdf_buffers:
            reader = PdfFileReader(buffer)
            for page in reader.pages:
                writer.addPage(page)

        # Guardar el archivo PDF final
        # Reemplazar espacios por guiones bajos
        lugar = self.lugar_entry.get().replace(" ", "_")
        # Reemplazar caracteres de fecha si es necesario
        fecha = self.fecha_entry.get().replace("/", "-")

        pdf_path = os.path.join(os.path.expanduser(
            "~"), "Documents", "Anexos_PDFs")  # Ruta de la carpeta PDFs

        # Crear un nombre de archivo dinámico
        nombre_archivo = os.path.join(
            pdf_path, f"Anexos_VI_agrupados_{lugar}_{fecha}.pdf")

        with open(nombre_archivo, "wb") as f:
            writer.write(f)

        messagebox.showinfo(
            "Éxito", f"El PDF fue creado exitosamente como {os.path.basename(nombre_archivo)} en la carpeta Documentos\\Anexos_PDFs.")


root = tk.Tk()
root.geometry("930x600")
app = FormularioCarga(root)
root.mainloop()
