import sqlite3

# Ruta donde querés guardar la base de datos
ruta_bd = "K:/Mi unidad/Diplomatura/GESTION MANTENIMIENTO/mantenimiento.sqlite3"

# Conectar (si no existe la crea)
conn = sqlite3.connect(ruta_bd)
cursor = conn.cursor()

# Crear tabla OT
cursor.execute("""
CREATE TABLE IF NOT EXISTS OT (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Codigo TEXT,
    Version TEXT,
    MantenimientoCorrectivo TEXT,
    Fecha TEXT,
    Planta TEXT,
    Sector TEXT,
    Parte TEXT,
    Nave TEXT,
    Equipo TEXT,
    Elemento TEXT,
    NombreSolicitante TEXT,
    Area TEXT,
    DescripcionDefecto TEXT,
    Observaciones TEXT,
    Prioridad TEXT,
    Solucion TEXT,
    FechaCierreOT TEXT,
    DescripcionSolucion TEXT,
    MaterialUtilizado TEXT,
    NombreRealizo TEXT,
    AproboSolicitante TEXT,
    AproboMant TEXT,
    AproboCalidad TEXT
    Realizada TEXT          
)
""")

# Crear tabla partediario
cursor.execute("""
CREATE TABLE IF NOT EXISTS partediario (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Fecha TEXT,
    Turno TEXT,
    Operador TEXT,
    Actividad TEXT,
    Observaciones TEXT
)
""")

# Guardar y cerrar
conn.commit()
conn.close()

print("Base de datos y tablas creadas correctamente.")
