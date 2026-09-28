import sqlite3

def obtener_todas_las_np(conexion):
    cursor = conexion.cursor()
    query = """
        SELECT id_nota, id_ot, fecha_pedido, fecha_requerida, destino, autor, 
               tipo_gasto, mano_de_obra, justificacion, estado 
        FROM notas_pedido 
        ORDER BY id_nota DESC
    """
    cursor.execute(query)
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description] if cursor.description else []
    return columnas, filas

def filtrar_np_por_texto(conexion, columna, texto):
    cursor = conexion.cursor()
    query = f"""
        SELECT id_nota, id_ot, fecha_pedido, fecha_requerida, destino, autor, 
               tipo_gasto, mano_de_obra, justificacion, estado 
        FROM notas_pedido 
        WHERE [{columna}] LIKE ? 
        ORDER BY id_nota DESC
    """
    cursor.execute(query, (f"%{texto}%",))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description] if cursor.description else []
    return columnas, filas

def obtener_detalle_por_nota(conexion, id_nota):
    cursor = conexion.cursor()
    query = """
        SELECT id_detalle, id_nota, num_item, cantidad, detalle, destino_equipo 
        FROM detalle_nota_pedido 
        WHERE id_nota = ?
        ORDER BY num_item ASC
    """
    cursor.execute(query, (id_nota,))
    filas = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description] if cursor.description else []
    return columnas, filas

def obtener_nota_por_id(conexion, id_nota):
    cursor = conexion.cursor()
    query = "SELECT * FROM notas_pedido WHERE id_nota = ?"
    cursor.execute(query, (id_nota,))
    fila = cursor.fetchone()
    columnas = [desc[0] for desc in cursor.description] if cursor.description else []
    
    cabecera = dict(zip(columnas, fila)) if fila else {}
    
    # Obtenemos sus detalles ordenados por num_item
    query_det = """
        SELECT id_detalle, id_nota, num_item, cantidad, detalle, destino_equipo 
        FROM detalle_nota_pedido 
        WHERE id_nota = ? 
        ORDER BY num_item ASC
    """
    cursor.execute(query_det, (id_nota,))
    detalles = cursor.fetchall()
    
    return {"cabecera": cabecera, "detalles": detalles}

def eliminar_np(conexion, id_nota):
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM detalle_nota_pedido WHERE id_nota = ?", (id_nota,))
        cursor.execute("DELETE FROM notas_pedido WHERE id_nota = ?", (id_nota,))
        conexion.commit()
        return True
    except Exception:
        conexion.rollback()
        return False

# --- Alias de compatibilidad ---
def obtener_todas_las_notas(conexion): 
    return obtener_todas_las_np(conexion)

def filtrar_notas_por_texto(conexion, col, txt): 
    return filtrar_np_por_texto(conexion, col, txt)

def eliminar_nota_pedido(conexion, id_nota): 
    return eliminar_np(conexion, id_nota)