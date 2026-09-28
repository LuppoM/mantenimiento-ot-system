def insertar_partediario(conexion, datos):
    campos = ", ".join([f"[{k}]" for k in datos.keys()])
    placeholders = ", ".join(["?"] * len(datos))
    sql = f"INSERT INTO Partediario ({campos}) VALUES ({placeholders})"

    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()))
    conexion.commit()
    cursor.close()


def actualizar_partediario(conexion, id_pd, datos):
    sets = ", ".join([f"[{k}] = ?" for k in datos.keys()])
    sql = f"UPDATE Partediario SET {sets} WHERE ID = ?"

    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()) + [id_pd])
    conexion.commit()
    cursor.close()
def obtener_proximo_id(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(ID) FROM Partediario")
    ultimo = cursor.fetchone()[0]
    cursor.close()

    return 1 if ultimo is None else ultimo + 1