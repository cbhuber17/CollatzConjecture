"""Plots the sequence of the Collatz Conjecture"""

import plotly.offline as pyo
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
import collatz_conjecture as cc
from PlotlyHexagonTheme import plotly_hexagon_theme

pio.templates.default = 'plotly+hex_novatel'

# Dark/light mode colors
COLOR_MODE = {'title': ('black', 'white'),
              'spikecolor': ('black', 'white'),
              'paper_bgcolor': ('white', 'black'),
              'plot_bgcolor': ('#D6D6D6', '#3A3F44'),
              'range_bgcolor': ('lawngreen', 'navy'),
              'range_border_color': ('black', 'orange')}

# ----------------------------------------------------------------------------------------

def plot_line(x, y, processing_time, plot_offline=True, autorange=False, dark_mode=True) -> go.Figure:
    """
    Generates a plot of the Collatz Conjecture sequence.

    Args:
        x (list): List of x values.
        y (list): List of y values.
        processing_time (float): The time it took to process the sequence.
        plot_offline (bool, optional): Whether to display the plot offline. Defaults to True.
        autorange (bool, optional): Whether to enable automatic scaling of the y-axis. Defaults to False.

    Returns:
        go.Figure: A figure object representing the plot.

    Raises:
        None

    """

    if not x or not y:
        return None
    
    # Plot layout
    layout = go.Layout(title={'text': f'Collatz Conjecture',
               'x': 0.5,
               'y': 0.95,
               'xanchor': 'center',
               'yanchor': 'top'},
               xaxis_title={'text': "Step #"},
               yaxis_title={'text': "Value"},
               yaxis=dict(range=[0, max(y)], autorange=autorange),
               font=dict(
                         size=20,
                         color=COLOR_MODE['title'][dark_mode]
                        ),
                paper_bgcolor=COLOR_MODE['paper_bgcolor'][dark_mode],
                plot_bgcolor=COLOR_MODE['plot_bgcolor'][dark_mode],
                )

    # Offline plotting animation
    if plot_offline:
        init = 1
        traces = go.Scatter(x=x[:init], y=y[:init], mode='lines', name='CC', connectgaps=True)
        fig = go.Figure(data=traces, layout=layout)

        # Show processing time and steps
        fig.add_annotation(xref='paper', yref='paper', x=0.9, y=0.9, showarrow=False, text=f'<b>Processing Time:</b> {processing_time*1e6:.3f} us')
        fig.add_annotation(xref='paper', yref='paper', x=0.9, y=0.8, showarrow=False, text=f'<b>Number Steps:</b> {len(x)}')

        # Animate plotting
        fig.update(frames=[go.Frame(data=[go.Scatter(x=x[:k], y=y[:k])]) for k in range(init, len(x)+1)])

        # Add "play" button to start animation
        # TODO: Control animation speed on page load, not with "play" button
        fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Play",
                            method="animate",
                        args=[None, {"frame": {"duration": 250},
                                     "fromcurrent": True,
                                     "transition": {"duration": 0}
                                    }
                            ]
                        )
                    ]
                )
            )
        ]
    )

        # In milliseconds
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 250
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["transition"] = 100

    # Dash server plotting, just return the plot without animation 
    # (animation will be done by a clientside callback in dash)
    else:
        traces = go.Scatter(x=x, y=y, mode='lines', name='CC', connectgaps=True)
        fig = go.Figure(data=traces, layout=layout)
        fig.data[0]['x'] = []
        fig.data[0]['y'] = []

    fig.update_xaxes(showgrid=False, gridwidth=5, gridcolor='White', showspikes=True,
                     spikecolor=COLOR_MODE['spikecolor'][dark_mode], spikesnap="cursor", spikemode="across",
                     spikethickness=2,
                     rangeselector=dict(
                                        bgcolor=COLOR_MODE['range_bgcolor'][dark_mode],
                                        bordercolor=COLOR_MODE['range_border_color'][dark_mode],
                                        borderwidth=1,
                                       )
                     )

    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='White', showspikes=True,
                     spikecolor=COLOR_MODE['spikecolor'][dark_mode], spikethickness=2)


    if plot_offline:
        pyo.plot(fig, filename='cc.html')

    return fig

# ----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    n = cc.get_number()
    n = cc.check_number(n)
    step_num, conjecture, processing_time = cc.do_cc(n)

    plot_line(step_num, conjecture, processing_time)