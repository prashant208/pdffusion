from reportlab.pdfgen import canvas

def create_pdf(filename, text):
    c = canvas.Canvas(filename)
    c.drawString(100, 750, text)
    c.save()

if __name__ == "__main__":
    create_pdf("dummy1.pdf", "This is the first PDF.")
    create_pdf("dummy2.pdf", "This is the second PDF.")
    print("Created dummy1.pdf and dummy2.pdf")
