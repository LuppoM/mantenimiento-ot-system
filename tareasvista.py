import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Tareas de Fin de Semana - Mantenimiento")
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

def crear_toolstrip(ventana, agregar, modificar, eliminar, imprimir):
    toolstrip = tk.Frame(ventana, bg="#dde6ed")
    toolstrip.pack(fill=tk.X)
    fuente = ("Segoe UI", 12, "bold")
    fg, bg, hover = "#003366", "#cfe2f3", "#a4c2f4"

    def boton(texto, comando):
        return tk.Button(toolstrip, text=texto, font=fuente, fg=fg, bg=bg,
                         activebackground=hover, activeforeground=fg, bd=0,
                         relief="flat", command=comando)

    boton("Agregar", agregar).pack(side=tk.LEFT, padx=10, pady=10)
    boton("Modificar", modificar).pack(side=tk.LEFT, padx=10, pady=10)
    boton("Imprimir", imprimir).pack(side=tk.LEFT, padx=10, pady=10)
    boton("Eliminar", eliminar).pack(side=tk.LEFT, padx=10, pady=10)
    boton("Cerrar", ventana.destroy).pack(side=tk.LEFT, padx=10, pady=10)

def crear_filtro(ventana, callback_buscar):
    frame = tk.Frame(ventana, bg="#f0f4f8")
    frame.pack(fill=tk.X, padx=15, pady=(8, 5))
    tk.Label(frame, text="Filtrar por:", bg="#f0f4f8", font=("Segoe UI", 11, "bold"), fg="#003366").pack(side=tk.LEFT, padx=5)
    combo_columna = ttk.Combobox(frame, state="readonly", width=20)
    combo_columna.pack(side=tk.LEFT, padx=5)
    entrada = ttk.Entry(frame, width=40)
    entrada.pack(side=tk.LEFT, padx=5)
    entrada.bind("<Return>", lambda e: callback_buscar(combo_columna.get(), entrada.get()))
    return combo_columna, entrada

def crear_tabla(ventana, filas_visibles=18):
    contenedor = tk.Frame(ventana, bg="#f0f4f8")
    contenedor.pack(fill=tk.BOTH, expand=True, padx=15, pady=10) 
    
    tree = ttk.Treeview(contenedor, show="headings", height=filas_visibles)
    
    scroll_y = ttk.Scrollbar(contenedor, orient=tk.VERTICAL, command=tree.yview)
    scroll_x = ttk.Scrollbar(contenedor, orient=tk.HORIZONTAL, command=tree.xview)
    
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    
    contenedor.grid_rowconfigure(0, weight=1)
    contenedor.grid_columnconfigure(0, weight=1)
    
    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#d9e1f2", foreground="#003366")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background="white")
    
    return tree

# --- NUEVA FUNCIÓN AGREGADA A LA VISTA PARA RESOLVER EL PROBLEMA ---
def limpiar_y_llenar_tabla(tree, lista_de_filas):
    """
    Esta función vacía por completo el Treeview antes de insertar los nuevos datos.
    También remueve los saltos de línea (\n) automáticos para que no colapse el texto.
    """
    # 1. BORRADO CRÍTICO: Esto evita que se superpongan los textos antiguos
    for item in tree.get_children():
        tree.delete(item)
        
    # 2. INSERCIÓN LIMPIA
    for fila in lista_de_filas:
        # Convertimos a lista para poder modificar las celdas con saltos de línea
        valores = list(fila)
        
        # Limpiamos los saltos de línea de cada celda para evitar el colapso visual
        valores_limpios = [
            str(celda).replace("\n", "  —  ") if celda is not None else "" 
            for celda in valores
        ]
        
        tree.insert("", "end", values=valores_limpios)