# abmotmodelo.py

def insertar_ot(conexion, datos):
    campos = ", ".join([f"[{k}]" for k in datos.keys()])
    placeholders = ", ".join(["?"] * len(datos))
    sql = f"INSERT INTO OT ({campos}) VALUES ({placeholders})"

    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()))
    conexion.commit()
    cursor.close()


def actualizar_ot(conexion, id_ot, datos):
    sets = ", ".join([f"[{k}] = ?" for k in datos.keys()])
    sql = f"UPDATE OT SET {sets} WHERE ID = ?"

    cursor = conexion.cursor()
    cursor.execute(sql, list(datos.values()) + [id_ot])
    conexion.commit()
    cursor.close()
def obtener_proximo_id(conexion):
    cur = conexion.cursor()
    cur.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM OT")
    return cur.fetchone()[0]

def obtener_sectores_por_planta(conexion, planta):
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT nombre FROM sectores WHERE planta = ? ORDER BY nombre",
        (planta,)
    )
    datos = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    return datos

def obtener_proximo_id(conexion):
    cur = conexion.cursor()
    cur.execute("SELECT COALESCE(MAX(ID), 0) + 1 FROM OT")
    proximo = cur.fetchone()[0]
    cur.close()
    return proximo

def obtener_mecanicos(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM mecanicos ORDER BY nombre")
    datos = [fila[0] for fila in cursor.fetchall()]
    cursor.close()
    return datos

