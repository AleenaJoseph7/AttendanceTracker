from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO


def generate_pdf_table(title, data_rows, column_color_map=None):
    buffer = BytesIO()
    styles = getSampleStyleSheet()

    # Title
    title_text = f"<para alignment='center'><b>{title}</b></para>"

    line_style = ParagraphStyle(
        name='LineStyle',
        alignment=TA_CENTER,
        fontSize=16,
        leading=22,
        textColor=colors.HexColor("#2C3E50"),
    )

    #cell styles
    header_style = ParagraphStyle(
        name='HeaderStyle',
        fontSize=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        textColor=colors.white,
    )

    first_col_style = ParagraphStyle(
        name='FirstColStyle',
        fontSize=11,
        alignment=TA_JUSTIFY,
        wordWrap='CJK',
        textColor=colors.HexColor("#2C3E50"),
        leading=14,
    )

    center_style = ParagraphStyle(
        name='CenterStyle',
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2C3E50"),
        leading=14,
    )

    # footer
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(30, 15, "Confidential - For Internal Use Only")
        canvas.drawRightString(A4[0] - 30, 15, f"Page {doc.page}")
        canvas.restoreState()

    # document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=60,
        bottomMargin=40
    )

    # wrap data
    wrapped_data = []
    for i, row in enumerate(data_rows):
        wrapped_row = []
        for j, cell in enumerate(row):

            style_used = header_style if i == 0 else (
                first_col_style if j == 0 else center_style
            )

            if column_color_map and i > 0 and j in column_color_map:
                color = column_color_map[j](cell)
                style_used = ParagraphStyle(
                    name="DynamicStyle",
                    parent=style_used,
                    textColor=color
                )

            wrapped_row.append(Paragraph(str(cell), style_used))

        wrapped_data.append(wrapped_row)

    # width
    available_width = A4[0] - 60
    col_widths = [
        available_width * 0.28,
        available_width * 0.15,
        available_width * 0.15,
        available_width * 0.15,
        available_width * 0.17
    ]

    table = Table(wrapped_data, colWidths=col_widths, hAlign="CENTER")

    # header color
    header_color = colors.HexColor("#7EA6C4")

    # border
    border_color = colors.HexColor("#4D4D4D")

    # Table Style
    style = TableStyle([

        # HEADER
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        ('TOPPADDING', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 14),

        # HEADER BORDER LINES
        ('LINEBEFORE', (1, 0), (-1, 0), 1, border_color),
        ('LINEAFTER', (0, 0), (-2, 0), 1, border_color),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, border_color),

        # FULL TABLE BORDER
        ('BOX', (0, 0), (-1, -1), 1.2, border_color),

        # INNER GRID
        ('GRID', (0, 1), (-1, -1), 0.7, border_color),

        # CELL SPACING
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table.setStyle(style)

    # Elements
    elements = [
        Spacer(1, 5),
        Paragraph("<u></u>", line_style),
        Paragraph(title_text, line_style),
        Paragraph("<u></u>", line_style),
        Spacer(1, 20),
        table
    ]

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

    buffer.seek(0)
    return buffer
