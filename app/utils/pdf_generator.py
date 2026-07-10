from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO


def generate_invoice(order):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []

    # عنوان المتجر
    elements.append(Paragraph("MEDIA ARTECH STORE", styles['Title']))
    elements.append(Spacer(1, 10))

    # رقم الطلب
    elements.append(Paragraph(f"Invoice #{order.id}", styles['Heading2']))
    elements.append(Spacer(1, 10))

    # بيانات العميل
    elements.append(Paragraph(f"Customer: {order.customer_name}", styles['Normal']))
    elements.append(Paragraph(f"Phone: {order.customer_phone}", styles['Normal']))
    elements.append(Paragraph(f"Email: {order.customer_email}", styles['Normal']))
    elements.append(Paragraph(f"Address: {order.customer_address}", styles['Normal']))
    elements.append(Spacer(1, 15))

    # الجدول
    data = [["Product", "Qty", "Price", "Color", "Size", "Text"]]

    for item in order.items:
        data.append([
            item.product_title,
            str(item.quantity),
            f"¥{item.price}",
            item.color or "-",
            item.size or "-",
            item.custom_text or "-"
        ])

    table = Table(data)

    table.setStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2563eb")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 1, colors.grey),
        ('ALIGN', (1,1), (-1,-1), 'CENTER'),
    ])

    elements.append(table)
    elements.append(Spacer(1, 20))

    # الإجمالي
    elements.append(Paragraph(f"Total: ¥{order.total_price}", styles['Heading2']))

    doc.build(elements)

    buffer.seek(0)
    return buffer