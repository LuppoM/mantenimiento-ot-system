import os
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class NotaPedidoPapel:

    def generar(self, datos_cabecera, lista_detalles) -> str:
        fd, pdf_path = tempfile.mkstemp(suffix=".pdf")
        os.close(fd)

        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30
        )

        styles = getSampleStyleSheet()
        
        style_title = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=15, leading=18, textColor=colors.HexColor('#003366'), alignment=1)
        style_header_lbl = ParagraphStyle('HeaderLbl', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#003366'))
        style_header_val = ParagraphStyle('HeaderVal', fontName='Helvetica', fontSize=9, leading=11)
        style_table_th = ParagraphStyle('ThStyle', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=colors.HexColor('#003366'), alignment=1)
        style_table_td = ParagraphStyle('TdStyle', fontName='Helvetica', fontSize=9, leading=11)
        style_table_td_center = ParagraphStyle('TdStyleCenter', fontName='Helvetica', fontSize=9, leading=11, alignment=1)

        story = []

        # Normalización de cabecera
        num_nota = str(datos_cabecera.get("id_nota", datos_cabecera.get("num_nota", "N/A")))
        ot_asociada = str(datos_cabecera.get("id_ot", datos_cabecera.get("ot_asociada", "Sin OT")))
        if not ot_asociada or ot_asociada == "None":
            ot_asociada = "Sin OT"

        fecha_ped = str(datos_cabecera.get("fecha_pedido", ""))
        fecha_req = str(datos_cabecera.get("fecha_requerida", ""))
        destino = str(datos_cabecera.get("destino", datos_cabecera.get("planta_destino", "")))
        autor = str(datos_cabecera.get("autor", datos_cabecera.get("solicitante", "")))
        tipo_gasto = str(datos_cabecera.get("tipo_gasto", ""))
        mano_obra = str(datos_cabecera.get("mano_de_obra", datos_cabecera.get("mano_obra", "")))
        justificacion = str(datos_cabecera.get("justificacion", "Sin especificaciones."))

        # --- ENCABEZADO Y TÍTULO ---
        encabezado_data = [
            [
                Paragraph("<b>NOTA DE PEDIDO DE MATERIALES / SERVICIOS</b>", style_title),
                Paragraph(f"<b>N° NOTA:</b> {num_nota}<br/><b>OT:</b> {ot_asociada}", style_header_lbl)
            ]
        ]
        t_encabezado = Table(encabezado_data, colWidths=[390, 145])
        t_encabezado.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#003366')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0F4F8')),
            ('PADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(t_encabezado)
        story.append(Spacer(1, 10))

        # --- DATOS GENERALES ---
        datos_grid = [
            [
                Paragraph("Fecha Pedido:", style_header_lbl), Paragraph(fecha_ped, style_header_val),
                Paragraph("Planta Destino:", style_header_lbl), Paragraph(destino, style_header_val)
            ],
            [
                Paragraph("Fecha Requerida:", style_header_lbl), Paragraph(fecha_req, style_header_val),
                Paragraph("Solicitante:", style_header_lbl), Paragraph(autor, style_header_val)
            ],
            [
                Paragraph("Tipo de Gasto:", style_header_lbl), Paragraph(tipo_gasto, style_header_val),
                Paragraph("Mano de Obra:", style_header_lbl), Paragraph(mano_obra, style_header_val)
            ]
        ]
        t_datos = Table(datos_grid, colWidths=[90, 175, 95, 175])
        t_datos.setStyle(TableStyle([
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 5),
            ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F9FAFC')),
            ('BACKGROUND', (2,0), (2,-1), colors.HexColor('#F9FAFC')),
        ]))
        story.append(t_datos)
        story.append(Spacer(1, 8))

        # --- JUSTIFICACIÓN ---
        just_data = [
            [Paragraph("Justificación / Observaciones:", style_header_lbl)],
            [Paragraph(justificacion, style_header_val)]
        ]
        t_just = Table(just_data, colWidths=[535])
        t_just.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F9FAFC')),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_just)
        story.append(Spacer(1, 12))

        # --- TABLA DE ÍTEMS ---
        items_table_data = [
            [
                Paragraph("Item", style_table_th),
                Paragraph("Cant.", style_table_th),
                Paragraph("Detalle / Repuesto Solicitado", style_table_th),
                Paragraph("Destino", style_table_th)
            ]
        ]

        for item in lista_detalles:
            if isinstance(item, (list, tuple)):
                n = len(item)
                if n >= 6:
                    # (id_detalle, id_nota, num_item, cantidad, detalle, destino_equipo)
                    num, cant, det, dest = item[2], item[3], item[4], item[5]
                elif n == 5:
                    # (id_nota, num_item, cantidad, detalle, destino_equipo)
                    num, cant, det, dest = item[1], item[2], item[3], item[4]
                elif n == 4:
                    # (num_item, cantidad, detalle, destino_equipo)
                    num, cant, det, dest = item[0], item[1], item[2], item[3]
                else:
                    continue
                
                num, cant, det, dest = str(num), str(cant), str(det), str(dest)

            elif isinstance(item, dict):
                num = str(item.get("num_item", item.get("num", "")))
                cant = str(item.get("cantidad", item.get("cant", "")))
                det = str(item.get("detalle", ""))
                dest = str(item.get("destino_equipo", item.get("destino", "")))
            else:
                continue

            items_table_data.append([
                Paragraph(num, style_table_td_center),
                Paragraph(cant, style_table_td_center),
                Paragraph(det, style_table_td),
                Paragraph(dest, style_table_td)
            ])

        t_items = Table(items_table_data, colWidths=[40, 50, 245, 200])
        t_items.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#D9E1F2')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#888888')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_items)
        story.append(Spacer(1, 30))

        # --- FIRMAS ---
        firmas_data = [
            [
                Paragraph("___________________________<br/><b>Firma</b>", style_table_td_center)
            ]
        ]
        t_firmas = Table(firmas_data, colWidths=[535])
        t_firmas.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ]))
        
        story.append(KeepTogether(t_firmas))

        doc.build(story)
        return pdf_path