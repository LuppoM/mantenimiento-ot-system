import os

import ctypes

from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import A4





# ==========================================

def obtener_carpeta_documentos():



    CSIDL_PERSONAL = 5



    buf = ctypes.create_unicode_buffer(260)



    ctypes.windll.shell32.SHGetFolderPathW(

        None,

        CSIDL_PERSONAL,

        None,

        0,

        buf

    )



    return buf.value





# ==========================================

class PDFService:



    def __init__(self):



        carpeta_documentos = obtener_carpeta_documentos()



        self.carpeta_pdf = os.path.join(

            carpeta_documentos,

            "impresionot"

        )



        os.makedirs(self.carpeta_pdf, exist_ok=True)



    # -----------------------------------

    def generar(self, datos_ot):



        ruta_pdf = os.path.join(

            self.carpeta_pdf,

            f"OT_{datos_ot.get('ID')}.pdf"

        )



        c = canvas.Canvas(ruta_pdf, pagesize=A4)



        # Copia 1

        self._dibujar_ot(

            c,

            datos_ot,

            y_base=420,

            titulo="COPIA SUPERVISOR"

        )



        # Copia 2

        self._dibujar_ot(

            c,

            datos_ot,

            y_base=30,

            titulo="COPIA MECANICO"

        )



        c.save()



        return ruta_pdf



    # -----------------------------------

    def _dibujar_ot(self, c, datos, y_base, titulo):



        ancho = 500

        alto = 360

        x = 50

        y = y_base



        # ----- Marco -----

        c.rect(x, y, ancho, alto)



        # ----- Titulo -----

        c.setFont("Helvetica-Bold", 13)

        c.drawCentredString(300, y + alto - 30, "ORDEN DE TRABAJO")



        c.setFont("Helvetica-Bold", 10)

        c.drawCentredString(300, y + alto - 50, titulo)



        # ----- Datos -----

        c.setFont("Helvetica", 9)



        y_texto = y + alto - 80



        col1_x = x + 15

        col2_x = x + 260



        mitad = len(datos) // 2

        items = list(datos.items())



        # Columna 1

        for campo, valor in items[:mitad]:



            y_texto = self._dibujar_texto_ajustado(

                c,

                f"{campo}: {valor}",

                col1_x,

                y_texto,

                220

            )



        # Reiniciar altura para columna 2

        y_texto = y + alto - 80



        for campo, valor in items[mitad:]:



            y_texto = self._dibujar_texto_ajustado(

                c,

                f"{campo}: {valor}",

                col2_x,

                y_texto,

                220

            )



    # -----------------------------------

    def _dibujar_texto_ajustado(self, c, texto, x, y, max_ancho):



        palabras = texto.split()

        linea = ""



        for palabra in palabras:



            prueba = linea + " " + palabra if linea else palabra



            if c.stringWidth(prueba, "Helvetica", 9) < max_ancho:

                linea = prueba

            else:

                c.drawString(x, y, linea)

                y -= 13

                linea = palabra



        if linea:

            c.drawString(x, y, linea)

            y -= 13



        return y