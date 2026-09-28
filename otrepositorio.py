from datetime import datetime


class RepositorioOT:

    def __init__(self, conexion):
        self.conexion = conexion

    # =====================================================
    # HELPERS
    # =====================================================
    def texto_seguro(self, valor):
        if valor is None:
            return ""
        return str(valor).strip().lower()

    # -----------------------------------------------------
    # FECHA SEGURA (mejorada)
    # -----------------------------------------------------
    def fecha_segura(self, fecha_valor):

        if not fecha_valor:
            return None

        # ✅ Si ya es datetime
        if isinstance(fecha_valor, datetime):
            return fecha_valor

        formatos = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
        ]

        for fmt in formatos:
            try:
                return datetime.strptime(str(fecha_valor), fmt)
            except ValueError:
                continue

        return None

    # -----------------------------------------------------
    # ESTADO CERRADA
    # -----------------------------------------------------
    def es_cerrada(self, valor):
        valor = self.texto_seguro(valor)

        return valor in (
            "si", "s", "true", "1",
            "cerrada", "cerrado"
        )

    # =====================================================
    # FILTRO GENERICO
    # =====================================================
    def filtrar_lista(self, datos, planta=None, linea=None, mes=None, anio=None):

        planta = self.texto_seguro(planta)
        linea = self.texto_seguro(linea)

        if not planta or planta == "todos":
            planta = None

        if not linea or linea == "todas":
            linea = None

        filtradas = []

        for ot in datos:

            fecha = ot.get("fecha")
            if not fecha:
                continue

            if planta and ot["planta"] != planta:
                continue

            if linea and ot["linea"] != linea:
                continue

            if mes and fecha.month != mes:
                continue

            if anio and fecha.year != anio:
                continue

            filtradas.append(ot)

        return filtradas
