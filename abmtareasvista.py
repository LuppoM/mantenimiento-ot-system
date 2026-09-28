import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import os
from principalvista import ICON_PATH
# Ruta para el icono (ajustar según tu estructura de carpetas)
ICON_PATH = "iconom.ico" 

def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Registro de Tareas de Fin de Semana")
    ventana.geometry("750x750")
    ventana.configure(bg="#e8eef3")
    ventana.transient(parent)
    ventana.grab_set()

    # Intento de cargar el icono con manejo de errores más robusto
    if os.path.exists(ICON_PATH):
        try:
            ventana.iconbitmap(ICON_PATH)
        except Exception as e:
            # En algunos sistemas (Linux/Mac) iconbitmap falla, se usa iconphoto como backup
            try:
                img = tk.PhotoImage(file=ICON_PATH)
                ventana.iconphoto(False, img)
            except:
                print(f"No se pudo cargar el icono: {e}")
    else:
        print(f"Ruta de icono no encontrada: {ICON_PATH}")
        
    return ventana

def crear_toolstrip(ventana, estado_texto, comando_guardar, comando_cancelar):
    barra = tk.Frame(ventana, bg="#dde6ed", height=55)
    barra.pack(side=tk.TOP, fill=tk.X)
    barra.pack_propagate(False)

    tk.Label(barra, text=estado_texto, bg="#dde6ed", fg="#003366", 
             font=("Segoe UI", 11, "bold")).pack(side=tk.LEFT, padx=15)

    tk.Button(barra, text="Cancelar", font=("Segoe UI", 10, "bold"), bg="#ffc7ce", 
              fg="#9c0006", command=comando_cancelar).pack(side=tk.RIGHT, padx=10, pady=8)

    tk.Button(barra, text="Guardar Registro", font=("Segoe UI", 10, "bold"), bg="#c6efce", 
              fg="#006100", command=comando_guardar).pack(side=tk.RIGHT, pady=8)

def crear_formulario(ventana, lista_mecanicos_db):
    contenedor = tk.Frame(ventana, bg="#e8eef3")
    contenedor.pack(side=tk.TOP, fill="both", expand=True, padx=40, pady=20)

    entradas = {}
    fuente_label = ("Segoe UI", 10, "bold")

    # ID Tarea
    tk.Label(contenedor, text="ID Tarea:", bg="#e8eef3", font=fuente_label).grid(row=0, column=0, sticky="w", pady=5)
    ent_id = tk.Entry(contenedor, width=15, state="readonly")
    ent_id.grid(row=0, column=1, sticky="w")
    entradas["id_tarea"] = ent_id

    # Fecha
    tk.Label(contenedor, text="Fecha:", bg="#e8eef3", font=fuente_label).grid(row=1, column=0, sticky="w", pady=5)
    ent_fecha = DateEntry(contenedor, width=13, date_pattern="dd-mm-yyyy")
    ent_fecha.grid(row=1, column=1, sticky="w")
    entradas["fecha"] = ent_fecha

    # --- SECCIÓN MECÁNICOS ---
    tk.Label(contenedor, text="Seleccionar Mecánico:", bg="#e8eef3", font=fuente_label).grid(row=2, column=0, sticky="w", pady=5)
    f_mec = tk.Frame(contenedor, bg="#e8eef3")
    f_mec.grid(row=2, column=1, sticky="w")
    cb_mec = ttk.Combobox(f_mec, values=lista_mecanicos_db, state="readonly", width=30)
    cb_mec.pack(side=tk.LEFT)
    
    btn_add_mec = tk.Button(f_mec, text="+", width=3, bg="#c6efce", font=("Arial", 9, "bold"),
                            command=lambda: agregar_al_texto(cb_mec, ent_mec))
    btn_add_mec.pack(side=tk.LEFT, padx=5)
    
    ent_mec = tk.Entry(contenedor, width=50)
    ent_mec.grid(row=3, column=1, sticky="w", pady=(0, 10))
    entradas["mecanicos"] = ent_mec

    # --- SECCIÓN HORARIOS ---
    tk.Label(contenedor, text="Seleccionar Horario:", bg="#e8eef3", font=fuente_label).grid(row=4, column=0, sticky="w", pady=5)
    f_hor = tk.Frame(contenedor, bg="#e8eef3")
    f_hor.grid(row=4, column=1, sticky="w")
    cb_hor = ttk.Combobox(f_hor, values=["6 a 14", "14 a 22", "22 a 6"], state="readonly", width=30)
    cb_hor.pack(side=tk.LEFT)
    
    btn_add_hor = tk.Button(f_hor, text="+", width=3, bg="#c6efce", font=("Arial", 9, "bold"),
                            command=lambda: agregar_al_texto(cb_hor, ent_hor))
    btn_add_hor.pack(side=tk.LEFT, padx=5)
    
    ent_hor = tk.Entry(contenedor, width=50)
    ent_hor.grid(row=5, column=1, sticky="w", pady=(0, 10))
    entradas["horarios"] = ent_hor

    # --- SECCIÓN REPORTE (CON SCROLLBAR) ---
    tk.Label(contenedor, text="Reporte Detallado:", bg="#e8eef3", font=fuente_label).grid(row=6, column=0, sticky="nw", pady=10)
    
    f_texto = tk.Frame(contenedor)
    f_texto.grid(row=6, column=1, sticky="nsew", pady=10)
    
    scroll_y = tk.Scrollbar(f_texto)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    ent_rep = tk.Text(f_texto, width=55, height=15, font=("Segoe UI", 10), 
                      undo=True, wrap="word", yscrollcommand=scroll_y.set)
    ent_rep.pack(side=tk.LEFT, fill="both", expand=True)
    scroll_y.config(command=ent_rep.yview)
    
    entradas["reporte"] = ent_rep

    def agregar_al_texto(combo, entry):
        seleccion = combo.get()
        if seleccion:
            actual = entry.get()
            nuevo = seleccion if not actual else f"{actual}, {seleccion}"
            entry.delete(0, tk.END)
            entry.insert(0, nuevo)

    return entradas