import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from principalvista import BASE_DIR
import os

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")


# ============================================================
# VENTANA
# ============================================================
def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Parte Diario")
    ventana.geometry("800x600")
    ventana.configure(bg="#e8eef3")
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
def crear_toolstrip(ventana, estado_texto, comando_guardar, comando_cancelar):
    barra = tk.Frame(ventana, bg="#dde6ed", height=55)
    barra.pack(fill=tk.X)
    barra.pack_propagate(False)

    tk.Label(
        barra,
        text=estado_texto,
        bg="#dde6ed",
        fg="#003366",
        font=("Segoe UI", 11, "bold")
    ).pack(side=tk.LEFT, padx=15)

    tk.Button(
        barra,
        text="Cancelar",
        font=("Segoe UI", 10, "bold"),
        bg="#ffc7ce",
        fg="#9c0006",
        command=comando_cancelar
    ).pack(side=tk.RIGHT, pady=8)

    tk.Button(
        barra,
        text="Guardar",
        font=("Segoe UI", 10, "bold"),
        bg="#c6efce",
        fg="#006100",
        command=comando_guardar
    ).pack(side=tk.RIGHT, padx=10, pady=8)


# ============================================================
# FORMULARIO
# ============================================================
def crear_formulario(ventana):
    contenedor = tk.Frame(ventana, bg="#e8eef3")
    contenedor.pack(fill="both", expand=True, padx=20, pady=20)

    entradas = {}

    campos = [
        "ID",
        "Fecha",
        "Nombre",
        "Turno",
        "Codigo maquina",
        "Reporte"
    ]

    fila = 0
    for campo in campos:
        tk.Label(
            contenedor,
            text=f"{campo}:",
            bg="#e8eef3",
            font=("Segoe UI", 10)
        ).grid(row=fila, column=0, sticky="w", pady=6)

        # =========================
        # WIDGETS
        # =========================
        if campo == "Fecha":
            widget = DateEntry(
                contenedor,
                width=37,
                date_pattern="dd/mm/yyyy"
            )

        elif campo == "Reporte":
            widget = tk.Text(
                contenedor,
                width=45,
                height=6
            )

        else:
            widget = tk.Entry(
                contenedor,
                width=40
            )

        widget.grid(row=fila, column=1, pady=6)

        # ID SOLO LECTURA
        if campo == "ID":
            widget.configure(state="readonly")

        entradas[campo] = widget
        fila += 1

    return entradas
