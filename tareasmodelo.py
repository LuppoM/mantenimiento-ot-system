import sqlite3

def obtener_todas_las_tareas(conexion):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM tareasfinsemana ORDER BY fecha DESC")
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        return columnas, datos
    finally:
        cursor.close()

def filtrar_tareas(conexion, columna, valor):
    cursor = conexion.cursor()
    try:
        sql = f"SELECT * FROM tareasfinsemana WHERE [{columna}] LIKE ? ORDER BY fecha DESC"
        cursor.execute(sql, (f"%{valor}%",))
        datos = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        return columnas, datos
    finally:
        cursor.close()

def eliminar_tarea(conexion, id_tarea):
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM tareasfinsemana WHERE id_tarea = ?", (id_tarea,))
        conexion.commit()
        return True
    finally:
        cursor.close()

def obtener_tarea_por_id(conexion, id_tarea):
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT * FROM tareasfinsemana WHERE id_tarea = ?", (id_tarea,))
        fila = cursor.fetchone()
        columnas = [desc[0] for desc in cursor.description]
        return dict(zip(columnas, fila)) if fila else None
    finally:
        cursor.close()