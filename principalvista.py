import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")
FONDO_PATH = os.path.join(BASE_DIR, "fondo.jpg")

def crear_ventana_principal():
    root = tk.Tk()
    root.title("Gestión de Mantenimiento")
    root.state("zoomed")
    root.configure(bg="#f0f4f8")

    # Icono
    if os.path.exists(ICON_PATH):
        try:
            root.iconbitmap(ICON_PATH)
        except Exception:
            pass

    # Lógica de Fondo Optimizada
    if os.path.exists(FONDO_PATH):
        try:
            img_original = Image.open(FONDO_PATH)
            fondo_label = tk.Label(root)
            fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)

            def actualizar_fondo(event=None):
                ancho = root.winfo_width()
                alto = root.winfo_height()
                
                if ancho > 100 and alto > 100:
                    img_reseteada = img_original.resize((ancho, alto), Image.Resampling.NEAREST)
                    root.photo_fondo = ImageTk.PhotoImage(img_reseteada)
                    fondo_label.config(image=root.photo_fondo)

            root.bind("<Configure>", actualizar_fondo)
        except Exception as e:
            print(f"Error al cargar fondo: {e}")

    return root

def configurar_estilos(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Botones principales
    style.configure(
        "TButton",
        font=("Segoe UI", 14, "bold"),
        padding=15,
        foreground="#004080",
        background="#cce6ff"
    )

    style.map(
        "TButton",
        foreground=[("active", "#00264d")],
        background=[("active", "#99ccff")]
    )

    # Etiquetas
    style.configure(
        "TLabel",
        font=("Segoe UI", 18, "bold"),
        foreground="#003366",
        background="#f0f4f8"
    )

def crear_botones(root, botones, abrir_sectores=None, abrir_mecanicos=None, abrir_plantas=None, abrir_notas_pedido=None):
    # Frame superior con transparencia visual (gris suave)
    button_frame = tk.Frame(root, bg="#999a9c", height=70)
    button_frame.pack(side="top", fill="x")

    # Crear botones dinámicamente (OT, Tareas, Parte Diario, Notas de Pedido, etc.)
    for i, (texto, comando) in enumerate(botones[:-1]):
        btn = ttk.Button(button_frame, text=texto, command=comando)
        btn.grid(row=0, column=i, padx=15, pady=10, sticky="nsew")
        button_frame.columnconfigure(i, weight=1)

    # Menú de Parámetros (Agrupación de configuraciones)
    col_params = len(botones) - 1
    menu_btn = tk.Menubutton(
        button_frame, 
        text="Parámetros",
        font=("Segoe UI", 14, "bold"),
        bg="#cce6ff",
        fg="#004080",
        relief="raised",
        padx=15,
        pady=10
    )
    menu_btn.grid(row=0, column=col_params, padx=15, pady=10, sticky="nsew")
    button_frame.columnconfigure(col_params, weight=1)

    menu = tk.Menu(menu_btn, tearoff=0)
    if abrir_mecanicos:
        menu.add_command(label="Mecánicos", command=abrir_mecanicos)
    if abrir_sectores:
        menu.add_command(label="Sectores", command=abrir_sectores)
    if abrir_plantas:
        menu.add_command(label="Plantas", command=abrir_plantas)
    
    menu_btn.config(menu=menu)

    # Botón Salir
    texto_salir, comando_salir = botones[-1]
    btn_salir = ttk.Button(button_frame, text=texto_salir, command=comando_salir)
    btn_salir.grid(row=0, column=col_params + 1, padx=15, pady=10, sticky="nsew")
    button_frame.columnconfigure(col_params + 1, weight=1)

    return button_frame