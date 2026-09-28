# sectoresmodelo.py

def obtener_sectores(conexion):
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, nombre, planta
        FROM sectores
        ORDER BY nombre
    """)
    return cursor.fetchall()
