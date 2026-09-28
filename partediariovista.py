# partediariovista.py
import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

# ============================================================
# VENTANA PARTE DIARIO
# ============================================================
def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Parte Diario")
    ventana.state("zoomed")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()

    if os.path.exists(ICON_PATH):
        try:
            ventana.iconbitmap(ICON_PATH)
        except:
            pass

    return ventana


# ============================================================
# TOOLSTRIP
# ============================================================
def crear_toolstrip(
    ventana,
    abrir_agregar=None,
    abrir_modificar=None,
    abrir_eliminar=None
):
    toolstrip = tk.Frame(ventana, bg="#dde6ed")
    toolstrip.pack(fill=tk.X)

    fuente = ("Segoe UI", 12, "bold")
    fg = "#003366"
    bg = "#cfe2f3"
    hover = "#a4c2f4"

    def boton(texto, comando):
        return tk.Button(
            toolstrip,
            text=texto,
            font=fuente,
            fg=fg,
            bg=bg,
            activebackground=hover,
            activeforeground=fg,
            bd=0,
            relief="flat",
            command=comando
        )

    if abrir_agregar:
        boton("Agregar", abrir_agregar).pack(side=tk.LEFT, padx=10, pady=10)

    if abrir_modificar:
        boton("Modificar", abrir_modificar).pack(side=tk.LEFT, padx=10, pady=10)

    if abrir_eliminar:
        boton("Eliminar", abrir_eliminar).pack(side=tk.LEFT, padx=10, pady=10)

    boton("Cerrar", ventana.destroy).pack(side=tk.LEFT, padx=10, pady=10)

    tk.Frame(toolstrip, bg="#dde6ed").pack(side=tk.LEFT, expand=True, fill=tk.X)


# ============================================================
# FILTRO
# ============================================================
def crear_filtro(ventana, callback_filtro):
    frame = tk.Frame(ventana, bg="#f0f4f8")
    frame.pack(fill=tk.X, padx=15, pady=(8, 5))

    tk.Label(
        frame,
        text="Filtrar por:",
        bg="#f0f4f8",
        font=("Segoe UI", 12, "bold"),
        fg="#003366"
    ).pack(side=tk.LEFT, padx=5)

    combo = ttk.Combobox(
        frame,
        state="readonly",
        width=30,
        values=["ID", "Fecha", "Nombre", "Turno", "Codigo maquina", "Reporte"]
    )
    combo.set("Nombre")
    combo.pack(side=tk.LEFT, padx=8)

    entry = ttk.Entry(frame)
    entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)

    entry.bind(
        "<Return>",
        lambda e: callback_filtro(combo.get(), entry.get())
    )

    return combo, entry


# ============================================================
# TABLA
# ============================================================
def crear_tabla(ventana, filas_visibles=18):
    contenedor = tk.Frame(ventana, bg="#f0f4f8")
    contenedor.pack(fill=tk.X, padx=15, pady=10)

    frame_tree = tk.Frame(contenedor, bg="#f0f4f8")
    frame_tree.pack(fill=tk.BOTH, expand=False)

    tree = ttk.Treeview(
        frame_tree,
        show="headings",
        height=filas_visibles
    )

    scroll_y = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=tree.yview)
    scroll_x = ttk.Scrollbar(frame_tree, orient=tk.HORIZONTAL, command=tree.xview)

    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    frame_tree.grid_rowconfigure(0, weight=1)
    frame_tree.grid_columnconfigure(0, weight=1)

    tree["columns"] = (
        "ID", "Fecha", "Nombre", "Turno", "Codigo maquina", "Reporte"
    )

    tree.column("ID", width=80, anchor="center")

    for c in tree["columns"]:
        tree.heading(c, text=c)
        if c != "ID":
            tree.column(c, width=200, anchor="w")

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),
        background="#d9e1f2",
        foreground="#003366"
    )

    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=28,
        background="white"
    )

    return tree
