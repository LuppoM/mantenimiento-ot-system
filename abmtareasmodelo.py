import sqlite3

def insertar_tarea(conexion, datos):
    # Inserta los datos mapeados desde la interfaz
    campos = ", ".join([f"[{k}]" for k in datos.keys()])
    placeholders = ", ".join(["?"] * len(datos))
    sql = f"INSERT INTO tareasfinsemana ({campos}) VALUES ({placeholders})"
    
    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()))
    conexion.commit()
    cursor.close()

def actualizar_tarea(conexion, id_tarea, datos):
    # Actualiza un registro existente usando su ID[cite: 1]
    sets = ", ".join([f"[{k}] = ?" for k in datos.keys()])
    sql = f"UPDATE tareasfinsemana SET {sets} WHERE id_tarea = ?"
    
    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()) + [id_tarea])
    conexion.commit()
    cursor.close()

def obtener_proximo_id(conexion):
    # Calcula el siguiente ID para mostrarlo en el formulario[cite: 1]
    cur = conexion.cursor()
    cur.execute("SELECT COALESCE(MAX(id_tarea), 0) + 1 FROM tareasfinsemana")
    proximo = cur.fetchone()[0]
    cur.close()
    return proximo