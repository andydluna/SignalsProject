import matplotlib.figure
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

START = 0
END = 3

def plot_graph(operator, val):
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    if operator == "+":
        t = np.arange(START - val, END - val, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    elif operator == "*":
        t = np.arange(START, END, .01)
        fig.add_subplot(111).plot(t / val, 2 * np.sin(2 * np.pi * t))
    else:
        t = np.arange(START, END, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * -t))

    
    layout = [
        [sg.Text("Sine Wave")],
        [sg.Canvas(key="-CANVAS-")],
        [
            sg.In(size=(25, 1), enable_events=True, key="-SHIFT VALUE-"), 
            sg.VSeparator(),
            sg.Button("Shift", size=(10, 1), key="-SHIFT-")
        ],
        [
            sg.In(size=(25, 1), enable_events=True, key="-COMPRESS VALUE-"), 
            sg.VSeparator(),
            sg.Button("Compress", size=(10, 1), key="-COMPRESS-")
        ],
        [sg.Button("Reverse", size=(10, 1), key="-REVERSE-")],
    ]
    
    new_window = sg.Window(
        "Matplotlib Single Graph",
        layout,
        location=(0,0),
        finalize=True,
        element_justification="center",
        font="Helvetica 18",
    )
    
    draw_figure(new_window["-CANVAS-"].TKCanvas, fig)

fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
t = np.arange(START, END, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg

# Define the window layout 
layout = [
    [sg.Text("Sine Wave")],
    [sg.Canvas(key="-CANVAS-")],
    [
        sg.In(size=(25, 1), enable_events=True, key="-SHIFT VALUE-"), 
        sg.VSeparator(),
        sg.Button("Shift", size=(10, 1), key="-SHIFT-")
    ],
    [
        sg.In(size=(25, 1), enable_events=True, key="-COMPRESS VALUE-"), 
        sg.VSeparator(),
        sg.Button("Compress", size=(10, 1), key="-COMPRESS-")
    ],
    [sg.Button("Reverse", size=(10, 1), key="-REVERSE-")],
]

# Create the form and show it without the plot
window = sg.Window(
    "Matplotlib Single Graph",
    layout,
    location=(0,0),
    finalize=True,
    element_justification="center",
    font="Helvetica 18",
)

# Add the plot to the window
draw_figure(window["-CANVAS-"].TKCanvas, fig)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    
    if event == "-SHIFT-":
        val = float(values["-SHIFT VALUE-"])
        plot_graph("+", val)
        
    if event == "-COMPRESS-":
        val = float(values["-COMPRESS VALUE-"])
        plot_graph("*", val)
        
    if event == "-REVERSE-":
        plot_graph("", "")