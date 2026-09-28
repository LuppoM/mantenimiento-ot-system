from tkinter import messagebox
import sectoresmodelo as modelo
import sectoresvista as vista
import abmsectores


def iniciar_sectores(parent, conexion):
    # -------------------------------------------------
    # VISTA
    # -------------------------------------------------
    ventana = vista.crear_ventana(parent)
    botones = vista.crear_toolstrip(ventana)
    tree = vista.crear_tabla(ventana)

    # -------------------------------------------------
    # LÓGICA
    # -------------------------------------------------
    def cargar_datos():
        tree.delete(*tree.get_children())
        for fila in modelo.obtener_sectores(conexion):
            tree.insert("", "end", values=fila)

    def agregar():
        abmsectores.abrir_abm_sector(
            parent=ventana,
            conexion=conexion,
            modo="agregar",
            on_guardar=cargar_datos   # 🔁 CALLBACK
        )

    def modificar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccione un sector",
                parent=ventana
            )
            return

        datos = tree.item(seleccionado)["values"]

        abmsectores.abrir_abm_sector(
            parent=ventana,
            conexion=conexion,
            modo="modificar",
            datos=datos,
            on_guardar=cargar_datos   # 🔁 CALLBACK
        )

    def eliminar():
        seleccionado = tree.focus()
        if not seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccione un sector",
                parent=ventana
            )
            return

        sector_id = tree.item(seleccionado)["values"][0]

        if messagebox.askyesno(
            "Confirmar",
            "¿Eliminar sector?",
            parent=ventana
        ):
            modelo.eliminar_sector(conexion, sector_id)
            cargar_datos()

    # -------------------------------------------------
    # ASIGNACIÓN DE COMANDOS
    # -------------------------------------------------
    botones["agregar"].config(command=agregar)
    botones["modificar"].config(command=modificar)
    botones["eliminar"].config(command=eliminar)
    botones["atras"].config(command=ventana.destroy)

    cargar_datos()
