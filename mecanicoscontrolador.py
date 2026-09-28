from tkinter import messagebox
import mecanicosmodelo as modelo
import mecanicosvista as vista
import abmmecanicos


def iniciar_mecanicos(parent, conexion):
    ventana = vista.crear_ventana(parent)
    botones = vista.crear_toolstrip(ventana)
    tree = vista.crear_tabla(ventana)

    # -------------------------
    # CARGA DE DATOS
    # -------------------------
    def cargar_datos():
        tree.delete(*tree.get_children())
        for fila in modelo.obtener_mecanicos(conexion):
            tree.insert("", "end", values=fila)

    # -------------------------
    # ACCIONES
    # -------------------------
    def agregar():
        abmmecanicos.abrir_abm_mecanico(
            parent=ventana,
            conexion=conexion,
            modo="agregar",
            on_guardar=cargar_datos
        )

    def modificar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccione un mecánico",
                parent=ventana
            )
            return

        datos = tree.item(seleccionado)["values"]

        abmmecanicos.abrir_abm_mecanico(
            parent=ventana,
            conexion=conexion,
            modo="modificar",
            datos=datos,
            on_guardar=cargar_datos
        )

    def eliminar():
        messagebox.showinfo(
            "Info",
            "Eliminación se hará en ABMMecánicos",
            parent=ventana
        )

    # -------------------------
    # ASIGNACIÓN DE BOTONES
    # -------------------------
    botones["agregar"].config(command=agregar)
    botones["modificar"].config(command=modificar)
    botones["eliminar"].config(command=eliminar)
    botones["atras"].config(command=ventana.destroy)

    cargar_datos()
