from abmnpcontrolador import iniciar_abmnotaspedido

def abrir_abmnp(parent, conexion, estado="AGREGAR", datos_nota=None, id_ot_asociada=None):
    iniciar_abmnotaspedido(parent, conexion, estado, datos_nota, id_ot_asociada)