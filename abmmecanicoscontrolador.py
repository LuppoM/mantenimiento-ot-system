from tkinter import messagebox
import abmmecanicosvista as vista
import abmmecanicosmodelo as modelo


def iniciar_abm_mecanico(parent, conexion, modo, datos=None, on_guardar=None):
    titulo = "Agregar Mecánico" if modo == "agregar" else "Modificar Mecánico"
    ventana = vista.crear_ventana(parent, titulo)

    botones = vista.crear_toolstrip(ventana)
    campos = vista.crear_formulario(ventana)

    if modo == "modificar" and datos:
        mecanico_id, nombre = datos
        campos["nombre"].insert(0, nombre)

    def guardar():
        nombre = campos["nombre"].get().strip()

        if not nombre:
            messagebox.showwarning(
                "Atención",
                "Ingrese el nombre",
                parent=ventana
            )
            return

        if modo == "agregar":
            modelo.insertar_mecanico(conexion, nombre)
        else:
            modelo.modificar_mecanico(conexion, mecanico_id, nombre)

        if on_guardar:
            on_guardar()

        ventana.destroy()

    botones["guardar"].config(command=guardar)
    botones["cancelar"].config(command=ventana.destroy)
