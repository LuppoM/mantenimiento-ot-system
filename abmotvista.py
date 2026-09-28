import os
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")


# =========================
# VENTANA ADAPTABLE
# =========================
def crear_ventana(parent):
    ventana = tk.Toplevel(parent)
    ventana.title("Orden de Trabajo")

    # Tamaño inicial seguro para pantallas de baja resolución (1024x768 / laptops)
    ventana.geometry("1100x720")
    ventana.minsize(800, 500)

    # Maximizar automáticamente según la resolución de la pantalla del usuario
    try:
        ventana.state("zoomed")  # En Windows abre la ventana maximizada
    except Exception:
        pass

    ventana.configure(bg="#e8eef3")
    ventana.transient(parent)
    ventana.grab_set()

    if os.path.exists(ICON_PATH):
        try:
            ventana.iconbitmap(ICON_PATH)
        except Exception:
            pass

    return ventana


# =========================
# TOOLSTRIP
# =========================
def crear_toolstrip(ventana, estado_texto, comando_guardar, comando_cancelar):
    barra = tk.Frame(ventana, bg="#dde6ed", height=55)
    barra.pack(fill=tk.X, side=tk.TOP)
    barra.pack_propagate(False)

    tk.Label(
        barra,
        text=estado_texto,
        bg="#dde6ed",
        fg="#003366",
        font=("Segoe UI", 11, "bold"),
    ).pack(side=tk.LEFT, padx=15)

    tk.Button(
        barra,
        text="Cancelar",
        font=("Segoe UI", 10, "bold"),
        bg="#ffc7ce",
        fg="#9c0006",
        command=comando_cancelar,
    ).pack(side=tk.RIGHT, padx=10, pady=8)

    tk.Button(
        barra,
        text="Guardar",
        font=("Segoe UI", 10, "bold"),
        bg="#c6efce",
        fg="#006100",
        command=comando_guardar,
    ).pack(side=tk.RIGHT, padx=5, pady=8)


# =========================
# FORMULARIO CON SCROLL INTEGRADO
# =========================
def crear_formulario(ventana):

    # --- Contenedor Principal con Scrollbar para Monitores de Poca Altura ---
    contenedor_scroll = tk.Frame(ventana, bg="#e8eef3")
    contenedor_scroll.pack(fill="both", expand=True)

    canvas = tk.Canvas(contenedor_scroll, bg="#e8eef3", highlightthickness=0)
    v_scrollbar = ttk.Scrollbar(
        contenedor_scroll, orient="vertical", command=canvas.yview
    )
    h_scrollbar = ttk.Scrollbar(
        contenedor_scroll, orient="horizontal", command=canvas.xview
    )

    contenedor = tk.Frame(canvas, bg="#e8eef3")

    def _actualizar_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    contenedor.bind("<Configure>", _actualizar_scroll)

    window_id = canvas.create_window((0, 0), window=contenedor, anchor="nw")

    # Permite expandir el contenedor si el monitor es muy ancho
    def _al_resizear_canvas(event):
        if event.width > contenedor.winfo_reqwidth():
            canvas.itemconfig(window_id, width=event.width)

    canvas.bind("<Configure>", _al_resizear_canvas)

    canvas.configure(
        xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set
    )

    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    # Soporte para desplazar la pantalla usando la rueda del mouse (MouseWheel)
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # --- Marcos de Trabajo ---
    frm_pre = tk.LabelFrame(
        contenedor,
        text="Pre Resolución",
        bg="#e8eef3",
        font=("Segoe UI", 11, "bold"),
        padx=10,
        pady=10,
    )
    frm_pre.pack(
        side="left", fill="both", expand=True, padx=15, pady=15, anchor="n"
    )

    frm_post = tk.LabelFrame(
        contenedor,
        text="Post Resolución / Cierre",
        bg="#e8eef3",
        font=("Segoe UI", 11, "bold"),
        padx=10,
        pady=10,
    )
    frm_post.pack(
        side="left", fill="both", expand=True, padx=15, pady=15, anchor="n"
    )

    entradas = {}

    # =========================
    # PRE (Mantiene tu orden intacto)
    # =========================
    campos_pre = [
        "ID",
        "Codigo",
        "Version",
        "Mantenimiento correctivo",
        "Fecha",
        "Planta",
        "Sector",
        "Parte",
        "Nave",
        "Equipo",
        "Elemento",
        "Nombre del solicitante",
        "Area",
        "Descripcion del defecto",
        "Observaciones",
        "Prioridad",
        "Realizada",
    ]

    areas = [
        "Producción",
        "Calidad",
        "Depósito y Logística",
        "Seguridad",
        "Mantenimiento",
        "Otros",
    ]

    fila = 0
    for campo in campos_pre:

        tk.Label(
            frm_pre,
            text=f"{campo}:",
            bg="#e8eef3",
            font=("Segoe UI", 10),
        ).grid(row=fila, column=0, sticky="w", pady=3)

        if campo in ("Descripcion del defecto", "Observaciones"):
            widget = tk.Text(frm_pre, width=38, height=3)

        elif campo == "Fecha":
            widget = DateEntry(frm_pre, width=35, date_pattern="dd/mm/yyyy")

        elif campo == "Mantenimiento correctivo":
            widget = ttk.Combobox(
                frm_pre,
                values=[
                    "Correctivo inmediato",
                    "Correctivo diferido",
                    "Mejora",
                ],
                state="readonly",
                width=35,
            )

        elif campo == "Area":
            widget = ttk.Combobox(
                frm_pre, values=areas, state="readonly", width=35
            )

        elif campo in ("Planta", "Sector"):
            widget = ttk.Combobox(frm_pre, state="readonly", width=35)

        elif campo == "Prioridad":
            widget = ttk.Combobox(
                frm_pre,
                values=["BAJA", "MEDIA", "ALTA", "CRITICA"],
                state="readonly",
                width=35,
            )

        elif campo == "Realizada":
            widget = ttk.Combobox(
                frm_pre, values=["NO", "SI"], state="readonly", width=35
            )

        else:
            widget = tk.Entry(frm_pre, width=38)

        widget.grid(row=fila, column=1, pady=3, padx=5)
        entradas[campo] = widget
        fila += 1

    # =========================
    # POST (Mantiene tu orden intacto)
    # =========================
    campos_post = [
        "Solucion",
        "Fecha cierre ot",
        "Descripcion solucion",
        "Material utilizado",
        "NombreRealizo",
        "Aprobo solicitante",
        "Aprobo mant",
        "Aprobo calidad",
    ]

    soluciones = [
        "Mantenimiento mecánico",
        "Mantenimiento eléctrico",
        "Mantenimiento electrónico",
        "Mantenimiento edilicio",
        "Otro",
    ]

    fila = 0
    for campo in campos_post:

        tk.Label(
            frm_post,
            text=f"{campo}:",
            bg="#e8eef3",
            font=("Segoe UI", 10),
        ).grid(row=fila, column=0, sticky="w", pady=3)

        if campo == "Solucion":
            widget = ttk.Combobox(
                frm_post, values=soluciones, state="readonly", width=35
            )

        elif campo == "Descripcion solucion":
            widget = tk.Text(frm_post, width=38, height=3)

        elif campo.startswith("Aprobo"):
            widget = ttk.Combobox(
                frm_post, values=["NO", "SI"], state="readonly", width=35
            )

        elif campo == "Fecha cierre ot":
            widget = DateEntry(frm_post, width=35, date_pattern="dd/mm/yyyy")

        elif campo == "NombreRealizo":
            widget = ttk.Combobox(frm_post, state="readonly", width=35)

        else:
            widget = tk.Entry(frm_post, width=38)

        widget.grid(row=fila, column=1, pady=3, padx=5)
        widget.configure(state="disabled")

        entradas[campo] = widget
        fila += 1

    return entradas


# =========================
# HABILITADORES DE LOS CAMPOS POST
# =========================
def habilitar_campos(campos, lista_campos):
    for campo in lista_campos:
        widget = campos.get(campo)
        if widget:
            widget.configure(state="normal")


def deshabilitar_campos(campos, lista_campos):
    for campo in lista_campos:
        widget = campos.get(campo)
        if widget:
            widget.configure(state="disabled")


def limpiar_campos(campos, lista_campos):
    for campo in lista_campos:
        widget = campos.get(campo)
        if not widget:
            continue

        try:
            if isinstance(widget, tk.Text):
                widget.delete("1.0", "end")
            elif isinstance(widget, DateEntry):
                widget.delete(0, "end")
            elif hasattr(widget, "delete"):
                estado_previo = widget.cget("state")
                if estado_previo == "readonly":
                    widget.configure(state="normal")
                    widget.delete(0, "end")
                    widget.configure(state="readonly")
                else:
                    widget.delete(0, "end")
            elif hasattr(widget, "set"):
                widget.set("")
        except Exception:
            pass