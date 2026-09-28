import os

class NPImpresionControlador:

    def __init__(self, modelo, pdf_service, impresion_service=None):
        self.modelo = modelo
        self.pdf_service = pdf_service
        self.impresion_service = impresion_service
        self.ruta_pdf = None

    def generar_y_abrir(self):
        datos = self.modelo.to_dict()
        
        # Desempaqueta cabecera y detalles para enviar ambos argumentos esperados por NotaPedidoPapel
        cabecera = datos.get("cabecera", datos)
        detalles = datos.get("detalles", [])

        self.ruta_pdf = self.pdf_service.generar(cabecera, detalles)

        if self.ruta_pdf and os.path.exists(self.ruta_pdf):
            os.startfile(self.ruta_pdf)

        return self.ruta_pdf