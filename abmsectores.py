from tkinter import messagebox
import abmsectoresvista as vista
import abmsectoresmodelo as modelo


def abrir_abm_sector(parent, conexion, modo, datos=None, on_guardar=None):
    """
    modo: 'agregar' | 'modificar'
    datos: (id, nombre, planta)
    on_guardar: callback para refrescar tabla
    """

    titulo = "Agregar Sector" if modo == "agregar" else "Modificar Sector"
    ventana = vista.crear_ventana(parent, titulo)

    botones = vista.crear_toolstrip(ventana)
    campos = vista.crear_formulario(ventana)

    # -----------------------------------------
    # PRECARGA EN MODIFICAR
    # -----------------------------------------
    if modo == "modificar" and datos:
        sector_id, nombre, planta = datos
        campos["nombre"].insert(0, nombre)
        campos["planta"].set(planta)

    # -----------------------------------------
    # GUARDAR
    # -----------------------------------------
    def guardar():
        nombre = campos["nombre"].get().strip()
        planta = campos["planta"].get().strip()

        if not nombre or not planta:
            messagebox.showwarning(
                "Atención",
                "Complete todos los campos",
                parent=ventana
            )
            return

        if modo == "agregar":
            modelo.insertar_sector(conexion, nombre, planta)
        else:
            modelo.modificar_sector(conexion, sector_id, nombre, planta)

        # 🔁 AVISO AL CONTROLADOR
        if on_guardar:
            on_guardar()

        ventana.destroy()

    botones["guardar"].config(command=guardar)
    botones["cancelar"].config(command=ventana.destroy)
