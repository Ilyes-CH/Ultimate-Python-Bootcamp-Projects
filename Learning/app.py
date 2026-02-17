# app.py
from taipy.gui import Gui

# State variable
name = ""
input_text = ""
output = ""

# Output text will depend on name
def greet(state):
    state.greeting = f"Hello, {state.name}!"

def update_text(state):
    state.output = f"Printing: {state.input_text}"

greeting = ""

page = """
## Welcome to Taipy 🐍

### Enter your name

<|{name}|input|label=Your Name|>

<|{input_text}|input|label=Say Something|on_change=update_text|>

## Output:

<|{output}|text|>

<|Click me!|button|on_action=greet|>

## Greeting:

<|{greeting}|text|>
"""

Gui(page).run()
