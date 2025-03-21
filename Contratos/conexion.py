# Conexión a BD en SQL Server


import os
import pyodbc

class Conexion:

    server = os.getenv('DB_SERVER', 'FAE08/FAE08')
    bd = os.getenv('DB_NAME')
    usuario = os.getenv('DB_USER')
    contrasena = os.getenv('DB_PASSWORD', 'sql$05')


    try:
        conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                                'SERVER=' + server + ';'
                                'DATABASE=' + bd + ';'
                                'UID=' + usuario + ';'
                                'PWD=' + contrasena)
        print("Conexión exitosa")
    except pyodbc.Error as e:
        print("Error al intentar conectar a la BD:", e)

    
# # # Consulta a la BD

# cursor = conexion.cursor()
# cursor.execute("Select * FROM Al_carreras")

# # al_alumnos_materias = cursor.fetchone()

# # while al_alumnos_materias:
# #     print(al_alumnos_materias[4])
# #     al_alumnos_materias = cursor.fetchone()
    
# Al_carreras = cursor.fetchall()

# for carreras in Al_carreras:
#     print(carreras[4])
    
# cursor.close()
# conexion.close()    


# import os

# # Verifica si las variables de entorno están definidas
# print(f"DB_SERVER: {os.getenv('DB_SERVER')}")
# print(f"DB_NAME: {os.getenv('DB_NAME')}")
# print(f"DB_USER: {os.getenv('DB_USER')}")
# print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
