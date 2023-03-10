from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib import animation
from flask import Flask, request, Response
from flask_cors import CORS
from solve import solve
from the_algo_wrapper import plot_return_fig, plot_figure_8
import io
import json

app = Flask(__name__)
CORS(app)

# http://127.0.0.1:5000/api/threebody?query=[1.989e30,9.945e29,4.972e29,0,0,0,0,149.6e9,0,0,29.78e3,-149.6e9,0,0,-29.78e3,200,10000]
@app.route('/api/threebody')
def threebody():
    print(request.args)
    
    query = request.args.copy().get('query', 'hello').replace(' ', '')
    print(query)
    if query is None:
        query = ''
    print(f'app.py:{query}')
    paras = json.loads(query)
    x1, y1, x2, y2, x3, y3 = solve(*paras)
    # some processing
    output = {'ans': [x1, y1, x2, y2, x3, y3]}
    return output

@app.route('/api/threebody/plot.gif')
def plot_png():
    fig, anim = plot_figure_8()

    f = r"plot.gif" 
    writergif = animation.PillowWriter(fps=30) 
    anim.save(f, writer=writergif)
    
    output = io.BytesIO()
    # FigureCanvasSVG(anim).print_svg(output)
    with open(f, "rb") as fh:
        output = io.BytesIO(fh.read())
    return Response(output.getvalue(), mimetype='image/gif')

if __name__ == "__main__":
    app.run()
