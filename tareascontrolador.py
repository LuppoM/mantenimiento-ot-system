import os
from tkinter import messagebox, simpledialog
from tareaspdf import TareasPDFService
import tareasvista as vista
from tareasmodelo import (
    obtener_todas_las_tareas, 
    filtrar_tareas, 
    eliminar_tarea, 
    obtener_tarea_por_id
)
from abmtareascontrolador import iniciar_abmtareas

# Clave de seguridad para acciones críticas
CLAVE_ELIMINAR_TAREA = "Mario456"

def iniciar(parent, conexion):
    ventana = vista.crear_ventana(parent)
    c_col, e_txt = None, None
    # Mantiene el registro de las columnas para el mapeo del PDF
    columnas_actuales = []

    def refrescar_interfaz(columnas, datos):
        nonlocal columnas_actuales
        columnas_actuales = columnas
        
        # Primero vaciamos completamente las filas actuales
        tree.delete(*tree.get_children())
        tree["columns"] = columnas
        
        for col in columnas:
            tree.heading(col, text=col.upper())
            # Configuración de anchos según el tipo de columna
            if col.lower() in ["id_tarea", "fecha"]:
                tree.column(col, width=100, anchor="center", stretch=False)
            elif "reporte" in col.lower():
                tree.column(col, width=450, anchor="w", stretch=True) 
            else:
                tree.column(col, width=200, anchor="center", stretch=True)
        
        # CORREGIDO: Limpieza de saltos de línea al insertar para evitar superposición
        for fila in datos:
            fila_limpia = []
            for celda in fila:
                if celda is not None:
                    # Reemplaza saltos de línea por un separador visual limpio
                    texto_limpio = str(celda).replace("\n", "  —  ")
                    fila_limpia.append(texto_limpio)
                else:
                    fila_limpia.append("")
                    
            tree.insert("", "end", values=fila_limpia)
        
        # Configuración inicial del combo de filtro
        if columnas and c_col and not c_col.get():
            c_col["values"] = columnas
            c_col.current(1) 

    def cargar_todo():
        cols, datos = obtener_todas_las_tareas(conexion)
        refrescar_interfaz(cols, datos)

    def ejecutar_filtro(columna, valor):
        if not valor.strip():
            cargar_todo()
        else:
            cols, datos = filtrar_tareas(conexion, columna, valor)
            refrescar_interfaz(cols, datos)

    def obtener_id():
        sel = tree.focus()
        return tree.item(sel, "values")[0] if sel else None

    # --- Acciones del Toolstrip ---

    def agregar():
        if iniciar_abmtareas(ventana, conexion, "AGREGAR"):
            cargar_todo()

    def modificar():
        id_t = obtener_id()
        if not id_t:
            messagebox.showwarning("Atención", "Seleccione una tarea de la lista")
            return
        datos = obtener_tarea_por_id(conexion, id_t)
        if iniciar_abmtareas(ventana, conexion, "MODIFICAR", datos):
            cargar_todo()

    def eliminar():
        id_t = obtener_id()
        if not id_t: return
        
        pw = simpledialog.askstring("Seguridad", "Ingrese clave para eliminar:", show="*", parent=ventana)
        if pw == CLAVE_ELIMINAR_TAREA:
            if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la tarea ID {id_t}?"):
                if eliminar_tarea(conexion, id_t):
                    cargar_todo()
        elif pw is not None:
            messagebox.showerror("Error", "Clave incorrecta")

    def imprimir():
        """
        Imprime exclusivamente la fila seleccionada.
        Genera un PDF con el diseño de bloque (ID, Fecha, Mecánicos, Horario, Reporte).
        """
        seleccion = tree.selection()
        
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una fila de la tabla para imprimir el informe.")
            return

        # 1. Extraer datos de la fila seleccionada
        item = seleccion[0]
        valores = tree.item(item, "values")
        
        # Mapeamos los valores a un diccionario usando los nombres de las columnas
        tarea_dict = dict(zip(columnas_actuales, valores))
        lista_para_pdf = [tarea_dict] # El servicio requiere una lista

        try:
            # 2. Instanciar servicio y generar el PDF
            pdf_service = TareasPDFService()
            
            # Usamos el ID de la tarea para el nombre del archivo
            id_t = tarea_dict.get('id_tarea', 'Indiv')
            ruta = pdf_service.generar_informe_diario(lista_para_pdf, f"Tarea_ID_{id_t}")
            
            # 3. Abrir el documento automáticamente
            os.startfile(ruta)
            
        except Exception as e:
            messagebox.showerror("Error de Impresión", f"No se pudo generar el PDF: {e}")

    # --- Construcción de la Interfaz ---
    # Vinculamos las funciones a los botones de la vista
    vista.crear_toolstrip(ventana, agregar, modificar, eliminar, imprimir)
    
    # Filtros y Tabla
    c_col, e_txt = vista.crear_filtro(ventana, ejecutar_filtro)
    tree = vista.crear_tabla(ventana, filas_visibles=18)

    # Carga inicial de datos
    cargar_todo()
    
    # Mantener la ventana enfocada
    parent.wait_window(ventana)