import abmplantascontrolador

def abrir_abmplantas(parent, conexion, estado="AGREGAR", datos_planta=None):
    """
    Puente que invoca el controlador del formulario ABM.
    estado: 'AGREGAR' o 'MODIFICAR'
    datos_planta: Diccionario {'id': x, 'nombre': 'y'}
    """
    abmplantascontrolador.iniciar_abm_planta(
        parent=parent, 
        conexion=conexion, 
        estado=estado, 
        datos_planta=datos_planta
    )