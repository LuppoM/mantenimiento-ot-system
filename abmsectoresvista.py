import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")


# ------------------------------------------------------------
# VENTANA ABM SECTORES
# ------------------------------------------------------------
def crear_ventana(parent, titulo):
    ventana = tk.Toplevel(parent)
    ventana.title(titulo)
    ventana.geometry("600x350")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()

    if os.path.exists(ICON_PATH):
        try:
            ventana.iconbitmap(ICON_PATH)
        except:
            pass

    return ventana


# ------------------------------------------------------------
# TOOLSTRIP
# ------------------------------------------------------------
def crear_toolstrip(ventana):
    barra = tk.Frame(ventana, bg="#dde6ed", height=60)
    barra.pack(fill=tk.X)
    barra.pack_propagate(False)

    fuente = ("Segoe UI", 11, "bold")
    fg = "#003366"
    bg = "#cfe2f3"
    hover = "#a4c2f4"

    def boton(texto, x):
        b = tk.Button(
            barra,
            text=texto,
            font=fuente,
            fg=fg,
            bg=bg,
            activebackground=hover,
            activeforeground=fg,
            bd=0,
            relief="flat"
        )
        b.place(x=x, y=10, width=120, height=40)
        return b

    btn_guardar = boton("Guardar", 10)
    btn_cancelar = boton("Cancelar", 150)

    return {
        "guardar": btn_guardar,
        "cancelar": btn_cancelar
    }


# ------------------------------------------------------------
# FORMULARIO
# ------------------------------------------------------------
def crear_formulario(ventana):
    frame = tk.Frame(ventana, bg="#f0f4f8")
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # ---- Sector ----
    tk.Label(
        frame,
        text="Sector:",
        bg="#f0f4f8",
        font=("Segoe UI", 11, "bold")
    ).grid(row=0, column=0, sticky="w", pady=10)

    entry_nombre = ttk.Entry(frame, width=40)
    entry_nombre.grid(row=0, column=1, pady=10)

    # ---- Planta ----
    tk.Label(
        frame,
        text="Planta:",
        bg="#f0f4f8",
        font=("Segoe UI", 11, "bold")
    ).grid(row=1, column=0, sticky="w", pady=10)

    combo_planta = ttk.Combobox(
        frame,
        values=["Chocolate", "Golosinas"],
        state="readonly",
        width=38
    )
    combo_planta.grid(row=1, column=1, pady=10)
    combo_planta.current(0)

    return {
        "nombre": entry_nombre,
        "planta": combo_planta
    }
