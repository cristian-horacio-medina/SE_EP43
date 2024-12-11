from tkinter import messagebox
from Servicio import *
from Mensaje import Mensaje
from pruebas.crearPDF import crea_pdf


class Gestor:

    @staticmethod
    def conexionBBDD():
        try:
            Servicio.conexionBBDD()
            messagebox.showinfo("CONEXION", Mensaje.EXITO_BD)
        except:
            messagebox.showinfo("CONEXION", Mensaje.ERROR_BD)

    # @staticmethod
    # def eliminarBBDD():
    #     if messagebox.askyesno(message=Mensaje.CONFIRMAR_BD, title="ADVERTENCIA"):
    #         Servicio.eliminarBBDD()
    #     else:
    #         messagebox.showinfo("CONEXION", Mensaje.ERROR_ELIMINAR_BD)

    @staticmethod
    def mostrar(tree, anio_actual, modulo, carrera):
        # Limpiar el Treeview antes de mostrar los datos
        for item in tree.get_children():
            tree.delete(item)

        # Obtener los datos de la base de datos
        datos = Servicio.consultar(anio_actual, modulo, carrera)

        # Insertar los datos en el Treeview de forma eficiente
        for row in datos:
            tree.insert("", "end", values=(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

    # @staticmethod
    # def buscar(anio_actual, modulo, carrera, criterio, tree):
        
    #     # Limpiar el Treeview
    #     for item in tree.get_children():
    #         tree.delete(item)

    #     try:
    #         if (criterio != "" and anio_actual != "" and modulo != "" and carrera != ""):
    #             docentes = Servicio.buscar(anio_actual, modulo, carrera, criterio)
    #             print(docentes)  # Para verificar la estructura de los datos

    #             if docentes:
    #                 # Asegúrate de que los datos tengan el número correcto de columnas
    #                 for row in docentes:
    #                     # Ajusta según el número de columnas
    #                     tree.insert("", "end", values=(
    #                         row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    #             else:
    #                 messagebox.showinfo(
    #                     "Información", "No se encontraron resultados.")
    #         else:
    #             messagebox.showwarning("ADVERTENCIA", Mensaje.NOMBRE_FALTANTE)

    #     except Exception as e:
    #         messagebox.showwarning("ADVERTENCIA", f"{Mensaje.ERROR_BUSCAR}\nError: {str(e)}")

    @staticmethod
    def buscar(anio_actual, modulo, carrera, criterio, tree):
        # Limpiar el Treeview
        for item in tree.get_children():
            tree.delete(item)

        try:
            if criterio != "" and anio_actual != "" and modulo != "" and carrera != "":
                docentes = Servicio.buscar(anio_actual, modulo, carrera, criterio)
                print(docentes)  # Para verificar la estructura de los datos

                if docentes:
                    # Procesar la información de los docentes y generar el PDF
                    for row in docentes:
                        # Aquí puedes ajustar según el número de columnas de la tabla
                        tree.insert("", "end", values=(
                            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))

                        # Crear la información para el PDF
                        info = {
                            "docente": row[1].strip(),
                            "carrera": row[2].strip(),
                            "materia": row[7].strip(),
                            "año": str(row[4]),
                            "division": row[5].strip(),
                            "turno": row[6].strip(),
                            "dia": row[8].strip(),
                            "horario": "19 a 22",
                            "tipo_dni": str(row[10]).strip(),
                            "DNI": str(row[11])  # Convertir a string
                        }

                        # Llamar a la función para crear el PDF
                        crea_pdf(info)
                else:
                    messagebox.showinfo(
                        "Información", "No se encontraron resultados.")
            else:
                messagebox.showwarning("ADVERTENCIA", Mensaje.NOMBRE_FALTANTE)

        except Exception as e:
            messagebox.showwarning("ADVERTENCIA", f"{Mensaje.ERROR_BUSCAR}\nError: {str(e)}")

    

    # @staticmethod
    # def buscar(anio_actual, modulo, carrera, criterio, tree):
    #     # Limpiar el Treeview
    #     for item in tree.get_children():
    #         tree.delete(item)

    #     try:
    #         if criterio != "" and anio_actual != "" and modulo != "" and carrera != "":
    #             docentes = Servicio.buscar(anio_actual, modulo, carrera, criterio)
    #             print(docentes)  # Para verificar la estructura de los datos

    #             if docentes:
    #                 # Crear un diccionario para almacenar la información por docente
    #                 info_por_docente = {}

    #                 # Procesar la información de los docentes
    #                 for row in docentes:
    #                     docente_id = row[0]  # ID del docente
    #                     docente_nombre = row[1].strip()
    #                     carrera_nombre = row[2].strip()
    #                     materia = row[7].strip()
    #                     año = str(row[4])
    #                     division = row[5].strip()
    #                     turno = row[6].strip()
    #                     dia = row[8].strip()
    #                     tipo_dni = str(row[10]).strip()
    #                     dni = str(row[11])  # Convertir a string

    #                     # Si el docente ya está en el diccionario, agregar la materia
    #                     if docente_id not in info_por_docente:
    #                         info_por_docente[docente_id] = {
    #                             "docente": docente_nombre,
    #                             "carrera": carrera_nombre,
    #                             "materias": [],
    #                             "año": año,
    #                             "division": division,
    #                             "turno": turno,
    #                             "dia": dia,
    #                             "tipo_dni": tipo_dni,
    #                             "DNI": dni
    #                         }

    #                     # Agregar la materia a la lista de materias
    #                     info_por_docente[docente_id]["materias"].append(materia)

    #                 # Generar el PDF para cada docente
    #                 for info in info_por_docente.values():
    #                     # Convertir la lista de materias en una cadena separada por comas
    #                     info["materias"] = ', '.join(info["materias"])
                        
    #                     # Llamar a la función para crear el PDF
    #                     crea_pdf(info)

    #                 messagebox.showinfo("Información", "Contratos generados con éxito.")
    #             else:
    #                 messagebox.showinfo("Información", "No se encontraron resultados.")
    #         else:
    #             messagebox.showwarning("ADVERTENCIA", Mensaje.NOMBRE_FALTANTE)

    #     except Exception as e:
    #         messagebox.showwarning("ADVERTENCIA", f"{Mensaje.ERROR_BUSCAR}\nError: {str(e)}")


    # # def crear(nombre, cargo, salario):
    # #     try:
    # #         if (nombre != "" and cargo != "" and salario != ""):
    # #             Servicio.crear(nombre, cargo, salario)
    # #         else:
    # #             messagebox.showwarning("ADVERTENCIA", Mensaje.CAMPOS_FALTANTES)
    # #     except:
    # #         messagebox.showwarning("ADVERTENCIA", Mensaje.ERROR_CREAR)

    @staticmethod
    def actualizar(comision_id, division):  # Asegúrate de que el argumento sea correcto
        try:
            Servicio.actualizar(comision_id, division)
        except Exception as e:
            print(f"Error al actualizar: {e}")
            messagebox.showwarning(
                "ADVERTENCIA", "Error al actualizar los datos.")

   

    # def borrar(ide):
    #     try:
    #         if messagebox.askyesno(message=Mensaje.CONFIRMAR, title="ADVERTENCIA"):
    #             Servicio.borrar(ide)
    #     except:
    #         messagebox.showwarning("ADVERTENCIA", Mensaje.ERROR_ELIMINAR)

    def mensaje():
        messagebox.showinfo(title="INFORMACION", message=Mensaje.ACERCA)

    
    def obtener_carreras(anio_actual, modulo):
        conexion, cursor = Servicio.conectar()
        # Consulta para obtener carrera_id y Descripcion
        resultados = Servicio.buscar_carrera(anio_actual, modulo)
        return resultados