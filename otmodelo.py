import sqlite3

# 1. Trae TODO para el inicio
def obtener_todas_las_ot(conexion):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM OT")
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        return columnas, datos
    finally:
        cursor.close()

# 2. Trae solo lo que dice el TEXTBOX
def filtrar_ot_por_texto(conexion, columna, valor):
    cursor = conexion.cursor()
    try:
        sql = f"SELECT * FROM OT WHERE [{columna}] LIKE ?"
        cursor.execute(sql, (f"%{valor}%",))
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        return columnas, datos
    finally:
        cursor.close()

# --- Otras funciones ---
def eliminar_ot(conexion, id_ot):
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM OT WHERE ID = ?", (id_ot,))
        conexion.commit()
        return True
    finally:
        cursor.close()

def obtener_ot_por_id(conexion, id_ot):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM OT WHERE ID = ?", (id_ot,))
        fila = cursor.fetchone()
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, fila)) if fila else None
    finally:
        cursor.close()