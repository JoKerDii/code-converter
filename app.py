import gradio as gr
from optimization import optimize_code
from execution import run_python_code, run_cpp_code

css = """
.python {background-color: #306998;}
.cpp {background-color: #050;}
"""

pi = """
import time

def calculate(iterations, param1, param2):
    result = 1.0
    for i in range(1, iterations+1):
        j = i * param1 - param2
        result -= (1/j)
        j = i * param1 + param2
        result += (1/j)
    return result

start_time = time.time()
result = calculate(100_000_000, 4, 1) * 4
end_time = time.time()

print(f"Result: {result:.12f}")
print(f"Execution Time: {(end_time - start_time):.6f} seconds")
"""


with gr.Blocks(css=css) as ui:
    gr.Markdown("## Convert Python to C++")
    with gr.Row():
        python = gr.Textbox(label="Python code:", value=pi, lines=10)
        cpp = gr.Textbox(label="C++ code:", lines=10)
    with gr.Row():
        model = gr.Dropdown(["GPT", "Claude"], label="Select model", value="GPT")
    with gr.Row():
        convert = gr.Button("Convert code")
    with gr.Row():
        python_run = gr.Button("Run Python")
        cpp_run = gr.Button("Run C++")
    with gr.Row():
        python_out = gr.TextArea(label="Python result:", elem_classes=["python"])
        cpp_out = gr.TextArea(label="C++ result:", elem_classes=["cpp"])

    convert.click(optimize_code, inputs=[python, model], outputs=[cpp])
    python_run.click(run_python_code, inputs=[python], outputs=[python_out])
    cpp_run.click(run_cpp_code, inputs=[cpp], outputs=[cpp_out])

ui.launch(inbrowser=True)
