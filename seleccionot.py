import tkinter as tk
from tkinter import ttk

def seleccionar_ot(parent, conexion):
    ventana = tk.Toplevel(parent)
    ventana.title("Seleccionar Orden de Trabajo")
    ventana.geometry("600x400")
    ventana.transient(parent)
    ventana.grab_set()

    ot_seleccionada = {"id_ot": None}

    tk.Label(ventana, text="Seleccione una Orden de Trabajo:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=5)

    tree = ttk.Treeview(ventana, columns=("id_ot", "fecha", "equipo", "estado"), show="headings")
    tree.heading("id_ot", text="ID OT")
    tree.heading("fecha", text="Fecha")
    tree.heading("equipo", text="Equipo / Sector")
    tree.heading("estado", text="Estado")

    tree.column("id_ot", width=60, anchor="center")
    tree.column("fecha", width=100, anchor="center")
    tree.column("equipo", width=250, anchor="w")
    tree.column("estado", width=100, anchor="center")

    tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Cargar OTs
    cursor = conexion.cursor()
    cursor.execute("SELECT id_ot, fecha, equipo, estado FROM ordenes_trabajo ORDER BY id_ot DESC")
    for fila in cursor.fetchall():
        tree.insert("", "end", values=fila)

    def confirmar():
        sel = tree.focus()
        if sel:
            ot_seleccionada["id_ot"] = tree.item(sel, "values")[0]
            ventana.destroy()

    btn_frame = tk.Frame(ventana)
    btn_frame.pack(fill=tk.X, padx=10, pady=10)
    tk.Button(btn_frame, text="Aceptar", command=confirmar, bg="#4CAF50", fg="white", width=10).pack(side=tk.RIGHT, padx=5)
    tk.Button(btn_frame, text="Cancelar", command=ventana.destroy, bg="#f44336", fg="white", width=10).pack(side=tk.RIGHT, padx=5)

    parent.wait_window(ventana)
    return ot_seleccionada["id_ot"]