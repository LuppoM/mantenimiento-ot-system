import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")


# ------------------------------------------------------------
# VENTANA MECÁNICOS
# ------------------------------------------------------------
def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Mecánicos")
    ventana.state("zoomed")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()

    # Icono
    try:
        ventana.iconbitmap(ICON_PATH)
    except:
        pass

    return ventana


# ------------------------------------------------------------
# TOOLSTRIP
# ------------------------------------------------------------
def crear_toolstrip(ventana):
    toolstrip = tk.Frame(ventana, bg="#dde6ed", height=70)
    toolstrip.pack(fill=tk.X, side=tk.TOP)
    toolstrip.pack_propagate(False)

    fuente = ("Segoe UI", 12, "bold")
    fg = "#003366"
    bg = "#cfe2f3"
    hover = "#a4c2f4"

    def boton(texto, x):
        b = tk.Button(
            toolstrip,
            text=texto,
            font=fuente,
            fg=fg,
            bg=bg,
            activebackground=hover,
            activeforeground=fg,
            bd=0,
            relief="flat"
        )
        b.place(x=x, y=15, width=140, height=40)
        return b

    btn_agregar = boton("Agregar", 10)
    btn_modificar = boton("Modificar", 160)
    btn_eliminar = boton("Eliminar", 310)
    btn_atras = boton("Cerrar", 460)

    return {
        "agregar": btn_agregar,
        "modificar": btn_modificar,
        "eliminar": btn_eliminar,
        "atras": btn_atras
    }


# ------------------------------------------------------------
# TABLA
# ------------------------------------------------------------
def crear_tabla(ventana):
    contenedor = tk.Frame(ventana, bg="#f0f4f8")
    contenedor.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    columnas = ("id", "nombre")

    tree = ttk.Treeview(
        contenedor,
        columns=columnas,
        show="headings"
    )

    tree.heading("id", text="ID")
    tree.heading("nombre", text="Mecánico")

    tree.column("id", width=80, anchor="center")
    tree.column("nombre", width=350)

    scroll_y = ttk.Scrollbar(contenedor, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(contenedor, orient="horizontal", command=tree.xview)

    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")

    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)

    # ESTILO
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
