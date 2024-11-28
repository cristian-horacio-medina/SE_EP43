import pyodbc
import os
from tkinter import ttk, messagebox
from Consulta import *
from Docente import *


class Servicio:

    @staticmethod
    def conectar():
        # Parámetros de conexión a SQL Server, obtenidos de las variables de entorno
        server = os.getenv('DB_SERVER')  # Servidor por defecto
        bd = os.getenv('DB_NAME')  # Nombre de la base de datos
        usuario = os.getenv('DB_USER')  # Usuario de la base de datos
        # Contraseña con valor por defecto
        contrasena = os.getenv('DB_PASSWORD')

        try:
            # Establecer conexión a SQL Server
            conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                      'SERVER=' + server + ';'
                                      'DATABASE=' + bd + ';'
                                      'UID=' + usuario + ';'
                                      'PWD=' + contrasena)
            cursor = conexion.cursor()
            return conexion, cursor  # Devolver tanto la conexión como el cursor
        except pyodbc.Error as e:
            print("Error al conectar a la base de datos:", e)
            return None

    @staticmethod
    def conexionBBDD():
        conexion, cursor = Servicio.conectar()

    @staticmethod
    def consultar(modulo, carrera, anio_actual):
        conexion, cursor = Servicio.conectar()
        cursor.execute(Consulta.SELECT, (modulo, carrera, anio_actual))
        resultado = cursor.fetchall()
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
        return resultado

    # if __name__ == "__main__":
    # # Llamada al método conectar para ver si funciona la conexión
    # conexion = Servicio.conectar()
    # if conexion:
    #     print("Conexión establecida correctamente.")
    # else:
    #     print("No se pudo establecer la conexión.")

    @staticmethod
    def actualizar(comision_id, division):
        conexion, cursor = Servicio.conectar()
        try:
            cursor.execute(Consulta.UPDATE, (division, comision_id))
            conexion.commit()  # Realiza el commit de los cambios
        except Exception as e:
            print("Error al actualizar:", e)
        finally:
            cursor.close()  # Cerrar el cursor
            conexion.close()  # Cerrar la conexión
    
    @staticmethod
    def buscar(anio_actual, modulo, carrera, criterio):
        conexion, cursor = Servicio.conectar()
        cursor.execute(Consulta.BUSCAR, (anio_actual, modulo, carrera, f"%{criterio}%"))
        return cursor.fetchall()
        
    @staticmethod
    def buscar_carrera(anio_actual, modulo):
        conexion, cursor = Servicio.conectar()
        cursor.execute(Consulta.BUSCAR_CARRERA, (anio_actual, modulo))
        resultado = cursor.fetchall()
        cursor.close()  # Cerrar el cursor
        conexion.close()  # Cerrar la conexión
        return resultado