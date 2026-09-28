class NPImpresionModelo:

    def __init__(self, datos_nota: dict):
        self._datos = datos_nota

    def obtener(self, campo):
        return self._datos.get(campo, "")

    def items(self):
        return self._datos.items()

    def to_dict(self):
        return self._datos