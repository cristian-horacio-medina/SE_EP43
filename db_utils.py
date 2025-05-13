import os
import sys
import shutil
import sqlite3

def get_resource_path(relative_path):
    """Devuelve la ruta a recursos, sea en desarrollo o empaquetado."""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_db_path():
    """Devuelve la ruta al archivo Excursion.db en Documents. Lo copia si no existe."""
    documents_path = os.path.join(os.path.expanduser("~"), "Documents")
    os.makedirs(documents_path, exist_ok=True)

    destino_db = os.path.join(documents_path, "Excursion.db")

    if not os.path.exists(destino_db):
        origen_db = get_resource_path("Excursion.db")
        shutil.copy(origen_db, destino_db)

    return destino_db

def eliminar_excursion_por_id(IdEXCURSION):
    """Elimina una excursión por su ID. Devuelve True si se eliminó, False si no se encontró."""
    conn = None
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM excursion WHERE IdEXCURSION = ?", (IdEXCURSION,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()
