import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

def crear_ventana_abm(parent, titulo="Nota de Pedido"):
    ventana = tk.Toplevel(parent)
    ventana.title(titulo)
    ventana.geometry("920x750")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()
    if os.path.exists(ICON_PATH):
        try: ventana.iconbitmap(ICON_PATH)
        except: pass
    return ventana

def crear_formulario_abm(ventana, callback_buscar_ot):
    # --- BARRA SUPERIOR ---
    top_frame = tk.Frame(ventana, bg="#f0f4f8")
    top_frame.pack(fill=tk.X, padx=15, pady=8)
    
    lbl_titulo = tk.Label(top_frame, text="Solicitud - Nota de Pedido", font=("Segoe UI", 12, "bold"), fg="#003366", bg="#f0f4f8")
    lbl_titulo.pack(side=tk.LEFT)

    # --- DATOS CABECERA ---
    frame_datos = tk.LabelFrame(ventana, text=" Datos de la Solicitud ", bg="#f0f4f8", font=("Segoe UI", 10, "bold"), fg="#003366")
    frame_datos.pack(fill=tk.X, padx=15, pady=5)

    entries = {}

    # Fila 0: N° Nota y OT
    tk.Label(frame_datos, text="N° Nota:", bg="#f0f4f8").grid(row=0, column=0, sticky="e", padx=5, pady=4)
    e_nota = ttk.Entry(frame_datos, width=15, state="disabled")
    e_nota.grid(row=0, column=1, sticky="w", padx=5, pady=4)
    entries["id_nota"] = e_nota

    tk.Label(frame_datos, text="OT Asociada:", bg="#f0f4f8").grid(row=0, column=2, sticky="e", padx=5, pady=4)
    frame_ot = tk.Frame(frame_datos, bg="#f0f4f8")
    frame_ot.grid(row=0, column=3, sticky="w", padx=5, pady=4)
    
    e_ot = ttk.Entry(frame_ot, width=12)
    e_ot.pack(side=tk.LEFT)
    btn_buscar_ot = tk.Button(frame_ot, text="Buscar", font=("Segoe UI", 8, "bold"), command=callback_buscar_ot, bg="#d0e0f0")
    btn_buscar_ot.pack(side=tk.LEFT, padx=(2, 0))
    entries["id_ot"] = e_ot

    # Fila 1: Fechas y Destino
    tk.Label(frame_datos, text="Fecha Pedido:", bg="#f0f4f8").grid(row=1, column=0, sticky="e", padx=5, pady=4)
    e_fpedido = DateEntry(frame_datos, date_pattern="dd/mm/yyyy", width=12)
    e_fpedido.grid(row=1, column=1, sticky="w", padx=5, pady=4)
    entries["fecha_pedido"] = e_fpedido

    tk.Label(frame_datos, text="Fecha Requerida:", bg="#f0f4f8").grid(row=1, column=2, sticky="e", padx=5, pady=4)
    e_frequerida = DateEntry(frame_datos, date_pattern="dd/mm/yyyy", width=12)
    e_frequerida.grid(row=1, column=3, sticky="w", padx=5, pady=4)
    entries["fecha_requerida"] = e_frequerida

    # Fila 2: Planta Destino y Autor
    tk.Label(frame_datos, text="Planta Destino:", bg="#f0f4f8").grid(row=2, column=0, sticky="e", padx=5, pady=4)
    cb_dest = ttk.Combobox(frame_datos, values=["Planta Chocolates", "Planta Golosinas"], state="readonly", width=20)
    cb_dest.set("Planta Golosinas")
    cb_dest.grid(row=2, column=1, sticky="w", padx=5, pady=4)
    entries["destino"] = cb_dest

    tk.Label(frame_datos, text="Solicitante / Autor:", bg="#f0f4f8").grid(row=2, column=2, sticky="e", padx=5, pady=4)
    e_autor = ttk.Entry(frame_datos, width=22)
    e_autor.grid(row=2, column=3, sticky="w", padx=5, pady=4)
    entries["autor"] = e_autor

    # Fila 3: Clasificación de Gasto y Mano de Obra
    tk.Label(frame_datos, text="Tipo de Gasto:", bg="#f0f4f8").grid(row=3, column=0, sticky="e", padx=5, pady=4)
    cb_gasto = ttk.Combobox(frame_datos, values=["Gasto de Mantenimiento", "Inversión"], state="readonly", width=20)
    cb_gasto.set("Gasto de Mantenimiento")
    cb_gasto.grid(row=3, column=1, sticky="w", padx=5, pady=4)
    entries["tipo_gasto"] = cb_gasto

    tk.Label(frame_datos, text="Mano de Obra:", bg="#f0f4f8").grid(row=3, column=2, sticky="e", padx=5, pady=4)
    cb_mo = ttk.Combobox(frame_datos, values=["Mano de Obra Interna", "Tercerizado (Servicio Externo)"], state="readonly", width=22)
    cb_mo.set("Mano de Obra Interna")
    cb_mo.grid(row=3, column=3, sticky="w", padx=5, pady=4)
    entries["mano_de_obra"] = cb_mo

    # Fila 4: Estado de la Nota
    tk.Label(frame_datos, text="Estado Nota:", bg="#f0f4f8").grid(row=4, column=0, sticky="e", padx=5, pady=4)
    cb_estado = ttk.Combobox(frame_datos, values=["PENDIENTE", "APROBADO", "RECHAZADO"], state="readonly", width=20)
    cb_estado.set("PENDIENTE")
    cb_estado.grid(row=4, column=1, sticky="w", padx=5, pady=4)
    entries["estado"] = cb_estado

    # Fila 5: Justificación del Pedido (Text)
    tk.Label(frame_datos, text="Justificación del Pedido:", bg="#f0f4f8").grid(row=5, column=0, sticky="ne", padx=5, pady=4)
    txt_just = tk.Text(frame_datos, width=62, height=3, font=("Segoe UI", 9))
    txt_just.grid(row=5, column=1, columnspan=3, sticky="w", padx=5, pady=4)
    entries["justificacion"] = txt_just

    # --- SECCIÓN ITEMS ---
    frame_items = tk.LabelFrame(ventana, text=" Ítems y Repuestos Solicitados ", bg="#f0f4f8", font=("Segoe UI", 10, "bold"), fg="#003366")
    frame_items.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

    input_frame = tk.Frame(frame_items, bg="#f0f4f8")
    input_frame.pack(fill=tk.X, padx=5, pady=5)

    tk.Label(input_frame, text="Cant:", bg="#f0f4f8").pack(side=tk.LEFT, padx=2)
    e_item_cant = ttk.Entry(input_frame, width=6)
    e_item_cant.pack(side=tk.LEFT, padx=4)

    tk.Label(input_frame, text="Detalle / Ítem:", bg="#f0f4f8").pack(side=tk.LEFT, padx=2)
    e_item_det = ttk.Entry(input_frame, width=30)
    e_item_det.pack(side=tk.LEFT, padx=4)

    tk.Label(input_frame, text="Destino / Equipo Exacto:", bg="#f0f4f8").pack(side=tk.LEFT, padx=2)
    e_item_dest_eq = ttk.Entry(input_frame, width=30)
    e_item_dest_eq.pack(side=tk.LEFT, padx=4)

    entries_item = {
        "cantidad": e_item_cant,
        "detalle": e_item_det,
        "destino_equipo": e_item_dest_eq
    }

    # Grilla de Ítems (Con columna id_detalle oculta para evitar desfase de mapeo)
    tree_items = ttk.Treeview(frame_items, columns=("id_detalle", "num", "cantidad", "detalle", "destino_equipo"), show="headings", height=6)
    
    tree_items.heading("id_detalle", text="")
    tree_items.heading("num", text="Item N°")
    tree_items.heading("cantidad", text="Cant.")
    tree_items.heading("detalle", text="Detalle / Repuesto")
    tree_items.heading("destino_equipo", text="Ubicación / Equipo Destino")

    tree_items.column("id_detalle", width=0, stretch=False)
    tree_items.column("num", width=60, anchor="center")
    tree_items.column("cantidad", width=60, anchor="center")
    tree_items.column("detalle", width=300, anchor="w")
    tree_items.column("destino_equipo", width=300, anchor="w")

    tree_items.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    return entries, entries_item, tree_items, input_frame