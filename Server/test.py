from reportlab.pdfgen import canvas

data = ["apple", "banana", "cherry", "date"]
pdf = canvas.Canvas("fruits.pdf")

y = 700  # starting y-coordinate
line_height = 20  # height of each line

for i, fruit in enumerate(data):
    x = 100  # starting x-coordinate
    y -= line_height * i  # adjust y-coordinate based on index
    pdf.drawString(x, y, f"{i + 1}. {fruit}")

pdf.save()
