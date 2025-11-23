from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf_table(title, data_rows):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"<b>{title}</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    table = Table(data_rows, hAlign='LEFT')

    # Table styling
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
    ])

    # Apply coloring to Internal Mark column (column index 1)
    for i, row in enumerate(data_rows[1:], start=1):
        try:
            mark = int(row[1])
            if mark < 35:
                style.add('TEXTCOLOR', (1,i), (1,i), colors.red)
            else:
                style.add('TEXTCOLOR', (1,i), (1,i), colors.green)
        except:
            pass

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    buffer.seek(0)
    return buffer
