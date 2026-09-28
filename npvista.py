import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

def crear_ventana_np(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Notas de Pedido")
    ventana.state("zoomed")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()
    if os.path.exists(ICON_PATH):
        try: ventana.iconbitmap(ICON_PATH)
        except: pass
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

def crear_tablas(ventana):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#d9e1f2", foreground="#003366")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=26, background="white")

    # --- TABLA 1: CABECERA ---
    frame_cabecera = tk.Frame(ventana, bg="#f0f4f8")
    frame_cabecera.pack(fill=tk.X, padx=15, pady=(5, 5))

    cols_cabecera = ("id_nota", "id_ot", "fecha_pedido", "fecha_requerida", "destino", "autor", "tipo_gasto", "mano_de_obra", "justificacion", "estado")
    tree_cabecera = ttk.Treeview(frame_cabecera, columns=cols_cabecera, show="headings", height=10)
    
    # Encabezados Cabecera
    tree_cabecera.heading("id_nota", text="ID NOTA")
    tree_cabecera.heading("id_ot", text="ID OT")
    tree_cabecera.heading("fecha_pedido", text="FECHA PEDIDO")
    tree_cabecera.heading("fecha_requerida", text="FECHA REQUERIDA")
    tree_cabecera.heading("destino", text="DESTINO")
    tree_cabecera.heading("autor", text="AUTOR")
    tree_cabecera.heading("tipo_gasto", text="TIPO GASTO")
    tree_cabecera.heading("mano_de_obra", text="MANO DE OBRA")
    tree_cabecera.heading("justificacion", text="JUSTIFICACION")
    tree_cabecera.heading("estado", text="ESTADO")

    # Formato Columnas Cabecera
    tree_cabecera.column("id_nota", width=80, anchor="center")
    tree_cabecera.column("id_ot", width=80, anchor="center")
    tree_cabecera.column("fecha_pedido", width=110, anchor="center")
    tree_cabecera.column("fecha_requerida", width=120, anchor="center")
    tree_cabecera.column("destino", width=130, anchor="center")
    tree_cabecera.column("autor", width=110, anchor="center")
    tree_cabecera.column("tipo_gasto", width=150, anchor="center")
    tree_cabecera.column("mano_de_obra", width=150, anchor="center")
    tree_cabecera.column("justificacion", width=200, anchor="w")
    tree_cabecera.column("estado", width=110, anchor="center")

    scroll_y1 = ttk.Scrollbar(frame_cabecera, orient=tk.VERTICAL, command=tree_cabecera.yview)
    scroll_x1 = ttk.Scrollbar(frame_cabecera, orient=tk.HORIZONTAL, command=tree_cabecera.xview)
    tree_cabecera.configure(yscrollcommand=scroll_y1.set, xscrollcommand=scroll_x1.set)

    tree_cabecera.grid(row=0, column=0, sticky="nsew")
    scroll_y1.grid(row=0, column=1, sticky="ns")
    scroll_x1.grid(row=1, column=0, sticky="ew")
    frame_cabecera.grid_columnconfigure(0, weight=1)

    # --- TÍTULO DETALLE ---
    label_detalle = tk.Label(ventana, text="Ítems del Pedido Seleccionado", bg="#f0f4f8", 
                             font=("Segoe UI", 11, "bold"), fg="#003366", anchor="w")
    label_detalle.pack(fill=tk.X, padx=15, pady=(8, 2))

    # --- TABLA 2: DETALLE (Sin ID DETALLE ni ID NOTA) ---
    frame_detalle = tk.Frame(ventana, bg="#f0f4f8")
    frame_detalle.pack(fill=tk.X, padx=15, pady=(0, 10))

    cols_detalle = ("num_item", "cantidad", "detalle", "destino_equipo")
    tree_detalle = ttk.Treeview(frame_detalle, columns=cols_detalle, show="headings", height=7)
    
    # Encabezados Detalle
    tree_detalle.heading("num_item", text="NUM ITEM")
    tree_detalle.heading("cantidad", text="CANTIDAD")
    tree_detalle.heading("detalle", text="DETALLE")
    tree_detalle.heading("destino_equipo", text="DESTINO EQUIPO")

    # Formato Columnas Detalle
    tree_detalle.column("num_item", width=100, anchor="center")
    tree_detalle.column("cantidad", width=100, anchor="center")
    tree_detalle.column("detalle", width=350, anchor="w")
    tree_detalle.column("destino_equipo", width=300, anchor="w")

    scroll_y2 = ttk.Scrollbar(frame_detalle, orient=tk.VERTICAL, command=tree_detalle.yview)
    scroll_x2 = ttk.Scrollbar(frame_detalle, orient=tk.HORIZONTAL, command=tree_detalle.xview)
    tree_detalle.configure(yscrollcommand=scroll_y2.set, xscrollcommand=scroll_x2.set)

    tree_detalle.grid(row=0, column=0, sticky="nsew")
    scroll_y2.grid(row=0, column=1, sticky="ns")
    scroll_x2.grid(row=1, column=0, sticky="ew")
    frame_detalle.grid_columnconfigure(0, weight=1)

    return tree_cabecera, tree_detalle

def crear_ventana_notas(parent):
    return crear_ventana_np(parent)

def crear_tabla(ventana, filas_visibles=18):
    c, d = crear_tablas(ventana)
    return c