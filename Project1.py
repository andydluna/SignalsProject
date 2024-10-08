import matplotlib.figure
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

def overview_window():
  layout = [
    [sg.Titlebar("Overview")],
    [sg.Text("The purpose of this project is to:", size=(23, 2))],
    [sg.Text(" - Visualize the given signal", size=(23, 1))],
    [sg.Text(" - Simulate the effects of shifting, scaling, and reversing a signal", size=(23, 3))],
    [sg.Button("Exit", key="Exit", size=(10,1))]
  ]
  
  window = sg.Window(
    "Overview",
    layout,
    font="Helvetica 25",
  )
  
  while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
  window.close()
      
def graph_window(type, scale=1, reverse=1, start=-5, end=5, show_options=True):
  fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
  t = np.arange(start, end, .01)
  
  if type == "Sin":
    fig.add_subplot(111).plot(t, np.sin(2 * np.pi * reverse *(t / scale)))
  if type == "Cos":
    fig.add_subplot(111).plot(t, np.cos(2 * np.pi * reverse *(t / scale)))
    
  matplotlib.use("TkAgg")

  def draw_figure(canvas, figure):
      figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
      figure_canvas_agg.draw()
      figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
      return figure_canvas_agg

  # Define the window layout 
  if show_options:
    layout = [
        [sg.Text(f"{type} Wave")],
        [sg.Canvas(key="-CANVAS-")],
        [
            sg.In(size=(25, 1), enable_events=True, key="-SHIFT VALUE-"), 
            sg.VSeparator(),
            sg.Button("Shift", size=(10, 1), key="-SHIFT-")
        ],
        [
            sg.In(size=(25, 1), enable_events=True, key="-COMPRESS VALUE-"), 
            sg.VSeparator(),
            sg.Button("Scale", size=(10, 1), key="-COMPRESS-")
        ],
        [
          sg.Button("Reverse", size=(10, 1), key="-REVERSE-"),
          sg.Button("Shift & Scale", size=(10, 1), key="-COMBINATION-"),
          sg.Button("SSR", size=(10, 1), key="-ALL-"),
        ],
        [ sg.Button("Exit", size=(10, 1), key="Exit") ]
    ]
  else:
    layout = [
        [sg.Text(f"{type} Wave")],
        [sg.Canvas(key="-CANVAS-")],
        [ sg.Button("Exit", size=(10, 1), key="Exit") ]
    ]

  # Create the form and show it without the plot
  window = sg.Window(
      "Graph Manipulation",
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
        shift = float(values["-SHIFT VALUE-"])
        graph_window(type, start= start - shift, end= end - shift, show_options=False)
          
      if event == "-COMPRESS-":
        scale = float(values["-COMPRESS VALUE-"])
        graph_window(type, scale=scale, start=start, end=end, show_options=False)
          
      if event == "-REVERSE-":
        graph_window(type, reverse=-1, start=start, end=end, show_options=False)
        
      if event == "-COMBINATION-":
        shift = float(values["-SHIFT VALUE-"])
        scale = float(values["-COMPRESS VALUE-"])
        graph_window(type, start= start - shift, end= end - shift, scale = scale, show_options=False)
        
      if event == "-ALL-":
        shift = float(values["-SHIFT VALUE-"])
        scale = float(values["-COMPRESS VALUE-"])
        graph_window(type, start= start - shift, end= end - shift, scale = scale, reverse=-1, show_options=False)
  window.close()
  
def main_menu():
  layout = [
    [sg.Titlebar("Wave Manipulation Simulator")],
    [sg.Text("Select an option to continue:")],
    [sg.Button("Overview", size=(10, 1), key="-OVERVIEW-")],
    [sg.Button("Sin Wave Plot", size=(15, 1), key="-SIN-")],
    [sg.Button("Cos Wave Plot", size=(15, 1), key="-COS-")],
    # [sg.Button("Tan Wave Plot", size=(15, 1), key="-TAN-")],
    [sg.Button("Exit", size=(10,1), key="Exit")]
  ]

  window = sg.Window(
    "Wave Manipulation Simulator",
    layout,
    element_justification="center",
    font="Helvetica 25",
  )

  while True:
      event, values = window.read()
      if event == "Exit" or event == sg.WIN_CLOSED:
        break
      if event == "-OVERVIEW-":
        overview_window()
      if event == "-SIN-":
        graph_window(type="Sin")
      if event == "-COS-":
        graph_window(type="Cos")
      # if event == "-TAN-":
      #   graph_window(type="Tan")
  window.close()
  
def main():
  main_menu()
  
if __name__ == '__main__':
  main()