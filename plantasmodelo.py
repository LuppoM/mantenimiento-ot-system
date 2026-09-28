def obtener_plantas(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM plantas")
    return cursor.fetchall()

def eliminar_planta(conexion, planta_id):
    cursor = conexion.cursor()
    # Nota: Habría que validar que no tenga sectores asociados antes de borrar
    cursor.execute("DELETE FROM plantas WHERE id = ?", (planta_id,))
    conexion.commit()

def guardar_planta(conexion, nombre, planta_id=None):
    cursor = conexion.cursor()
    if planta_id:
        cursor.execute("UPDATE plantas SET nombre = ? WHERE id = ?", (nombre, planta_id))
    else:
        cursor.execute("INSERT INTO plantas (nombre) VALUES (?)", (nombre,))
    conexion.commit()