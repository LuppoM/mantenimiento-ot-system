import os
import tkinter as tk
from tkinter import ttk
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")


def crear_ventana(parent, titulo):
    ventana = tk.Toplevel(parent)
    ventana.title(titulo)
    ventana.geometry("500x250")
    ventana.configure(bg="#f0f4f8")
    ventana.transient(parent)
    ventana.grab_set()

    if os.path.exists(ICON_PATH):
        try:
            ventana.iconbitmap(ICON_PATH)
        except:
            pass

    return ventana


def crear_toolstrip(ventana):
    barra = tk.Frame(ventana, bg="#dde6ed", height=60)
    barra.pack(fill=tk.X)
    barra.pack_propagate(False)

    def boton(texto, x):
        b = tk.Button(
            barra,
            text=texto,
            font=("Segoe UI", 11, "bold"),
            bg="#cfe2f3",
            bd=0,
            relief="flat"
        )
        b.place(x=x, y=10, width=120, height=40)
        return b

    return {
        "guardar": boton("Guardar", 10),
        "cancelar": boton("Cancelar", 150)
    }


def crear_formulario(ventana):
    frame = tk.Frame(ventana, bg="#f0f4f8")
    frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    tk.Label(
        frame,
        text="Mecánico:",
        bg="#f0f4f8",
        font=("Segoe UI", 11, "bold")
    ).grid(row=0, column=0, sticky="w", pady=10)

    entry_nombre = ttk.Entry(frame, width=40)
    entry_nombre.grid(row=0, column=1, pady=10)

    return {"nombre": entry_nombre}
