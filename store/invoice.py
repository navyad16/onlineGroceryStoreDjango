from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generate_invoice(order):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Invoice_Order_{order.id}.pdf"'
    )

    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    y = height - 50

    # ---- HEADER ----
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, y, "GroceryMart Invoice")
    y -= 30

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Order ID: {order.id}")
    y -= 20
    pdf.drawString(50, y, f"Customer: {order.user.username}")
    y -= 20
    pdf.drawString(50, y, f"Status: {order.status}")
    y -= 30

    # ---- TABLE HEADER ----
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Product")
    pdf.drawString(300, y, "Qty")
    pdf.drawString(350, y, "Price")
    y -= 15

    pdf.line(50, y, 550, y)
    y -= 20

    # ---- ITEMS ----
    pdf.setFont("Helvetica", 12)

    for item in order.items.all():
        pdf.drawString(50, y, item.product.name)
        pdf.drawString(300, y, str(item.quantity))
        pdf.drawString(350, y, f"₹{item.price * item.quantity}")
        y -= 20

        # NEW PAGE IF NEEDED
        if y < 100:
            pdf.showPage()
            y = height - 50
            pdf.setFont("Helvetica", 12)

    # ---- TOTAL ----
    y -= 10
    pdf.line(50, y, 550, y)
    y -= 30

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(350, y, f"Total: ₹{order.total_amount}")

    # ---- FOOTER ----
    y -= 40
    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, "Thank you for shopping with GroceryMart!")

    pdf.showPage()
    pdf.save()

    return response
