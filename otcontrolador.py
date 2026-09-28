from tkinter import messagebox, simpledialog
import otvista as vista
from otmodelo import obtener_todas_las_ot, filtrar_ot_por_texto, eliminar_ot, obtener_ot_por_id
from abmotcontrolador import iniciar_abmot
from pdfservice import PDFService
from otimpresionmodelo import OTImpresionModelo
from otimpresioncontrolador import OTImpresionControlador
from otgraficos import abrir_graficos
from otrepositorio import RepositorioOT

CLAVE_ELIMINAR_OT = "Mario456"

def iniciar_ot(parent, conexion):
    ventana = vista.crear_ventana_ot(parent)
    c_col, e_txt = None, None

    def refrescar_interfaz(columnas, datos):
        tree.delete(*tree.get_children())
        tree["columns"] = columnas
        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center", stretch=False)
        
        for fila in datos:
            tree.insert("", "end", values=fila)
        
        if columnas and c_col and not c_col.get():
            c_col["values"] = columnas
            c_col.current(0)

    def cargar_todo():
        cols, datos = obtener_todas_las_ot(conexion)
        refrescar_interfaz(cols, datos)

    def ejecutar_filtro(columna, valor):
        if not valor.strip():
            cargar_todo()
        else:
            cols, datos = filtrar_ot_por_texto(conexion, columna, valor)
            refrescar_interfaz(cols, datos)

    # --- Acciones ---
    def obtener_id():
        sel = tree.focus()
        return tree.item(sel, "values")[0] if sel else None

    def agregar():
        if iniciar_abmot(ventana, conexion, "AGREGAR"):
            cargar_todo()

    def modificar():
        id_ot = obtener_id()
        if not id_ot: return
        datos = obtener_ot_por_id(conexion, id_ot)
        if iniciar_abmot(ventana, conexion, "MODIFICAR", datos):
            cargar_todo()

    def eliminar():
        id_ot = obtener_id()
        if not id_ot: return
        pw = simpledialog.askstring("Seguridad", "Clave:", show="*", parent=ventana)
        if pw == CLAVE_ELIMINAR_OT:
            if messagebox.askyesno("Eliminar", f"¿Eliminar OT {id_ot}?"):
                if eliminar_ot(conexion, id_ot): cargar_todo()

    def imprimir():
        id_ot = obtener_id()
        if not id_ot: return
        datos = obtener_ot_por_id(conexion, id_ot)
        if datos:
            try:
                ctrl = OTImpresionControlador(OTImpresionModelo(datos), PDFService(), None)
                ctrl.generar_y_abrir()
            except Exception as e: messagebox.showerror("Error", str(e))

    # --- Armado de UI ---
    vista.crear_toolstrip(ventana, agregar, modificar, eliminar, imprimir, 
                          lambda: abrir_graficos(ventana, RepositorioOT(conexion)))

    c_col, e_txt = vista.crear_filtro(ventana, ejecutar_filtro)
    
    tree = vista.crear_tabla(ventana, filas_visibles=18)

    cargar_todo()
    parent.wait_window(ventana)