import os
from taipy.gui import Gui
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.utils import ImageReader

#state variables

watermark_text = ""
font = "Helvetica"
size = 36
image = None
message = ""

fonts = ["Helvetica", "Courier", "Times-Roman", "Helvetica-Bold", "Courier-Bold", "Times-Bold"]


def create_watermark_pdf(text,font,size,image_path=None, file_name= "watermark.pdf"):
    c = canvas.Canvas(file_name,pagesize=letter)
    width, height = letter

    c.setFont(font,size)
    c.setFillGray(0.5,0.5)
    c.saveState()
    c.translate(width/2,height/2)
    c.rotate(45)
    c.drawCentredString(0,0,text)
    c.restoreState()

    if image_path:
        try:
            img = ImageReader(image_path)
            c.drawImage(img,width/4,height/4,width=200,height=100,mask="auto")
        except Exception as e:
            print("Image Error: ",e)

    c.save()

def apply_watermark_to_pdfs(watermark_file="watermark.pdf"):
    watermark = PdfReader(watermark_file)
    watermark_page = watermark.pages[0]

    pdf_files = [f for f in os.listdir() if f.endswith(".pdf") and f != watermark_file]

    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        for page in reader.pages:
            page.merge_page(watermark_page)
            writer.add_page(page)
        
        output_filename = f"watermarked_{pdf_file}"
        with open(output_filename, "wb") as f:
            writer.write(f)




page = """
# 🖋️ Watermark PDF Generator

### Enter Watermark Text
<|{watermark_text}|input|placeholder="Confidential"|style="width: 100%;"|>

### Choose Font
<|{font}|selector|lov={fonts}|style="width: 100%;"|>

### Font Size
<|{size}|input|type=number|min=8|max=72|style="width: 100%;"|>

### Optional: Upload Image for Watermark
<|{image}|file_selector|label=Upload Image|accept="image/*"|extensions=.jpg,.jpeg,.png|style="width: 100%;"|>

<|Generate and Apply Watermark|button|on_action=apply_watermark_action|style="margin-top: 15px;"|>

<|{message}|text|>
"""

def apply_watermark_action(state):
    if not state.watermark_text.strip():
        state.message = "Please enter the watermark text."
        return
    
    try:
        img_path = state.image if state.image else None
        create_watermark_pdf(state.watermark_text, state.font,int(state.size),image_path=img_path)
        apply_watermark_to_pdfs()
        state.message = "Watermark applied to all PDFs in the directory"
    except Exception as e:
        state.message = f"Watermark failed to be applied: {e}"


gui = Gui(page)

if __name__ == "__main__":
    gui.run()