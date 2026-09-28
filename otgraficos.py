from otgraficocontrolador import OTGraficosControlador


def abrir_graficos(parent, repositorio_ot):
    """
    Archivo puente entre el sistema OT y el módulo de gráficos.

    parent: ventana padre (Tk o Toplevel)
    repositorio_ot: objeto que sabe obtener las OT
    """
    OTGraficosControlador(parent, repositorio_ot)

