import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import os
import tempfile
from principalvista import BASE_DIR

ICON_PATH = os.path.join(BASE_DIR, "iconom.ico")

class OTGraficosVista:
    def __init__(self, parent):
        self.controlador = None
        self.ventana = tk.Toplevel(parent)
        self.ventana.title("Gráficos de Gestión de Mantenimiento")
        self.ventana.state("zoomed")
        try: self.ventana.iconbitmap(ICON_PATH)
        except: pass
            
        self._crear_toolstrip()
        self._crear_filtros()
        self._crear_grafico()

    def set_controlador(self, controlador):
        self.controlador = controlador

    def _crear_toolstrip(self):
        ts = tk.Frame(self.ventana, bg="#dde6ed")
        ts.pack(fill=tk.X)
        fnt = ("Segoe UI", 11, "bold")
        def btn(txt, cmd): return tk.Button(ts, text=txt, font=fnt, fg="#003366", bg="#cfe2f3", bd=0, padx=15, pady=8, command=cmd)

        btn("Volver", self.ventana.destroy).pack(side=tk.LEFT, padx=10, pady=5)
        btn("Resumen Mensual", lambda: self.controlador.cambiar_modo("mensual")).pack(side=tk.LEFT, padx=5)
        btn("Evolución Anual", lambda: self.controlador.cambiar_modo("anual")).pack(side=tk.LEFT, padx=5)
        btn("Generar Presentación", lambda: self.controlador.generar_presentacion()).pack(side=tk.LEFT, padx=10, pady=5)

    def _crear_filtros(self):
        f = tk.Frame(self.ventana)
        f.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(f, text="Mes:").pack(side=tk.LEFT, padx=2)
        self.combo_mes = ttk.Combobox(f, width=6, state="readonly")
        self.combo_mes.pack(side=tk.LEFT, padx=5)

        tk.Label(f, text="Año:").pack(side=tk.LEFT, padx=2)
        self.combo_anio = ttk.Combobox(f, width=6, state="readonly")
        self.combo_anio.pack(side=tk.LEFT, padx=5)

        tk.Label(f, text="Planta:").pack(side=tk.LEFT, padx=2)
        self.combo_planta = ttk.Combobox(f, width=15, state="readonly")
        self.combo_planta.pack(side=tk.LEFT, padx=5)

        tk.Label(f, text="Línea:").pack(side=tk.LEFT, padx=2)
        self.combo_linea = ttk.Combobox(f, width=15, state="readonly")
        self.combo_linea.pack(side=tk.LEFT, padx=5)

        tk.Label(f, text="Tipo de OT:").pack(side=tk.LEFT, padx=2)
        self.combo_tipo = ttk.Combobox(f, width=22, state="readonly")
        self.combo_tipo.pack(side=tk.LEFT, padx=5)

    def guardar_grafico_temp(self):
        """Guarda la figura actual en un archivo temporal de imagen PNG"""
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "temp_grafico_ot.png")
        self.figura.savefig(file_path, format="png", dpi=300, bbox_inches='tight')
        return file_path

    def _crear_grafico(self):
        self.frame_grafico = tk.Frame(self.ventana, bg="white")
        self.frame_grafico.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.figura = Figure(figsize=(10, 6), dpi=100)
        self.ax = self.figura.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figura, master=self.frame_grafico)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _poner_valores(self, barras):
        alturas = [b.get_height() for b in barras]
        max_h = max(alturas) if alturas else 1
        for b in barras:
            h = b.get_height()
            self.ax.text(b.get_x() + b.get_width()/2, h + (max_h * 0.02), 
                         f"{int(h)}", ha="center", va="bottom", 
                         fontsize=10, fontweight="bold")

    def _estilizar_ejes(self, titulo_principal, sub_info):
        self.ax.set_title(f"{titulo_principal}\n{sub_info}", fontsize=14, fontweight="bold", pad=5)
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.grid(axis="y", linestyle="--", alpha=0.3)

    def mostrar_grafico_resumen(self, datos):
        self.ax.clear()
        etiquetas = ["Generadas", "Cerradas", "Pendientes"]
        valores = [datos.get("generadas", 0), datos.get("cerradas", 0), datos.get("pendientes", 0)]
        planta = datos.get("nombre_planta", "")
        
        colores = ["#3498db", "#2ecc71", "#e67e22"]
        barras = self.ax.bar(etiquetas, valores, width=0.6, color=colores)
        
        for barra, etiqueta in zip(barras, etiquetas):
            barra.set_label(etiqueta)
            
        self._poner_valores(barras)
        self._estilizar_ejes(f"Resumen mensual planta {planta}", f"porcentaje de Cierre: {datos.get('porcentaje_cierre', 0)}%")
        
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)
        self.ax.set_ylim(0, max(valores + [5]) * 1.15) 
        self.figura.tight_layout(rect=[0, 0.08, 1, 0.95]) 
        self.canvas.draw()

    def mostrar_grafico_anual(self, datos):
        self.ax.clear()
        meses = datos["meses"]
        x = np.arange(len(meses))
        w = 0.25
        planta = datos.get("nombre_planta", "")
        
        b1 = self.ax.bar(x - w, datos["generadas"], w, label="Generadas", color="#3498db")
        b2 = self.ax.bar(x, datos["cerradas"], w, label="Cerradas", color="#2ecc71")
        b3 = self.ax.bar(x + w, datos["pendientes"], w, label="Pendientes", color="#e67e22")
        
        self._poner_valores(b1); self._poner_valores(b2); self._poner_valores(b3)
        self._estilizar_ejes(f"Resumen anual planta {planta}", f"Porcentaje de cierre: {datos.get('porcentaje_anual', 0)}%")
        
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(meses)
        self.ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=3, frameon=False)
        
        max_v = max(max(datos["generadas"]), 1)
        self.ax.set_ylim(0, max_v * 1.20)
        self.figura.tight_layout(rect=[0, 0.05, 1, 0.95])
        self.canvas.draw()
    def exportar_grafico_a_imagen(self, tipo, datos, filepath):
        """Genera y guarda una imagen en resolución 16:9 apta para PowerPoint sin alterar la GUI."""
        # Figura 16:9 pura (13.33 x 7.5 pulgadas)
        fig = Figure(figsize=(13.333, 7.5), dpi=300)
        ax = fig.add_subplot(111)

        if tipo == "mensual":
            etiquetas = ["Generadas", "Cerradas", "Pendientes"]
            valores = [datos.get("generadas", 0), datos.get("cerradas", 0), datos.get("pendientes", 0)]
            planta = datos.get("nombre_planta", "")
            colores = ["#3498db", "#2ecc71", "#e67e22"]
            
            barras = ax.bar(etiquetas, valores, width=0.5, color=colores)
            
            # Poner etiquetas de valor sobre las barras
            max_h = max(valores) if valores else 1
            for b in barras:
                h = b.get_height()
                ax.text(b.get_x() + b.get_width()/2, h + (max_h * 0.02), 
                        f"{int(h)}", ha="center", va="bottom", fontsize=12, fontweight="bold")
            
            ax.set_title(f"Resumen mensual planta {planta}\nPorcentaje de Cierre: {datos.get('porcentaje_cierre', 0)}%", 
                         fontsize=16, fontweight="bold", pad=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            ax.set_ylim(0, max(valores + [5]) * 1.15)
            fig.tight_layout(rect=[0, 0.05, 1, 0.95])

        elif tipo == "anual":
            meses = datos["meses"]
            x = np.arange(len(meses))
            w = 0.25
            planta = datos.get("nombre_planta", "")

            b1 = ax.bar(x - w, datos["generadas"], w, label="Generadas", color="#3498db")
            b2 = ax.bar(x, datos["cerradas"], w, label="Cerradas", color="#2ecc71")
            b3 = ax.bar(x + w, datos["pendientes"], w, label="Pendientes", color="#e67e22")

            # Poner valores sobre barras
            todas_alturas = datos["generadas"] + datos["cerradas"] + datos["pendientes"]
            max_h = max(todas_alturas) if todas_alturas else 1
            for grupo in (b1, b2, b3):
                for b in grupo:
                    h = b.get_height()
                    ax.text(b.get_x() + b.get_width()/2, h + (max_h * 0.02), 
                            f"{int(h)}", ha="center", va="bottom", fontsize=9, fontweight="bold")

            ax.set_title(f"Resumen anual planta {planta}\nPorcentaje de Cierre: {datos.get('porcentaje_anual', 0)}%", 
                         fontsize=16, fontweight="bold", pad=10)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(axis="y", linestyle="--", alpha=0.3)
            ax.set_xticks(x)
            ax.set_xticklabels(meses)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=False)
            ax.set_ylim(0, max_h * 1.20)
            fig.tight_layout(rect=[0, 0.08, 1, 0.95])

        fig.savefig(filepath, format="png", dpi=300, bbox_inches='tight')