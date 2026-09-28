import sqlite3

def obtener_proximo_id_nota(conexion):
    cur = conexion.cursor()
    try:
        cur.execute("SELECT COALESCE(MAX(id_nota), 0) + 1 FROM notas_pedido")
        return cur.fetchone()[0]
    finally:
        cur.close()

def insertar_nota_pedido(conexion, cabecera, detalles):
    cursor = conexion.cursor()
    try:
        if "id_nota" in cabecera:
            cabecera.pop("id_nota")

        columnas_validas = [
            "id_ot", "fecha_pedido", "fecha_requerida", "destino", 
            "autor", "tipo_gasto", "mano_de_obra", "justificacion", "estado"
        ]

        cabecera_filtrada = {k: v for k, v in cabecera.items() if k in columnas_validas}

        campos = ", ".join([f"[{k}]" for k in cabecera_filtrada.keys()])
        placeholders = ", ".join(["?"] * len(cabecera_filtrada))
        
        sql_cabecera = f"INSERT INTO notas_pedido ({campos}) VALUES ({placeholders})"
        cursor.execute(sql_cabecera, list(cabecera_filtrada.values()))
        
        id_nota = cursor.lastrowid

        sql_detalle = """
            INSERT INTO detalle_nota_pedido (id_nota, num_item, cantidad, detalle, destino_equipo)
            VALUES (?, ?, ?, ?, ?)
        """
        for item in detalles:
            if isinstance(item, dict):
                num_item = item.get("num_item", 1)
                cantidad = item.get("cantidad", 1.0)
                detalle = item.get("detalle", "")
                destino_equipo = item.get("destino_equipo", "")
            else:
                num_item, cantidad, detalle, destino_equipo = item[0], item[1], item[2], item[3]

            cursor.execute(sql_detalle, (id_nota, num_item, float(cantidad), detalle, destino_equipo))

        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()

def actualizar_nota_pedido(conexion, id_nota, cabecera, detalles):
    cursor = conexion.cursor()
    try:
        if "id_nota" in cabecera:
            cabecera.pop("id_nota")

        columnas_validas = [
            "id_ot", "fecha_pedido", "fecha_requerida", "destino", 
            "autor", "tipo_gasto", "mano_de_obra", "justificacion", "estado"
        ]
        cabecera_filtrada = {k: v for k, v in cabecera.items() if k in columnas_validas}

        sets = ", ".join([f"[{k}] = ?" for k in cabecera_filtrada.keys()])
        sql_cabecera = f"UPDATE notas_pedido SET {sets} WHERE id_nota = ?"
        cursor.execute(sql_cabecera, list(cabecera_filtrada.values()) + [id_nota])

        cursor.execute("DELETE FROM detalle_nota_pedido WHERE id_nota = ?", (id_nota,))
        
        sql_detalle = """
            INSERT INTO detalle_nota_pedido (id_nota, num_item, cantidad, detalle, destino_equipo)
            VALUES (?, ?, ?, ?, ?)
        """
        for item in detalles:
            if isinstance(item, dict):
                num_item = item.get("num_item", 1)
                cantidad = item.get("cantidad", 1.0)
                detalle = item.get("detalle", "")
                destino_equipo = item.get("destino_equipo", "")
            else:
                num_item, cantidad, detalle, destino_equipo = item[0], item[1], item[2], item[3]

            cursor.execute(sql_detalle, (id_nota, num_item, float(cantidad), detalle, destino_equipo))

        conexion.commit()
        return True
    except Exception as e:
        conexion.rollback()
        raise e
    finally:
        cursor.close()