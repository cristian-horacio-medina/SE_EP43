import sqlite3
import os

db_path = os.path.join(os.path.expanduser("~"), "Documents", "Excursion.db")

# Conexión a la base de datos
conexion = sqlite3.connect(db_path)
conexion.row_factory = sqlite3.Row
cursor = conexion.cursor()

# La consulta SQL que proporcionaste
consulta = """
SELECT
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
    excursion.fecha = '24/10/2024'

UNION ALL

SELECT
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
    excursion.fecha = '24/10/2024'
"""

# Ejecuta la consulta
cursor.execute(consulta)

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

# Cierra la conexión
cursor.close()
conexion.close()

# Muestra el array con los registros
print(registros)
