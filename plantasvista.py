import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Gestión de Plantas / Unidades")
    ventana.state("zoomed")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()
    if os.path.exists(ICON_PATH):
        try: ventana.iconbitmap(ICON_PATH)
        except: pass
    return ventana

def crear_toolstrip(ventana, agregar, modificar, eliminar):
    toolstrip = tk.Frame(ventana, bg="#dde6ed")
    toolstrip.pack(fill=tk.X)
    fuente = ("Segoe UI", 12, "bold")
    fg, bg, hover = "#003366", "#cfe2f3", "#a4c2f4"

    def boton(texto, comando):
        return tk.Button(toolstrip, text=texto, font=fuente, fg=fg, bg=bg,
                         activebackground=hover, activeforeground=fg, bd=0,
                         relief="flat", command=comando)

    # Siguiendo tu orden de botones
    btn_add = boton("Agregar Planta", agregar)
    btn_add.pack(side=tk.LEFT, padx=10, pady=10)
    
    btn_mod = boton("Modificar", modificar)
    btn_mod.pack(side=tk.LEFT, padx=10, pady=10)
    
    btn_eli = boton("Eliminar", eliminar)
    btn_eli.pack(side=tk.LEFT, padx=10, pady=10)
    
    boton("Cerrar", ventana.destroy).pack(side=tk.LEFT, padx=10, pady=10)

    # Retornamos diccionario por si necesitás configurar algo después en el controlador
    return {
        "agregar": btn_add,
        "modificar": btn_mod,
        "eliminar": btn_eli,
        "atras": None # Para mantener compatibilidad con tu controlador
    }

def crear_tabla(ventana, filas_visibles=18):
    # Contenedor de la tabla: quitamos el expand=True para que no tire hacia abajo
    contenedor = tk.Frame(ventana, bg="#f0f4f8")
    contenedor.pack(fill=tk.X, padx=15, pady=10) 
    
    # El height=filas_visibles ahora manda sobre el tamaño real
    tree = ttk.Treeview(contenedor, columns=("id", "nombre"), show="headings", height=filas_visibles)
    
    tree.heading("id", text="ID")
    tree.heading("nombre", text="Nombre de la Planta / Unidad")
    
    tree.column("id", width=100, anchor="center", stretch=tk.NO)
    tree.column("nombre", width=600, stretch=tk.YES)

    scroll_y = ttk.Scrollbar(contenedor, orient=tk.VERTICAL, command=tree.yview)
    scroll_x = ttk.Scrollbar(contenedor, orient=tk.HORIZONTAL, command=tree.xview)
    
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    
    # Layout Grid
    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    
    # Solo le damos peso a la columna para que ocupe el ancho, pero no el alto infinito
    contenedor.grid_columnconfigure(0, weight=1)
    
    # Estilos (Clam)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#d9e1f2", foreground="#003366")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="white")
    
    return tree