import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

def crear_ventana(parent, titulo):
    ventana = tk.Toplevel(parent)
    ventana.title(titulo)
    ventana.geometry("450x250")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()
    
    if os.path.exists(ICON_PATH):
        try: ventana.iconbitmap(ICON_PATH)
        except: pass
    return ventana

def crear_toolstrip(ventana):
    barra = tk.Frame(ventana, bg="#dde6ed", height=60)
    barra.pack(fill=tk.X)
    barra.pack_propagate(False)
    fuente = ("Segoe UI", 11, "bold")
    
    def crear_boton(texto, x, color_bg="#cfe2f3"):
        b = tk.Button(barra, text=texto, font=fuente, fg="#003366", bg=color_bg,
                      activebackground="#a4c2f4", bd=0, relief="flat")
        b.place(x=x, y=10, width=120, height=40)
        return b

    return {
        "guardar": crear_boton("Guardar", 10, color_bg="#c6efce"),
        "cancelar": crear_boton("Cancelar", 150, color_bg="#ffc7ce")
    }

def crear_formulario(ventana):
    frame = tk.Frame(ventana, bg="#f0f4f8")
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

    tk.Label(frame, text="Nombre de la Planta / Unidad:", bg="#f0f4f8", 
             font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=5)

    entry_nombre = ttk.Entry(frame, width=40)
    entry_nombre.pack(fill=tk.X, pady=5)
    entry_nombre.focus_set()

    return {"nombre": entry_nombre}