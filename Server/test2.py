import PyPDF2

# create a new PDF file
pdf = PyPDF2.PdfFileWriter()

# create a new page
page = pdf.addPage(PyPDF2.pdf.PageObject())

# create the table and set its position and size
table_data = [["User ID", "Name"]]
user_dict = {"2345": "martin", "2346": "john", "2347": "jane"}
for user_id, name in user_dict.items():
    table_data.append([user_id, name])

table = PyPDF2.Table()
table.setStyle(PyPDF2.TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PyPDF2.Color(0, 0, 0, alpha=0.1)),
    ('TEXTCOLOR', (0, 0), (-1, 0), PyPDF2.Color(0, 0, 0)),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), PyPDF2.Color(0, 0, 0, alpha=0.05)),
    ('TEXTCOLOR', (0, 1), (-1, -1), PyPDF2.Color(0, 0, 0)),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BOX', (0, 0), (-1, -1), 1, PyPDF2.Color(0, 0, 0)),
]))

table.setData(table_data)
table.wrapOn(page, 0, 0)
table.drawOn(page, 50, 700)

# save the PDF file
with open('output.pdf', 'wb') as file:
    pdf.write(file)
