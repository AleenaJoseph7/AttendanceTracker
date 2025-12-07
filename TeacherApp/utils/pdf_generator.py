from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from io import BytesIO


def generate_pdf_table(title, data_rows, column_color_map=None):
    buffer = BytesIO()
    styles = getSampleStyleSheet()

    # =============== TITLE BETWEEN TWO HORIZONTAL LINES ===============
    title_text = f"<para alignment='center'><b>{title}</b></para>"

    line_style = ParagraphStyle(
        name='LineStyle',
        alignment=TA_CENTER,
        fontSize=16,
        leading=22,
        textColor=colors.HexColor("#2C3E50"),
    )

    # =============== COLUMN TEXT STYLES ===============
    header_style = ParagraphStyle(
        name='HeaderStyle',
        fontSize=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        textColor=colors.white
    )

    first_col_style = ParagraphStyle(
        name='FirstColStyle',
        fontSize=11,
        alignment=TA_JUSTIFY,
        wordWrap='CJK',
        textColor=colors.HexColor("#2C3E50"),
        leading=14
    )

    center_style = ParagraphStyle(
        name='CenterStyle',
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#2C3E50"),
        leading=14
    )

    # =============== FOOTER PAGE NUMBER ===============
    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(30, 15, "Confidential - For Internal Use Only")
        canvas.drawRightString(A4[0] - 30, 15, f"Page {doc.page}")
        canvas.restoreState()

    # =============== DOCUMENT SETUP ===============
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    # =============== WRAP DATA INTO PARAGRAPHS ===============
    wrapped_data = []
    for i, row in enumerate(data_rows):
        wrapped_row = []
        for j, cell in enumerate(row):

            style_used = header_style if i == 0 else (
                first_col_style if j == 0 else center_style
            )

            # Attendance colour mapping
            if column_color_map and i > 0 and j in column_color_map:
                color = column_color_map[j](cell)
                style_used = ParagraphStyle(
                    name="DynamicStyle",
                    parent=style_used,
                    textColor=color
                )

            wrapped_row.append(Paragraph(str(cell), style_used))

        wrapped_data.append(wrapped_row)

    # =============== TABLE WIDTHS (WIDER & SPACIOUS) ===============
    available_width = A4[0] - 80
    col_widths = [
        available_width * 0.30,   # Subject
        available_width * 0.15,   # Code
        available_width * 0.15,   # Internal
        available_width * 0.15,   # Total
        available_width * 0.15    # Attendance
    ]

    table = Table(wrapped_data, colWidths=col_widths, hAlign="CENTER")

    # =============== HEADER COLOR (medium pastel blue) ===============
    header_color = colors.HexColor("#7EA6C4")  # visible borders + classy

    # =============== TABLE STYLE (NO STRIPES) ===============
    style = TableStyle([

        # HEADER BACKGROUND
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        ('TOPPADDING', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 14),

        # ----- FIX: MAKE HEADER COLUMN BORDERS CLEAR -----
        ('LINEBEFORE', (1, 0), (-1, 0), 1, colors.white),
        ('LINEAFTER', (0, 0), (-2, 0), 1, colors.white),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, colors.HexColor("#5C6D7B")),

        # ----- BODY BORDER -----
        ('BOX', (0, 0), (-1, -1), 1.2, colors.HexColor("#7F8C8D")),
        ('GRID', (0, 1), (-1, -1), 0.7, colors.HexColor("#B0BEC5")),

        # ----- CELL SPACING -----
        ('TOPPADDING', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),

        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table.setStyle(style)

    # =============== ELEMENTS TO RENDER ===============
    elements = [
        Spacer(1, 5),
        Paragraph("<u></u>", line_style),   # top line
        Paragraph(title_text, line_style),  # centered title
        Paragraph("<u></u>", line_style),   # bottom line
        Spacer(1, 20),
        table
    ]

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

    buffer.seek(0)
    return buffer
