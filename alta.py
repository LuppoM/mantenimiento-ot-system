import sqlite3
import tkinter as tk
from tkinter import messagebox

# Ruta a la base de datos
RUTA_BD = "K:/Mi unidad/Diplomatura/GESTION MANTENIMIENTO/mantenimiento.sqlite3"

def guardar_datos():
    datos = [entry.get() for entry in entradas]
    
    conn = sqlite3.connect(RUTA_BD)
    cursor = conn.cursor()

    query = """
        INSERT INTO OT (
            Codigo, Version, MantenimientoCorrectivo, Fecha, Planta, Sector,
            Parte, Nave, Equipo, Elemento, NombreSolicitante, Area,
            DescripcionDefecto, Observaciones, Prioridad, Solucion,
            FechaCierreOT, DescripcionSolucion, MaterialUtilizado,
            NombreRealizo, AproboSolicitante, AproboMant, AproboCalidad
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.execute(query, datos)
        conn.commit()
        messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        for entry in entradas:
            entry.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        conn.close()

# Campos del formulario
campos = [
    "Codigo", "Version", "MantenimientoCorrectivo", "Fecha", "Planta", "Sector",
    "Parte", "Nave", "Equipo", "Elemento", "NombreSolicitante", "Area",
    "DescripcionDefecto", "Observaciones", "Prioridad", "Solucion",
    "FechaCierreOT", "DescripcionSolucion", "MaterialUtilizado",
    "NombreRealizo", "AproboSolicitante", "AproboMant", "AproboCalidad"
]

# Interfaz con Tkinter
root = tk.Tk()
root.title("Alta de Orden de Trabajo")

entradas = []

for i, campo in enumerate(campos):
    tk.Label(root, text=campo).grid(row=i, column=0, padx=5, pady=2, sticky='e')
    entry = tk.Entry(root, width=40)
    entry.grid(row=i, column=1, padx=5, pady=2)
    entradas.append(entry)

tk.Button(root, text="Guardar", command=guardar_datos).grid(row=len(campos), column=0, columnspan=2, pady=10)

root.mainloop()
