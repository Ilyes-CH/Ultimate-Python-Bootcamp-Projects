from taipy.gui import Gui
from taipy.gui.gui_actions import notify
from PIL import Image, ImageFilter, ImageOps
import os

# Initialize state variable
preview_image_path = "./images/placeholder.jpeg"
processed_image_path = "./images/placeholder.jpeg"
uploaded = None  
content = ""
effect = ""

# Define available effects

effects ={
    "Grayscale" : lambda img: ImageOps.grayscale(img),
    "Blur" :  lambda img: img.filter(ImageFilter.BLUR),
    "Contour" :  lambda img: img.filter(ImageFilter.CONTOUR),
    "Sharpen" :    lambda img: img.filter(ImageFilter.SHARPEN),
}
effect_list = list(effects.keys())

def apply_fx(state):
    if not state.preview_image_path or not os.path.exists(state.preview_image_path):
        notify(state,"error","Please upload an image first")
        return 
    if not state.effect:
        notify(state,"error","Please select an effect first")
        return
    try:
        img = Image.open(state.preview_image_path)
        new_img = effects[state.effect](img)
        out_path = f"./images/processed_{state.effect.lower()}.png"
        new_img.save(out_path)
        state.processed_image_path = out_path
        notify(state,"success",f"{state.effect} effect applied!")
    except Exception as e:
        notify(state,"error",f"{state.effect} effect failed: {e}")
    print(state.effect)
        

page = """
<style>
.image{
width:400px !important;
height:400px !important
}
</style>
# 🖼️ Image Effect App

<|layout|columns=1 1|


<|{content}|file_selector|label=Select an image|extensions==.jpg,.jpeg,.png|>

<|{effect}|selector|lov={effect_list}|label=Choose Effect|>

<|Apply Effect|button|on_action=apply_fx|>

## Original Preview:
<|{preview_image_path}|image|class_name=image|>

## Processed Preview:
<|{processed_image_path}|image|class_name=image|>


|>

"""

# Event listener
def on_change(state,var_name,var_val):
    
    print("var name: ",var_name)
    print("var value: ",var_val)
    if var_name == "content":
        state.preview_image_path = var_val
    if var_name == "effect":
        state.effect = var_val


gui = Gui(page)

if __name__ == "__main__":
    gui.run()
