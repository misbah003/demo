import random
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

# ---------- Helpers ----------
def money(x):
    d = Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(d)

def random_date(start_days_ago=365, end_days_ago=0):
    today = date.today()
    low = today - timedelta(days=start_days_ago)
    high = today - timedelta(days=end_days_ago)
    rand_days = random.randint(0, (high - low).days)
    return (low + timedelta(days=rand_days)).isoformat()

def generate_company():
    names = ["Acme Trading Pvt Ltd", "Nimbus Solutions", "Sunrise Exports", "BlueWave Imports"]
    return {
        "company_name": random.choice(names),
        "tax_id": f"GSTIN{random.randint(10000000,99999999)}",
    }

# ---------- Data Generators ----------
def generate_invoice():
    seller = generate_company()
    customer = generate_company()
    invoice_number = f"INV-{random.randint(1000,9999)}"
    inv_date = random_date()
    subtotal = 0
    items = []
    for i in range(random.randint(1,4)):
        qty = random.randint(1,10)
        rate = round(random.uniform(50, 500),2)
        line_total = qty * rate
        subtotal += line_total
        items.append((f"Item {i+1}", qty, rate, line_total))
    vat_rate = random.choice([0.05, 0.12, 0.18])
    vat_amount = round(subtotal * vat_rate,2)
    total = round(subtotal + vat_amount,2)
    return {
        "seller": seller,
        "customer": customer,
        "invoice_number": invoice_number,
        "invoice_date": inv_date,
        "items": items,
        "subtotal": subtotal,
        "vat_rate": vat_rate,
        "vat_amount": vat_amount,
        "total": total
    }

def create_invoice_pdf(inv, filename):
    # Create a simple text-based PDF using canvas directly
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Set font
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, "TAX INVOICE")

    c.setFont("Helvetica", 12)
    y_position = height - 1.5*inch

    # Seller info
    c.drawString(1*inch, y_position, f"Seller: {inv['seller']['company_name']}")
    y_position -= 0.3*inch
    c.drawString(1*inch, y_position, f"GSTIN: {inv['seller']['tax_id']}")
    y_position -= 0.5*inch

    # Customer info
    c.drawString(1*inch, y_position, f"Customer: {inv['customer']['company_name']}")
    y_position -= 0.3*inch
    c.drawString(1*inch, y_position, f"GSTIN: {inv['customer']['tax_id']}")
    y_position -= 0.5*inch

    # Invoice details
    c.drawString(1*inch, y_position, f"Invoice Number: {inv['invoice_number']}")
    y_position -= 0.3*inch
    c.drawString(1*inch, y_position, f"Date: {inv['invoice_date']}")
    y_position -= 0.5*inch

    # Items
    for item in inv['items']:
        c.drawString(1*inch, y_position, f"Item: {item[0]}, Qty: {item[1]}, Rate: ₹{item[2]}, Total: ₹{item[3]}")
        y_position -= 0.3*inch

    y_position -= 0.2*inch
    c.drawString(1*inch, y_position, f"Subtotal: ₹{inv['subtotal']}")
    y_position -= 0.3*inch
    c.drawString(1*inch, y_position, f"VAT ({inv['vat_rate']*100}%): ₹{inv['vat_amount']}")
    y_position -= 0.3*inch
    c.drawString(1*inch, y_position, f"Total: ₹{inv['total']}")

    c.save()

# Generate sample PDFs
for i in range(3):
    inv = generate_invoice()
    create_invoice_pdf(inv, f"sample_invoice_{i+1}.pdf")

print("✅ Sample PDFs generated successfully.")