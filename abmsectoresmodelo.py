import sqlite3


def insertar_sector(conexion, nombre, planta):
    cursor = conexion.cursor()
    cursor.execute(
        """
        INSERT INTO sectores (nombre, planta)
        VALUES (?, ?)
        """,
        (nombre, planta)
    )
    conexion.commit()


def modificar_sector(conexion, sector_id, nombre, planta):
    cursor = conexion.cursor()
    cursor.execute(
        """
        UPDATE sectores
        SET nombre = ?, planta = ?
        WHERE id = ?
        """,
        (nombre, planta, sector_id)
    )
    conexion.commit()
