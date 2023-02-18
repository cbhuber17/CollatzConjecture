from timeit import default_timer as timer
import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
import collatz_conjecture as cc
from PlotlyHexagonTheme import plotly_hexagon_theme


pio.templates.default = 'plotly+hex_novatel'

# ----------------------------------------------------------------------------------------------

def plot_line(x, y, processing_time, plot_offline=True):

    traces = go.Scatter(x=x, y=y, mode='lines', name='CC', connectgaps=True)

    layout = go.Layout(title={'text': f'Collatz Conjecture',
               'x': 0.5,
               'y': 0.95,
               'xanchor': 'center',
               'yanchor': 'top'},
               xaxis_title={'text': "Step #"},
               yaxis_title={'text': "Value"})

    fig = go.Figure(data=traces, layout=layout)

    # Show processing time and steps
    fig.add_annotation(xref='paper', yref='paper', x=0.9, y=0.9, showarrow=False, text=f'<b>Processing Time:</b> {processing_time*1e6:.3f} us')
    fig.add_annotation(xref='paper', yref='paper', x=0.9, y=0.8, showarrow=False, text=f'<b>Number Steps:</b> {len(x)}')

    if plot_offline:
        pyo.plot(fig, filename='cc.html')

    return fig

# ----------------------------------------------------------------------------------------------

# TODO: This should be in cc.py?
def do_cc(n):

    num_steps = 1
    step_num = []
    conjecture = []

    start = timer()

    while n != 1:
        n = cc.single_collatz_conjecture(n)
        num_steps += 1

        step_num.append(num_steps)
        conjecture.append(n)

    end = timer()
    processing_time = end - start
    return step_num, conjecture, processing_time

# ----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    n = cc.get_number()
    n = cc.check_number(n)
    step_num, conjecture, processing_time = do_cc(n)

    plot_line(step_num, conjecture, processing_time)