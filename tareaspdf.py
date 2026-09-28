import os
import ctypes
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

def obtener_carpeta_documentos():
    CSIDL_PERSONAL = 5
    buf = ctypes.create_unicode_buffer(260)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, 0, buf)
    return buf.value

class TareasPDFService:
    def __init__(self):
        carpeta_documentos = obtener_carpeta_documentos()
        self.carpeta_pdf = os.path.join(carpeta_documentos, "Informes_Tareas")
        os.makedirs(self.carpeta_pdf, exist_ok=True)

    def generar_informe_diario(self, lista_tareas, titulo_archivo):
        # Extraemos la fecha de la primera tarea
        fecha_tarea = lista_tareas[0].get('fecha', 'N/A') if lista_tareas else "N/A"
        
        nombre_archivo = f"Informe_{titulo_archivo.replace('-', '_')}.pdf"
        ruta_pdf = os.path.join(self.carpeta_pdf, nombre_archivo)
        
        c = canvas.Canvas(ruta_pdf, pagesize=A4)
        ancho_a4, alto_a4 = A4
        
        y_pos = alto_a4 - 50
        
        # Encabezado principal
        self._dibujar_cabecera_pagina(c, fecha_tarea, ancho_a4, alto_a4)
        y_pos -= 60

        for tarea in lista_tareas:
            # Control de salto de página proactivo
            if y_pos < 180: 
                c.showPage()
                self._dibujar_cabecera_pagina(c, fecha_tarea, ancho_a4, alto_a4)
                y_pos = alto_a4 - 110

            y_pos = self._dibujar_item_tarea(c, tarea, y_pos, ancho_a4)
            y_pos -= 25 # Espacio extra entre bloques para que no se peguen

        c.save()
        return ruta_pdf

    def _dibujar_cabecera_pagina(self, c, fecha, ancho, alto):
        # Título centrado y destacado
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(ancho/2, alto - 40, "INFORME DE TRABAJO REALIZADO")
        
        c.setFont("Helvetica", 12)
        c.drawCentredString(ancho/2, alto - 60, f"Fecha del Relevamiento: {fecha}")
        
        # Línea de división estética
        c.setStrokeColor(colors.black)
        c.setLineWidth(1.2)
        c.line(40, alto - 75, ancho - 40, alto - 75)

    def _dibujar_item_tarea(self, c, tarea, y, ancho_pagina):
        x_margen = 40
        ancho_util = ancho_pagina - 80 # Aprovechamos casi todo el ancho A4
        centro_x = ancho_pagina / 2
        
        mecs = tarea.get('mecanicos', '---')
        hors = tarea.get('horarios', '---')
        repo = tarea.get('reporte', '')

        # --- SECCIÓN CENTRADA (Encabezados) ---
        # Horario y Mecánicos con fuente clara y centrada
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(centro_x, y - 20, f"HORARIO: {hors}")
        
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(centro_x, y - 35, f"MECÁNICOS: {mecs}")
        
        # Línea sutil de separación interna
        c.setStrokeColor(colors.lightgrey)
        c.setLineWidth(0.5)
        c.line(x_margen + 20, y - 42, ancho_pagina - 60, y - 42)
        
        # --- SECCIÓN DE REPORTE ---
        c.setStrokeColor(colors.black)
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(x_margen + 10, y - 57, "Descripción detallada de la tarea:")
        
        c.setFont("Helvetica", 10)
        # El texto multilinea ahora usa el ancho máximo aprovechable
        y_final = self._dibujar_texto_multilinea(c, repo, x_margen + 10, y - 72, ancho_util - 20)
        
        # Dibujo del recuadro exterior (ajustado al contenido)
        alto_bloque = y - y_final + 8
        c.setLineWidth(1)
        c.rect(x_margen, y_final - 8, ancho_util, alto_bloque)
        
        return y_final - 8

    def _dibujar_texto_multilinea(self, c, texto, x, y, max_ancho):
        lineas = str(texto).split('\n')
        for parrafo in lineas:
            palabras = parrafo.split()
            linea = ""
            for palabra in palabras:
                prueba = linea + " " + palabra if linea else palabra
                # Verificamos ancho de línea dinámicamente
                if c.stringWidth(prueba, "Helvetica", 10) < max_ancho:
                    linea = prueba
                else:
                    c.drawString(x, y, linea)
                    y -= 14 # Interlineado un poco más amplio para mejor lectura
                    linea = palabra
            c.drawString(x, y, linea)
            y -= 14
        return y