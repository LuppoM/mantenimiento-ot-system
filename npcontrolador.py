from tkinter import messagebox, simpledialog
import npvista as vista
from npmodelo import (
    obtener_todas_las_np,
    filtrar_np_por_texto,
    obtener_detalle_por_nota,
    obtener_nota_por_id,
    eliminar_np
)
from abmnpcontrolador import iniciar_abmnp
from npimpresionmodelo import NPImpresionModelo
from npimpresioncontrolador import NPImpresionControlador
from notapedidopapel import NotaPedidoPapel

CLAVE_ELIMINAR_NOTA = "Mario456"

def iniciar_notas_pedido(parent, conexion, id_ot=None):
    ventana = vista.crear_ventana_np(parent)
    c_col, e_txt = None, None

    def refrescar_cabecera(columnas, datos):
        tree_cabecera.delete(*tree_cabecera.get_children())
        tree_detalle.delete(*tree_detalle.get_children())
        
        for fila in datos:
            tree_cabecera.insert("", "end", values=fila)
        
        if columnas and c_col and not c_col.get():
            c_col["values"] = columnas
            c_col.current(0)

    def refrescar_detalle(datos):
        tree_detalle.delete(*tree_detalle.get_children())
        
        for fila in datos:
            if isinstance(fila, (list, tuple)):
                if len(fila) == 6:
                    # Estructura SQL: id_detalle (0), id_nota (1), num_item (2), cantidad (3), detalle (4), destino_equipo (5)
                    id_det, id_n, num_item, cantidad, detalle, destino = fila
                    valores_visibles = (num_item, cantidad, detalle, destino)
                elif len(fila) == 4:
                    valores_visibles = fila
                else:
                    valores_visibles = fila
                
                tree_detalle.insert("", "end", values=valores_visibles)

            elif isinstance(fila, dict):
                valores_visibles = (
                    fila.get("num_item", ""),
                    fila.get("cantidad", ""),
                    fila.get("detalle", ""),
                    fila.get("destino_equipo", "")
                )
                tree_detalle.insert("", "end", values=valores_visibles)

    def cargar_todo():
        cols, datos = obtener_todas_las_np(conexion)
        refrescar_cabecera(cols, datos)

    def ejecutar_filtro(columna, valor):
        if not valor.strip():
            cargar_todo()
        else:
            cols, datos = filtrar_np_por_texto(conexion, columna, valor)
            refrescar_cabecera(cols, datos)

    def al_seleccionar_cabecera(event):
        sel = tree_cabecera.focus()
        if not sel: return
        id_nota = tree_cabecera.item(sel, "values")[0]
        _, datos_det = obtener_detalle_por_nota(conexion, id_nota)
        refrescar_detalle(datos_det)

    def obtener_id():
        sel = tree_cabecera.focus()
        return tree_cabecera.item(sel, "values")[0] if sel else None

    def agregar():
        if iniciar_abmnp(ventana, conexion, "AGREGAR", id_ot_asociada=id_ot):
            cargar_todo()

    def modificar():
        id_nota = obtener_id()
        if not id_nota: return
        datos_completos = obtener_nota_por_id(conexion, id_nota)
        if iniciar_abmnp(ventana, conexion, "MODIFICAR", datos_nota=datos_completos):
            cargar_todo()

    def eliminar():
        id_nota = obtener_id()
        if not id_nota: return
        pw = simpledialog.askstring("Seguridad", "Clave:", show="*", parent=ventana)
        if pw == CLAVE_ELIMINAR_NOTA:
            if messagebox.askyesno("Eliminar", f"¿Eliminar Nota de Pedido N° {id_nota}?"):
                if eliminar_np(conexion, id_nota): 
                    cargar_todo()

    def imprimir():
        id_nota = obtener_id()
        if not id_nota: return
        datos_completos = obtener_nota_por_id(conexion, id_nota)
        if datos_completos:
            try:
                modelo = NPImpresionModelo(datos_completos)
                pdf_service = NotaPedidoPapel()
                ctrl = NPImpresionControlador(modelo, pdf_service)
                ctrl.generar_y_abrir()
            except Exception as e:
                messagebox.showerror("Error de Impresión", str(e), parent=ventana)

    # UI setup
    vista.crear_toolstrip(ventana, agregar, modificar, eliminar, imprimir)
    c_col, e_txt = vista.crear_filtro(ventana, ejecutar_filtro)
    tree_cabecera, tree_detalle = vista.crear_tablas(ventana)

    tree_cabecera.bind("<<TreeviewSelect>>", al_seleccionar_cabecera)

    if id_ot:
        e_txt.insert(0, str(id_ot))
        ejecutar_filtro("id_ot", str(id_ot))
    else:
        cargar_todo()

    parent.wait_window(ventana)

def iniciar_np(parent, conexion, id_ot=None):
    iniciar_notas_pedido(parent, conexion, id_ot)