import os

class OTImpresionControlador:

    def __init__(self, modelo, pdf_service, impresion_service=None):

        self.modelo = modelo
        self.pdf_service = pdf_service
        self.impresion_service = impresion_service
        self.ruta_pdf = None

    def generar_y_abrir(self):

        self.ruta_pdf = self.pdf_service.generar(
            self.modelo.to_dict()
        )

        if self.ruta_pdf and os.path.exists(self.ruta_pdf):
            os.startfile(self.ruta_pdf)

        return self.ruta_pdf
