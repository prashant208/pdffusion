from reportlab.pdfgen import canvas

def create_multipage_pdf(filename, num_pages, prefix):
    c = canvas.Canvas(filename)
    for i in range(1, num_pages + 1):
        c.drawString(100, 750, f"{prefix} - Page {i}")
        c.showPage()
    c.save()

if __name__ == "__main__":
    create_multipage_pdf("multi1.pdf", 5, "Doc 1")
    create_multipage_pdf("multi2.pdf", 3, "Doc 2")
    print("Created multi1.pdf (5 pages) and multi2.pdf (3 pages)")
