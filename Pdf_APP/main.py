from taipy.gui import Gui
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import  ImageReader


user_input = ""
message = ""
font = "Helvetica" #Default font
size = 18 #Default size
title = ""
file_name = ""
image = None

# Available fonts in reportlab standard fonts
fonts = ["Helvetica", "Courier", "Times-Roman", "Helvetica-Bold", "Courier-Bold", "Times-Bold"]

def create_title(c:canvas.Canvas,title:str,size:int,font:str,width:int,height:int):
    title_width = c.stringWidth(title,font,size)
    c.drawString((width - title_width)/ 2,height-80,title)

def create_pdf(image_path:str,title:str,text:str,font:str,size:int,filename="output.pdf"):
    c = canvas.Canvas(filename,pagesize=letter)
    width, height = letter
    # Draw a page border (rectangle)
    margin = 40
    c.setLineWidth(2)
    c.rect(margin,margin,width - 2*margin, height - 2*margin)

    #Draw the Title
    create_title(c,title,size,font,width=width,height=height)

    # Draw the Text
    y = height - 120
    c.setFont(font,14)
    for line in text.splitlines():
        print(y)
        c.drawString(72,y,line)
        y -= 15
    print(height,y)
    # Draw the Image
    image_margin = 20
    y -= image_margin
    if image_path:
        c.drawImage(image_path,72,y - 250,width=200,height=200)
    c.save()

page = """
<style>
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 700px;
    margin: 30px auto;
    padding: 0 15px;
    color: white;
    background: #f9f9f9;
  }
  h1 {
    text-align: center;
    color: #4a90e2;
    margin-bottom: 10px;
  }
  header, footer {
    text-align: center;
    color: #666;
    font-size: 0.9em;
    margin: 15px 0 40px 0;
  }
  main {
    background: #fff;
    padding: 25px 30px 40px 30px;
    border-radius: 8px;
    box-shadow: 0 3px 10px rgb(0 0 0 / 0.1);
  }
  label {
    font-weight: 600;
    margin-bottom: 6px;
    display: block;
  }
  input, select, textarea, button {
    width: 100%;
    padding: 10px 12px;
    margin-bottom: 20px;
    border-radius: 6px;
    border: 1px solid #ddd;
    font-size: 1em;
    transition: border-color 0.3s ease;
  }
  input:focus, select:focus, textarea:focus {
    border-color: #4a90e2;
    outline: none;
  }
  button {
    background: #4a90e2;
    border: none;
    color: white;
    font-weight: 700;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  button:hover {
    background: #357ABD;
  }
  .message {
    text-align: center;
    font-weight: 600;
    color: #4a90e2;
    margin-top: 10px;
  }
</style>

# 📝 Create your PDF Document

---

### File Name (without extension)
<|{file_name}|input|placeholder=example_document|style="width: 100%;"|>

### Title
<|{title}|input|placeholder=My PDF Title|style="width: 100%;"|>

### Enter your text
<|{user_input}|input|multiline|rows=6|placeholder=Type your content here...|style="width: 100%;"|>

### Choose Font
<|{font}|selector|lov={fonts}|style="width: 100%;"|>

### Font Size for Title
<|{size}|input|type=number|min=8|max=72|placeholder=24|style="width: 100%;"|>

### Upload an Image to Append
<|{image}|file_selector|label=Choose Image|accept="image/*"|style="width: 100%;"|extensions==.jpg,.jpeg,.png|>

<|{message}|text|>

<|Create PDF|button|on_action=create_pdf_action|style="margin-top: 15px;"|>


---

<footer style="margin-top: 40px; font-size: 0.9em; color: #666; text-align: center;">
  © 2025 CrocoCoder. All rights reserved.
</footer>
"""

def create_pdf_action(state):
    if not state.file_name.strip():
        state.message = "Please enter a file name"
        return
    if not state.user_input.strip():
        state.message = "Please enter a some text"
        return
    if not state.title.strip():
        state.message = "Please enter a title"
        return

    try:
        clean_text = state.user_input.replace("\\n","\n")
        img = None
        if state.image:
            img = ImageReader(state.image)
        
        create_pdf(image_path=img,
                   title=state.title,
                   text=clean_text,
                   font=state.font,
                   size=int(state.size),
                   filename=f"{state.file_name}.pdf"
                   )
        state.message = f"PDF, '{state.file_name}.pdf' created successfully!"
    except Exception as e:
        state.message = f"Error in creating pdf file: {e}"

gui = Gui(page)

if __name__ == "__main__":
    gui.run()