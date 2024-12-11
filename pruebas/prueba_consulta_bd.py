import sqlite3

def conectar_y_consultar():
    try:
        conexion = sqlite3.connect(r"C:\Users\Papá\Python\Excursion.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT Apellido || ', ' || Nombre AS NombreCompleto, DNI, Alumno FROM alumnos")  # Cambia 'nombre_de_la_tabla' por el nombre real.
        datos = cursor.fetchall()
        if datos:
            for fila in datos:
                print(fila)
        else:
            print("La tabla no tiene datos.")
        conexion.close()
    except sqlite3.Error as e:
        print(f"Error: {e}")

conectar_y_consultar()
