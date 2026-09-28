def insertar_mecanico(conexion, nombre):
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO mecanicos (nombre) VALUES (?)",
        (nombre,)
    )
    conexion.commit()


def modificar_mecanico(conexion, mecanico_id, nombre):
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE mecanicos SET nombre = ? WHERE id = ?",
        (nombre, mecanico_id)
    )
    conexion.commit()
