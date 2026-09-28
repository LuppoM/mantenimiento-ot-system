def insertar_planta(conexion, datos):
    campos = ", ".join([f"[{k}]" for k in datos.keys()])
    placeholders = ", ".join(["?"] * len(datos))
    sql = f"INSERT INTO plantas ({campos}) VALUES ({placeholders})"
    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()))
    conexion.commit()
    cursor.close()

def actualizar_planta(conexion, id_planta, datos):
    sets = ", ".join([f"[{k}] = ?" for k in datos.keys()])
    sql = f"UPDATE plantas SET {sets} WHERE id = ?"
    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()) + [id_planta])
    conexion.commit()
    cursor.close()