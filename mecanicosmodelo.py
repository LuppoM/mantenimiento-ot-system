def obtener_mecanicos(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, nombre
        FROM mecanicos
        ORDER BY nombre
    """)
    return cursor.fetchall()
