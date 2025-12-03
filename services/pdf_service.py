#!/usr/bin/env python3
from typing import List, Tuple, Callable
import os
import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class PdfService:
    def __init__(self, obtener_moneda: Callable[[], str]):
        self.obtener_moneda = obtener_moneda

    def generar_reporte_inventario(self, filename: str, productos: List[Tuple]) -> None:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=30, alignment=1)

        elements.append(Paragraph("Reporte de Inventario", title_style))

        info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, spaceAfter=20)
        elements.append(Paragraph(f"Fecha de generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))

        # Resumen
        total_productos = len(productos)
        stock_bajo = sum(1 for p in productos if p[4] <= p[5])
        stock_agotado = sum(1 for p in productos if p[4] == 0)
        valor_total = sum((p[4] * float(p[3])) for p in productos)
        moneda = self.obtener_moneda()

        resumen_data = [
            ['Total de Productos', str(total_productos)],
            ['Stock Bajo', str(stock_bajo)],
            ['Agotados', str(stock_agotado)],
            ['Valor Total del Inventario', f"{moneda}{valor_total:.2f}"]
        ]
        resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(resumen_table)
        elements.append(Spacer(1, 20))

        # Tabla productos
        productos_data = [['ID', 'Nombre', 'Categoría', 'Precio', 'Stock', 'Stock Mínimo', 'Valor Total']]
        for p in productos:
            precio = f"{moneda}{float(p[3]):.2f}"
            valor_p = float(p[3]) * int(p[4])
            productos_data.append([
                str(p[0]), p[1], p[2], precio, str(p[4]), str(p[5]), f"{moneda}{valor_p:.2f}"
            ])
        productos_table = Table(productos_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1*inch, 0.8*inch, 1*inch, 1*inch])
        productos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (3, 1), (6, -1), 'RIGHT'),
        ]))
        elements.append(productos_table)

        doc.build(elements)

    def generar_reporte_ventas(self, filename: str, ventas: List[Tuple]) -> None:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=30, alignment=1)
        elements.append(Paragraph("Reporte de Ventas", title_style))

        info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, spaceAfter=20)
        fecha_inicio = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        fecha_fin = datetime.datetime.now().strftime("%Y-%m-%d")
        elements.append(Paragraph(f"Período: {fecha_inicio} a {fecha_fin}", info_style))
        elements.append(Paragraph(f"Fecha de generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))

        total_ventas = len(ventas)
        monto_total = sum(v[2] for v in ventas)
        promedio = monto_total / total_ventas if total_ventas > 0 else 0
        moneda = self.obtener_moneda()

        resumen_data = [
            ['Total de Ventas', str(total_ventas)],
            ['Monto Total', f"{moneda}{monto_total:.2f}"],
            ['Promedio', f"{moneda}{promedio:.2f}"]
        ]
        resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(resumen_table)
        elements.append(Spacer(1, 20))

        ventas_data = [['ID', 'Cliente', 'Total', 'Fecha', 'Usuario']]
        for v in ventas:
            fecha = v[3].strftime("%Y-%m-%d %H:%M") if v[3] else ""
            total = f"{moneda}{v[2]:.2f}"
            usuario = v[4] if v[4] else "Sistema"
            ventas_data.append([str(v[0]), v[1], total, fecha, usuario])
        ventas_table = Table(ventas_data, colWidths=[0.5*inch, 2*inch, 1*inch, 1.5*inch, 1.5*inch])
        ventas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),
        ]))
        elements.append(ventas_table)

        doc.build(elements)

    def generar_reporte_completo(self, filename: str, info_cafeteria: List[Tuple[str, str]], resumen_ventas: Tuple[int, float, float], productos_vendidos: List[Tuple[str, int]], productos_bajo: List[Tuple[str, int, int]]) -> None:
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=30, alignment=1)
        elements.append(Paragraph("Reporte Completo del Sistema", title_style))

        info_style = ParagraphStyle('Info', parent=styles['Normal'], fontSize=10, spaceAfter=20)
        elements.append(Paragraph(f"Fecha de generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", info_style))

        # Información de la cafetería
        elements.append(Paragraph("Información de la Cafetería", styles['Heading2']))
        info_table = Table(info_cafeteria, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))

        # Resumen de Ventas
        elements.append(Paragraph("Resumen de Ventas", styles['Heading2']))
        total_ventas, monto_total, promedio = resumen_ventas
        moneda = self.obtener_moneda()
        resumen_ventas_data = [
            ['Total de Ventas', str(total_ventas)],
            ['Monto Total', f"{moneda}{monto_total:.2f}"],
            ['Promedio', f"{moneda}{promedio:.2f}"]
        ]
        resumen_ventas_table = Table(resumen_ventas_data, colWidths=[3*inch, 2*inch])
        resumen_ventas_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(resumen_ventas_table)
        elements.append(Spacer(1, 20))

        # Productos más vendidos
        elements.append(Paragraph("Productos Más Vendidos", styles['Heading2']))
        if productos_vendidos:
            productos_data = [['Producto', 'Cantidad Vendida']]
            for nombre, cantidad in productos_vendidos:
                productos_data.append([nombre, str(cantidad)])
            productos_table = Table(productos_data, colWidths=[3*inch, 2*inch])
            productos_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(productos_table)
        else:
            elements.append(Paragraph("No hay productos vendidos en el último mes", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Productos con stock bajo
        elements.append(Paragraph("Productos con Stock Bajo", styles['Heading2']))
        if productos_bajo:
            bajo_data = [['Producto', 'Stock Actual', 'Stock Mínimo']]
            for nombre, stock, stock_min in productos_bajo:
                bajo_data.append([nombre, str(stock), str(stock_min)])
            bajo_table = Table(bajo_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
            bajo_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            elements.append(bajo_table)
        else:
            elements.append(Paragraph("No hay productos con stock bajo", styles['Normal']))

        doc.build(elements)


