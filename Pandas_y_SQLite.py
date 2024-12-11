import sqlite3
import pandas as pd
import os

# Ruta fija de la base de datos
db_path = os.path.join(os.path.expanduser(
            "~"), "Documents", "Excursion.db")
# Conectar a la base de datos
conn = sqlite3.connect(db_path)

# Ejecutar una consulta y cargarla en un DataFrame
query = "SELECT IdEXCURSION, fecha, lugar FROM excursion where fecha = '24/10/2024'"
df = pd.read_sql_query(query, conn)

# Mostrar el DataFrame
print(df)

# Cerrar la conexión
conn.close()
