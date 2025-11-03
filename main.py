import tkinter as tk
import os
import locale
import sys
import sqlite3
from datetime import datetime
from tkinter import messagebox, ttk
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF4 import PdfFileWriter, PdfFileReader
from db_utils import get_db_path
from db_utils import get_resource_path


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
        control_tabulador.grid(row=0, column=0, columnspan=4)

    def crear_componentes_tabulador1(self, tabulador):
        
        tk.Label(tabulador, text="Grado:").grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.combobox_grado = ttk.Combobox(
            tabulador, state="readonly", width=6)
        self.combobox_grado.grid(row=0, column=1, sticky="w", padx=3, pady=3)
        
        
        # Agregar una etiqueta y un campo de entrada para 'Fecha'
        tk.Label(tabulador, text="Fecha de salida:").grid(
            row=0, column=1, sticky='e', padx=100, pady=5)
        self.fecha_var = tk.StringVar()
        self.fecha_entry = tk.Entry(tabulador, width=10, textvariable=self.fecha_var)
        self.fecha_entry.grid(row=0, column=1, sticky='e', padx=5, pady=5)
        # Añadido: Evento para formatear la fecha
        self.fecha_entry.bind("<KeyRelease>", self.formatear_fecha)
        
       
        # Agregar una etiqueta y un campo de entrada para 'Lugar'
        tk.Label(tabulador, text="Lugar:").grid(
            row=1, column=0, sticky='w', padx=5, pady=3)
        self.lugar_entry = tk.Entry(tabulador, width=33)
        self.lugar_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        self.lugar_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.lugar_entry, 33, tabulador))

        # Agregar una etiqueta y un campo de entrada para 'Localidad'
        tk.Label(tabulador, text="Localidad:").grid(
            row=1, column=2, sticky='w', padx=(5,0), pady=5)
        self.localidad_entry = tk.Entry(tabulador, width=23)
        self.localidad_entry.grid(row=1, column=2, sticky='e', padx=(0, 5), pady=5)
        self.localidad_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.localidad_entry, 33, tabulador))

        # Apellido
        tk.Label(tabulador, text="Apellido:").grid(row=2, column=0, sticky='w', padx=5, pady=2)
        self.apellido_entry = tk.Entry(tabulador, width=40)
        self.apellido_entry.grid(row=2, column=1, sticky='w', padx=5, pady=2)
        self.apellido_entry.bind("<KeyRelease>", self.convertir_mayusculas)

        # Nombre
        tk.Label(tabulador, text="Nombre:").grid(row=2, column=1, sticky='e', padx=5, pady=2)
        self.nombre_entry = tk.Entry(tabulador, width=40)
        self.nombre_entry.grid(row=2, column=2,sticky='e', padx=5, pady=2)
        self.nombre_entry.bind("<KeyRelease>", self.convertir_mayusculas)

        # Agregar una etiqueta y un campo de entrada para 'Documento'
        tk.Label(tabulador, text="Documento:").grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        self.documento_entry = tk.Entry(tabulador, width=9)
        self.documento_entry.grid(row=3, column=1, sticky='w', padx=5, pady=5)
        self.documento_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(self.documento_entry, 9, tabulador))
        #Variable para el rol seleccionado
        self.rol_seleccionado = tk.StringVar(value="Estudiante")

        # Radiobuttons para seleccionar rol
        self.rol_seleccionado.set("Estudiante")  # Selecciona "Estudiante" por defecto
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

        

        # Botón para nueva excursión
        self.agregar_excursion_btn = tk.Button(
            tabulador, text="Nueva excursión", command=self.nueva_excursion)
        self.agregar_excursion_btn.grid(row=0, column=3, sticky='ew')
        self.agregar_excursion_btn.config(bg="green", fg="white", font=("Arial", 10, "bold"))
        
        #Botón eliminar excursión
        self.eliminar_excursion_btn = tk.Button(
            tabulador, text="Eliminar excursión", command=self.eliminar_excursion)
        self.eliminar_excursion_btn.grid(row=3, column=3, sticky='ew')
        self.eliminar_excursion_btn.config(bg="red", fg="white", font=("Arial", 10, "bold"))
        #Botón duplicar excursión
        self.duplicar_excursion_btn = tk.Button(
            tabulador, text="Duplicar excursión", command=lambda: self.duplicar_excursion(self.IdEXCURSION))
        self.duplicar_excursion_btn.grid(row=1, column=3, sticky='ew')
        self.duplicar_excursion_btn.config(bg="sky blue", fg="white", font=("Arial", 10, "bold"))
        
        # Botón para agregar registro
        self.agregar_btn = tk.Button(
            tabulador, text="Agregar", command=self.agregar, bg="green", fg="white", font=("Arial", 10, "bold"))
        self.agregar_btn.grid(row=6, column=0, sticky='ew')

        

        # Botón para mostrar o actualizar
        self.mostrar_button = tk.Button(
            tabulador, text="Modificar seleccionado", command=self.mostrar_o_actualizar, bg="blue", fg="white", font=("Arial", 10, "bold"))
        self.mostrar_button.grid(row=6, column=2, sticky='ew')
        self.mostrar_button.config(state="normal")  # Deshabilitar el botón
        
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
            tabulador, text="PLANILLA PARA MAESTRAS", command=self.imprimir_pdf)
        self.guardar_btn.grid(row=9, column=0, sticky='ew')

        self.guardar_btn = tk.Button(
            tabulador, text="Guardar excursión", command=self.guardar_sqlite)
        self.guardar_btn.grid(row=9, column=1, sticky='ew')

        
        self.generar_pdf_btn = tk.Button(
            tabulador, text="Generar Anexo V", command=self.generar_pdf_Anexo_V)
        self.generar_pdf_btn.grid(row=9, column=2, sticky='ew')
       

        # Botón para generar los PDFs individuales
        self.generar_pdfs_btn = tk.Button(
            tabulador, text="Generar Anexo VI", command=self.generar_pdf_Anexo_VI)
        self.generar_pdfs_btn.grid(row=9, column=3, sticky='ew')

        self.salir_btn = tk.Button(tabulador, text="Salir", command=self.confirmar_salida)
        self.salir_btn.grid(row=11, column=0, columnspan=4, sticky='ew')

    

        # Botón para abrir la carpeta donde se guardó el PDF
        abrir_carpeta_btn = tk.Button(
            tabulador, text="Abrir carpeta con Anexos", command=lambda: os.startfile(os.path.join(os.path.expanduser("~"), "Documents", "Anexos_PDFs")))
        abrir_carpeta_btn.grid(row=10, column=2, columnspan=2, sticky='ew')


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

    def convertir_mayusculas(self, event):
        widget = event.widget
        texto = widget.get()
        widget.delete(0, tk.END)
        widget.insert(0, texto.upper())
    

    def get_resource_path(relative_path):
        """Devuelve la ruta a recursos, en desarrollo o empaquetado."""
        try:
            base_path = sys._MEIPASS  # carpeta temporal de PyInstaller
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def imprimir_pdf(self):
        try:
            archivo = get_resource_path(os.path.join("resources", "planilla.pdf"))
            if not os.path.exists(archivo):
                messagebox.showerror("Error", f"No se encontró el archivo:\n{archivo}")
                return
            os.startfile(archivo)  # Abre con el visor predeterminado (Edge/Adobe/etc.)
        except Exception as e:
            messagebox.showerror("Error al abrir PDF", str(e))
        
    
    def confirmar_salida(self):
        if messagebox.askyesno("Confirmación", "¿Desea guardar los cambios antes de salir?"):
            self.guardar_sqlite()
        if messagebox.askyesno("Confirmación", "¿Está seguro de que desea salir?"):
            quit()    

    def limitar_texto(self, texto):
        return len(texto) <= 33

    def cargar_grados(self):
        try:
            db_path = os.path.join(os.path.expanduser(
                "~"), "Documents", "Excursion.db")
            conexion = sqlite3.connect(db_path)
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT idgrado, grado||seccion||turno AS grado_completo FROM grado;")
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

            # Obtener las excursiones con su ID, lugar, fecha y grado, ordenadas por fecha en formato de fecha real
            cursor.execute("""
                SELECT IdEXCURSION, lugar, fecha, 
                    (SELECT grado || seccion || turno FROM grado WHERE grado.IdGRADO = excursion.IdGRADO) AS grado
                FROM excursion
                ORDER BY date(substr(fecha, 7, 4) || '-' || substr(fecha, 4, 2) || '-' || substr(fecha, 1, 2))
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
        # Nombre del Proyecto
        tk.Label(tabulador, text="Nombre del Proyecto:").grid(
            row=0, column=0, sticky='w', padx=5, pady=5)
        self.proyecto_entry = tk.Entry(tabulador, width=80)
        self.proyecto_entry.grid(
            row=0, column=1, columnspan=5, sticky='w', padx=5, pady=5)
        self.proyecto_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.proyecto_entry, 60, tabulador))

        # Lugar de salida
        tk.Label(tabulador, text="Lugar de salida:").grid(
            row=1, column=0, sticky='w', padx=5, pady=2)
        self.lugardesalida_entry = tk.Entry(tabulador, width=25)
        self.lugardesalida_entry.grid(
            row=1, column=1, sticky='w', padx=5, pady=5)
        self.lugardesalida_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.lugardesalida_entry, 28, tabulador))

        # Fecha de salida
        tk.Label(tabulador, text="Fecha de salida:").grid(
            row=1, column=2, sticky='e', padx=2, pady=5)
        tk.Label(tabulador, textvariable=self.fecha_var).grid( 
            row=1, column=3, sticky='w', padx=2, pady=5)
        
        # Hora de salida
        tk.Label(tabulador, text="Hora de salida:").grid(
            row=1, column=4, sticky='e', padx=2, pady=5)
        self.horasalida_entry = tk.Entry(tabulador, width=8)
        self.horasalida_entry.grid(
            row=1, column=5, sticky='w', padx=2, pady=5) 
        self.horasalida_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.horasalida_entry, 5, tabulador))

        # Lugar de regreso
        tk.Label(tabulador, text="Lugar de regreso:").grid(
            row=2, column=0, sticky='w', padx=5, pady=2)
        self.lugarderegreso_entry = tk.Entry(tabulador, width=25)
        self.lugarderegreso_entry.grid(
            row=2, column=1, sticky='w', padx=5, pady=5)
        self.lugarderegreso_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.lugarderegreso_entry, 28, tabulador))

        # Fecha de regreso
        tk.Label(tabulador, text="Fecha de regreso:").grid(
            row=2, column=2, sticky='e', padx=2, pady=5)
        self.fecharegreso_entry = tk.Entry(tabulador, width=8)
        self.fecharegreso_entry.grid(
            row=2, column=3, sticky='w', padx=2, pady=2)
        # Añadido: Evento para formatear la fecha
        #self.fecha_entry.bind("<KeyRelease>", self.formatear_fecha)
        
        # Hora de regreso
        tk.Label(tabulador, text="Hora de regreso:").grid(
            row=2, column=4, sticky='e', padx=2, pady=2)
        self.horaregreso_entry = tk.Entry(tabulador, width=8)
        self.horaregreso_entry.grid(
            row=2, column=5, sticky='w', padx=2, pady=2)
        self.horaregreso_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.horaregreso_entry, 5, tabulador))

        # Lugar de estadía
        tk.Label(tabulador, text="Lugar de estadía\n(domicilios y tel.):").grid(
            row=3, column=0, sticky='w', padx=5, pady=5)
        self.lugarestadia_entry = tk.Entry(tabulador, width=60)
        self.lugarestadia_entry.grid(
            row=3, column=1, columnspan=5, sticky='w', padx=5, pady=5)
        self.lugarestadia_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.lugarestadia_entry, 50, tabulador))

        # Nombres y tel. de acompañantes
        tk.Label(tabulador, text="Nombres y tel.\nde acompañantes:").grid(
            row=4, column=0, sticky='w', padx=5, pady=5)
        self.datosacompañantes_entry = tk.Entry(tabulador, width=60)
        self.datosacompañantes_entry.grid(
            row=4, column=1, columnspan=5, sticky='w', padx=5, pady=5)
        self.datosacompañantes_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.datosacompañantes_entry, 50, tabulador))

        # Empresa y/o empresas contratadas
        tk.Label(tabulador, text="Empresa/s contratada/s\n(nombre, dirección, tel.:").grid(
            row=5, column=0, sticky='w', padx=5, pady=5)
        self.empresacontratada_entry = tk.Entry(tabulador, width=80)
        self.empresacontratada_entry.grid(
            row=5, column=1, columnspan=5, sticky='w', padx=5, pady=5)
        self.empresacontratada_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.empresacontratada_entry, 123, tabulador))

        # Otros datos de la infraestructura disponible
        tk.Label(tabulador, text="Otros datos de la\ninfraestructura disponible:").grid(
            row=6, column=0, sticky='w', padx=5, pady=5)
        self.datosinfraestructura_entry = tk.Entry(tabulador, width=80)
        self.datosinfraestructura_entry.grid(
            row=6, column=1, columnspan=5, sticky='w', padx=5, pady=5)
        self.datosinfraestructura_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.datosinfraestructura_entry, 147, tabulador))

        # Hospitales y centros asistenciales cercanos
        tk.Label(tabulador, text="Hospitales y centros asist.\ncercanos(direcciones y tel.:").grid(
            row=7, column=0, sticky='w', padx=5, pady=5)
        self.hospitales_entry = tk.Entry(tabulador, width=80)
        self.hospitales_entry.grid(
            row=7, column=1, columnspan=5, sticky='w', padx=5, pady=5)
        self.hospitales_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.hospitales_entry, 119, tabulador))

        # Otros datos de interés
        tk.Label(tabulador, text="Otros datos de interés:").grid(
            row=8, column=0, sticky='w', padx=5, pady=5)
        self.otrosdatos_entry = tk.Entry(tabulador, width=80)
        self.otrosdatos_entry.grid(
            row=8, column=1, columnspan=5, sticky='w', padx=5, pady=5)
        self.otrosdatos_entry.bind("<KeyRelease>", lambda e: self.limitar_caracteres(
            self.otrosdatos_entry, 170, tabulador))
         

    def mostrar_advertencia(self, texto):

        messagebox.showwarning("Advertencia", texto)
        
    def duplicar_excursion(self, id_excursion_original):
        db_path = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # 1. Obtener datos de la excursión original
            cursor.execute("SELECT lugar, localidad, fecha, nombre_proyecto, hora_salida, \
                             fecha_regreso, hora_regreso, lugar_estadia, datos_acompanantes, empresa_contratada, \
                            datos_infraestructura, hospitales, otros_datos, IdGRADO \
                            FROM excursion WHERE IdEXCURSION = ?", (id_excursion_original,))
            datos_excursion = cursor.fetchone()

            if not datos_excursion:
                messagebox.showerror("Error", "La excursión original no existe")
                return

            # 2. Insertar nueva excursión (idéntica a la original, salvo que podés cambiar fecha/lugar si querés)
            cursor.execute('''INSERT INTO excursion (lugar, localidad, fecha, nombre_proyecto, hora_salida,
                                fecha_regreso, hora_regreso, lugar_estadia, datos_acompanantes, empresa_contratada,
                                datos_infraestructura, hospitales, otros_datos, IdGRADO)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', datos_excursion)

            nuevo_id_excursion = cursor.lastrowid

            # 3. Copiar alumnos de la excursión original
            cursor.execute("SELECT apellido, nombre, DNI, ALUMNO, IdGRADO FROM alumnos WHERE IdEXCURSION = ?", 
                           (id_excursion_original,))
            alumnos = cursor.fetchall()

            for alumno in alumnos:
                cursor.execute('''INSERT INTO alumnos (IdEXCURSION, apellido, nombre, DNI, ALUMNO, IdGRADO)
                                  VALUES (?, ?, ?, ?, ?, ?)''',
                               (nuevo_id_excursion, alumno[0], alumno[1], alumno[2], alumno[3], alumno[4]))

            # 4. Copiar acompañantes de la excursión original
            cursor.execute("SELECT apellido, nombre, DNI, DOCENTE, NO_DOCENTE, IdGRADO FROM acompanantes WHERE IdEXCURSION = ?", 
                           (id_excursion_original,))
            acompanantes = cursor.fetchall()

            for acomp in acompanantes:
                cursor.execute('''INSERT INTO acompanantes (IdEXCURSION, apellido, nombre, DNI, DOCENTE, NO_DOCENTE, IdGRADO)
                                  VALUES (?, ?, ?, ?, ?, ?, ?)''',
                               (nuevo_id_excursion, acomp[0], acomp[1], acomp[2], acomp[3], acomp[4], acomp[5]))

            conn.commit()
            messagebox.showinfo("Éxito", f"Excursión duplicada con Id {nuevo_id_excursion}")
            self.actualizar_lista_excursiones()

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo duplicar la excursión: {e}")
        finally:
            conn.close()
    
    

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

    def formatear_fechaalt(self, event):  # Nuevo método para formatear la fecha
        fechaalt = self.fechaalt_entry.get().replace("/", "")
        if len(fechaalt) >= 2:
            fechaalt = fechaalt[:2] + "/" + fechaalt[2:]
        if len(fechaalt) >= 5:
            fechaalt = fechaalt[:5] + "/" + fechaalt[5:]
        self.fechaalt_entry.delete(0, tk.END)
        self.fechaalt_entry.insert(0, fechaalt)

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
        self.rol_seleccionado.set("Estudiante")  # Selecciona "Estudiante" por defecto
    def limpiar(self):
        # Limpiar los campos de entrada
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
            db_path = get_db_path()
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
                self.combobox_grado.config(state="readonly")
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
            db_path = get_db_path()
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
        self.combobox_grado.config(state="readonly")
        # Desvincular el evento para evitar múltiples actualizaciones
        self.combobox_grado.unbind("<<ComboboxSelected>>")

        # Actualizar la lista de excursiones en el combobox
        self.actualizar_lista_excursiones()
    def guardar_sqlite(self):
        # Obtén los registros desde el Treeview
        registros = [self.tree.item(child)["values"]
                     for child in self.tree.get_children()]
        
        # Obtener valores de los campos de entrada (TextBox)
        lugar = self.lugar_entry.get()
        localidad = self.localidad_entry.get()
        fecha = self.fecha_entry.get()
        nombre_proyecto = self.proyecto_entry.get()
        lugar_salida = self.lugardesalida_entry.get()
        #fecha_salida = self.fechasalida_entry.get()
        hora_salida = self.horasalida_entry.get()
        lugar_regreso = self.lugarderegreso_entry.get()
        fecha_regreso = self.fecharegreso_entry.get()
        hora_regreso = self.horaregreso_entry.get()
        lugar_estadia = self.lugarestadia_entry.get()
        datos_acompanantes = self.datosacompañantes_entry.get()
        empresa_contratada = self.empresacontratada_entry.get()
        datos_infraestructura = self.datosinfraestructura_entry.get()
        hospitales = self.hospitales_entry.get()
        otros_datos = self.otrosdatos_entry.get()

        # Obtener el IdGRADO del combobox_grado
        grado_seleccionado = self.combobox_grado.get()
        #messagebox.showinfo("Información", f"El grado seleccionado es: {grado_seleccionado}")
        if grado_seleccionado in self.grados:
            self.IdGRADO = self.grados[grado_seleccionado]
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un grado válido.")
            return
        #messagebox.showinfo("Información", f"El ID del grado seleccionado es: {self.IdGRADO}")
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
                                localidad TEXT,
                                fecha TEXT,
                                nombre_proyecto TEXT,
                                hora_salida TEXT,
                                fecha_regreso TEXT,
                                hora_regreso TEXT,
                                lugar_estadia TEXT,
                                datos_acompanantes TEXT,
                                empresa_contratada TEXT,
                                datos_infraestructura TEXT,
                                hospitales TEXT,
                                otros_datos TEXT,
                                IdGRADO INTEGER,
                                FOREIGN KEY(IdGRADO) REFERENCES grado(IdGRADO))''')

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
                cursor.execute('''UPDATE excursion SET lugar = ?, localidad = ?, fecha = ?, nombre_proyecto = ?, lugar_salida = ?, hora_salida = ?,
                                  fecha_regreso = ?, lugar_regreso = ?,  hora_regreso = ?, lugar_estadia = ?, datos_acompanantes = ?, empresa_contratada = ?,
                                    datos_infraestructura = ?, hospitales = ?, otros_datos = ?, IdGRADO = ?
                                    WHERE IdEXCURSION = ?''',
                               (lugar, localidad, fecha, nombre_proyecto, lugar_salida, hora_salida, fecha_regreso, lugar_regreso,
                                hora_regreso, lugar_estadia, datos_acompanantes, empresa_contratada,
                                datos_infraestructura, hospitales, otros_datos, self.IdGRADO, self.IdEXCURSION))
            else:
                # Insertar los datos en la tabla excursion
                cursor.execute('''INSERT INTO excursion (lugar, localidad, fecha, nombre_proyecto, lugar_salida, hora_salida,
                                    fecha_regreso, lugar_regreso,hora_regreso, lugar_estadia, datos_acompanantes, empresa_contratada,
                                    datos_infraestructura, hospitales, otros_datos, IdGRADO)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (lugar, localidad, fecha, nombre_proyecto, lugar_salida, hora_salida, fecha_regreso, lugar_regreso, 
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

            conn.commit()
            messagebox.showinfo(
                "Éxito", "Datos guardados correctamente en la base de datos.")
            self.combobox_grado.config(state="disabled")  # Mantenerlo en readonly para evitar modificaciones
            
            self.actualizar_lista_excursiones()
        except Exception as e:
            conn.rollback()
            messagebox.showerror(
                "Error", f"No se pudo guardar en la base de datos: {e}")
        finally:
            conn.close()
    def nueva_excursion(self):
        # Limpiar todos los campos del formulario
        self.reiniciar_formulario()

        # Restablecer las variables de instancia
        self.IdEXCURSION = None  # Resetear el ID de la excursión
        self.IdGRADO = None  # Resetear el ID del grado

        # Habilitar el combobox de grados para permitir la selección
        self.combobox_grado.config(state="normal")  # Habilitar el combobox para el grado
        self.combobox_grado.set("")  # Opcional: Limpiar el valor seleccionado del combobox

        # Colocar el foco en el primer campo (por ejemplo, el lugar de la excursión)
        self.lugar_entry.focus()


        messagebox.showinfo("Éxito", "Excursión guardada correctamente.")
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
            db_path = get_db_path()
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


    # def guardar_y_reiniciar(self):
    #     self.guardar_sqlite()
    #     self.reiniciar_formulario()
    #     self.combobox_grado.focus()  # Ubica el cursor en el campo Lugar

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

        # Ruta fija de la base de datos
        db_path = os.path.join(os.path.expanduser(
            "~"), "Documents", "Excursion.db")

        try:
            # Conexión a la base de datos
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Obtener los datos de la excursión seleccionada
            cursor.execute("""
                SELECT lugar, localidad, fecha, nombre_proyecto, lugar_salida, hora_salida,
                    fecha_regreso, lugar_regreso, hora_regreso, lugar_estadia, datos_acompanantes,
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
                self.lugar_entry,  self.localidad_entry,  self.fecha_entry,  self.proyecto_entry, self.lugardesalida_entry,
                self.horasalida_entry, self.fecharegreso_entry, self.lugarderegreso_entry,
                self.horaregreso_entry,
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
            #messagebox.showinfo(self.IdGRADO, f"El ID del grado seleccionado es: {self.IdGRADO}")
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
    def reiniciar_formulario(self):
        self.combobox_grado.focus()
        self.combobox_grado.state(["!disabled"])
        self.combobox_grado.set("")  # Limpiar el combobox de grados
        self.localidad_entry.delete(0, tk.END)
        self.lugar_entry.delete(0, tk.END)
        self.fecha_entry.delete(0, tk.END)
        self.combobox_excursion.set("")  # Limpiar el combobox de excursiones   
        self.proyecto_entry.delete(0, tk.END)
        self.lugardesalida_entry.delete(0, tk.END)
        #self.fechasalida_entry.delete(0, tk.END)
        self.horasalida_entry.delete(0, tk.END)
        self.lugarderegreso_entry.delete(0, tk.END)
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
            alumnos.apellido || ', ' || alumnos.nombre AS Apellido_Nombre,
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
            acompanantes.apellido || ', ' || acompanantes.nombre AS Apellido_Nombre,
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

        # Ordenar en tres grupos: Estudiantes, Docentes (excluyendo Reemplazantes), No Docentes, y Reemplazantes al final
        estudiantes = sorted(
            [r for r in registros if r['Alumno'] == "X"], key=lambda x: x['Apellido_Nombre'])
        docentes = sorted(
            [r for r in registros if r['Docente'] not in ["", "Reemplazante"]], key=lambda x: x['Apellido_Nombre'])
        no_docentes = sorted(
            [r for r in registros if r['NoDocente'] != ""], key=lambda x: x['Apellido_Nombre'])
        reemplazantes = sorted(
            [r for r in registros if r['Docente'] == "Reemplazante"], key=lambda x: x['Apellido_Nombre'])

        # Concatenar los grupos en el orden solicitado
        registros_ordenados = estudiantes + docentes + no_docentes

        # Enumerar secuencialmente solo los grupos enumerados
        for i, registro in enumerate(registros_ordenados, start=1):
            registro['Numero'] = i

        # Agregar los reemplazantes al final sin numerar
        for registro in reemplazantes:
            registro['Numero'] = ""

        # Combinar todos los registros
        registros_ordenados += reemplazantes

        # Generar múltiples PDFs en memoria y combinar
        self.generar_pdfs_en_memoria(registros_ordenados)

        # Cierra la conexión
        cursor.close()
        conexion.close()

    def crear_pdf_memoria(self, registros, imagen_fondo, mostrar_encabezado, posicion_inicial, max_por_pagina):
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.drawImage(imagen_fondo, 0, 0,
                    width=A4[0], height=A4[1], preserveAspectRatio=True, anchor='c')

        y = posicion_inicial

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

        c.setFont("Helvetica", 7)

        for i, registro in enumerate(registros):
            c.drawString(90, y, str(registro['Numero']))
            c.drawString(115, y, str(registro['Apellido_Nombre']))
            c.drawString(285, y, str(registro['DNI']))
            c.drawString(350, y, "X" if registro['Alumno'] == "X" else "")
            c.drawString(390, y, str(registro['Docente']))
            c.drawString(460, y, str(registro['NoDocente']))
            y -= 23

            if (i + 1) % max_por_pagina == 0 and (i + 1) < len(registros):
                c.showPage()
                c.drawImage(imagen_fondo, 0, 0,
                            width=A4[0], height=A4[1], preserveAspectRatio=True, anchor='c')
                y = posicion_inicial

        c.save()
        buffer.seek(0)
        return buffer


    def generar_pdfs_en_memoria(self, registros_ordenados):
        fondo_impar = self.get_resource_path("resources/Anexo_V_1.png")
        fondo_par = self.get_resource_path("resources/Anexo_V_2.png")

        posicion_impar = 632
        posicion_par = 686

        buffers = []

        if not registros_ordenados:
            # Caso 0 registros: hoja impar vacía + hoja par vacía
            buffer = self.crear_pdf_memoria(
                [],
                fondo_impar,
                mostrar_encabezado=True,
                posicion_inicial=posicion_impar,
                max_por_pagina=18
            )
            buffers.append(buffer)

            buffer = self.crear_pdf_memoria(
                [],
                fondo_par,
                mostrar_encabezado=False,
                posicion_inicial=posicion_par,
                max_por_pagina=9
            )
            buffers.append(buffer)

        elif len(registros_ordenados) <= 18:
            # Todos los registros en una hoja impar
            buffer = self.crear_pdf_memoria(
                registros_ordenados,
                fondo_impar,
                mostrar_encabezado=True,
                posicion_inicial=posicion_impar,
                max_por_pagina=18
            )
            buffers.append(buffer)

            # Hoja par vacía
            buffer = self.crear_pdf_memoria(
                [],
                fondo_par,
                mostrar_encabezado=False,
                posicion_inicial=posicion_par,
                max_por_pagina=9
            )
            buffers.append(buffer)

        else:
            # Generar hojas impares de 18 registros
            while len(registros_ordenados) > 9:
                registros_a_incluir = registros_ordenados[:18]
                buffer = self.crear_pdf_memoria(
                    registros_a_incluir,
                    fondo_impar,
                    mostrar_encabezado=True,
                    posicion_inicial=posicion_impar,
                    max_por_pagina=18
                )
                buffers.append(buffer)
                registros_ordenados = registros_ordenados[18:]

            # Los últimos registros (1 a 9) van en hoja par
            buffer = self.crear_pdf_memoria(
                registros_ordenados,
                fondo_par,
                mostrar_encabezado=False,
                posicion_inicial=posicion_par,
                max_por_pagina=9
            )
            buffers.append(buffer)

        # Combinar y guardar
        archivo_salida = os.path.join(
            os.environ["USERPROFILE"], "Documents", "Anexos_PDFs", "Anexo_V.pdf"
        )
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
        numero_establecimiento = "Nº 43"
        distrito = "ESTEBAN ECHEVERRÍA"
        lugar = self.lugar_entry.get()  # Lugar tomado directamente del TextBox
        localidad = self.localidad_entry.get()
        proyecto = self.proyecto_entry.get()
        lugar_salida = self.lugardesalida_entry.get()
        #fecha_salida = self.fecha_entry.get()
        hora_salida = self.horasalida_entry.get()
        lugar_regreso = self.lugarderegreso_entry.get()
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
            empresa_contratada, 23, 100)
        primera_linea_datos_infraestructura, segunda_linea_datos_infraestructura = self.dividir_texto(
            datos_infraestructura, 47, 100)
        primera_linea_datos_hospitales, segunda_linea_datos_hospitales = self.dividir_texto(
            hospitales, 19, 100)
        primera_linea_otros_datos, segunda_linea_otros_datos = self.dividir_texto(
            otros_datos, 70, 100)

        # Primera página - datos completos del alumno y encabezado
        c.drawImage(fondo_hoja_1, 0, 0, width=A4[0], height=A4[1])
        c.setFont("Helvetica", 10)

        # Encabezado y datos generales
        c.drawString(167.24, 162, establecimiento)
        c.drawString(385.51, 162, numero_establecimiento)
        c.drawString(99.21, 145, distrito)
        c.drawString(99.21, 105, localidad)
        c.drawString(453.6, 105, f"{dia}")
        c.drawString(140, 86, f"{mes}")
        # Datos del alumno
        c.drawString(340, 202, nombre)
        c.drawString(283.46, 182, str(dni))

        # Datos generales de la excursión
        # colocar datos

        c.drawString(255.15, 591, proyecto)
        c.drawString(85, 540, lugar_salida)
        #c.drawString(110,540, numero_establecimiento)
        c.drawString(240, 540, f",{fecha_formateada}, ")
        #c.drawString(180, 540, f"{dia},")
        c.drawString(356, 540, hora_salida + " hs.")
        c.drawString(227, 514, lugar_regreso)
        #c.drawString(250, 514, numero_establecimiento)
        c.drawString(378, 514, f",{fecha_formateada}, ")
        #c.drawString(320, 514, f"{dia},")
        c.drawString(494, 514, hora_regreso + " hs.")
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
        grado= self.combobox_grado.get()

        pdf_path = os.path.join(os.path.expanduser(
            "~"), "Documents", "Anexos_PDFs")  # Ruta de la carpeta PDFs

        # Crear un nombre de archivo dinámico
        nombre_archivo = os.path.join(
            pdf_path, f"Anexos_VI_agrupados_{grado}_{lugar}_{fecha}.pdf")

        with open(nombre_archivo, "wb") as f:
            writer.write(f)

        messagebox.showinfo(
            "Éxito", f"El PDF fue creado exitosamente como {os.path.basename(nombre_archivo)} en la carpeta Documentos\\Anexos_PDFs.")
        
        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("960x600")
    app = FormularioCarga(root)
    root.mainloop()
