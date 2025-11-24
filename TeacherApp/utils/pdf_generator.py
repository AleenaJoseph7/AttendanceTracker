from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO


def generate_pdf_table(title, data_rows, column_color_map=None):
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.alignment = TA_CENTER
    title_style.fontSize = 18

    header_style = ParagraphStyle(name='HeaderStyle', fontSize=12, alignment=TA_CENTER, fontName='Helvetica-Bold')
    first_col_style = ParagraphStyle(name='FirstColStyle', fontSize=10, alignment=TA_JUSTIFY, wordWrap='CJK')
    center_style = ParagraphStyle(name='CenterStyle', fontSize=10, alignment=TA_CENTER)

    def add_page_number(canvas, doc):
        canvas.saveState()
        page_number_text = f"Page {doc.page}"
        footer_text = "Confidential - For Internal Use Only"
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(30, 15, footer_text)
        canvas.drawRightString(A4[0] - 30, 15, page_number_text)
        canvas.restoreState()

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=30, bottomMargin=40)

    # Wrap cells in Paragraphs and apply color if needed
    wrapped_data = []
    for i, row in enumerate(data_rows):
        wrapped_row = []
        for j, cell in enumerate(row):
            style_to_use = header_style if i == 0 else (first_col_style if j == 0 else center_style)
            # Apply conditional color
            if column_color_map and i > 0 and j in column_color_map:
                color = column_color_map[j](cell)
                style_to_use = ParagraphStyle(name='TempStyle', parent=style_to_use, textColor=color)
            wrapped_row.append(Paragraph(str(cell), style_to_use))
        wrapped_data.append(wrapped_row)

    num_cols = len(data_rows[0])
    col_widths = [200] + [(A4[0] - 240) / (num_cols - 1)] * (num_cols - 1)
    table = Table(wrapped_data, colWidths=col_widths, hAlign='CENTER')

    zebra_colors = [colors.whitesmoke, colors.lightgrey]
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4A90E2')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.8, colors.grey),
        ('BOX', (0, 0), (-1, -1), 1, colors.grey)
    ])

    for i, row in enumerate(wrapped_data[1:], start=1):
        style.add('BACKGROUND', (0, i), (-1, i), zebra_colors[i % 2])

    table.setStyle(style)
    elements = [Paragraph(f"<b>{title}</b>", title_style), Spacer(1, 20), table]
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    buffer.seek(0)
    return buffer
