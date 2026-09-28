class OTImpresionModelo:

    def __init__(self, datos_ot: dict):
        self._datos = datos_ot

    def obtener(self, campo):
        return self._datos.get(campo, "")

    def items(self):
        return self._datos.items()

    def to_dict(self):
        return self._datos
