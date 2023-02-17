import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_daq as daq
from plot_cc import plot_line, do_cc
import collatz_conjecture as cc

app = dash.Dash(__name__, assets_folder='assets', title='Collatz Conjecture', update_title='Please wait...',
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True  # Dynamic layout

server = app.server

# ------------------------------------------------------------------------

app.layout = html.Div([
    dcc.Location(id='url'),
    dcc.Store(id='viewport-container', data={}, storage_type='session'),
    dcc.Store(id='dark-mode-value', data=True, storage_type='session'),
    html.Div(id='page-content')
])

# ------------------------------------------------------------------------

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), Input('dark-mode-value', 'data'), Input('viewport-container', 'data')])
def display_page(pathname, dark_mode, screen_size):
    """CALLBACK: Updates the page content based on the URL.
    TRIGGER: Upon page loading and when the URL changes
    :param: pathname (str) The URL in the browser
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :param: screen_size (dict) Dictionary of 'height' and 'width' the screen size
    :return: dash HTML layout based on the URL."""

    if pathname == '/':
        return main_layout(dark_mode)

# ------------------------------------------------------------------------

@app.callback(Output('line-cc', 'figure'), [Input('dark-mode-switch', 'value'), Input('input-num-cc', 'value')])
def update_line(dark_mode, n):
    """CALLBACK: Updates the line charts based on the dark mode selected.
    TRIGGER: Upon page load, toggling the dark mode switch, or changing x-axis timeline by button or zoom.
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :param: n (int) Starting seed for collatz-conjecture
    :return: (go.Figure), (go.Figure) objects that will be dynamically updated"""

    n = cc.check_number(n)

    step_num, conjecture, processing_time = do_cc(n)

    fig = plot_line(step_num, conjecture, processing_time, False)

    return fig

# ------------------------------------------------------------------------

def main_layout(dark_mode):
    """Returns the main/default (index) layout of the page.
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :return: dash HTML layout"""

    layout = html.Div([
        html.Header(
            [

            ]
        ),
        html.Div(
            [
                daq.ToggleSwitch(id='dark-mode-switch',
                                 label={'label': 'View Page in Dark Mode:', 'style': {'font-size': '20px'}},
                                 value=dark_mode,
                                 size=50,
                                 color='orange'),
                "Enter integer number to start the Collatz-Conjecture: ",  # Hit enter/click outside box
                dcc.Input(id='input-num-cc', type='number', value=1, min=1, step=1, debounce=True)
            ], id='page-settings'
        ),
        html.Hr(),
        dcc.Graph(id="line-cc",
                  mathjax='cdn',
                  responsive='auto',
                  figure=plot_line([0,1], [0,1], False)),
        html.Hr(),
        html.Footer(
            [
                html.Div(
                    ['This page was created using python apps: Plotly and Dash'],
                    id='footer-note'
                ),
                html.Div(
                    ['Contact:'],
                    id='footer-contact'
                ),
                html.Div(
                    ['Ⓒ Colin Huber 2023'],
                    id='copyright'
                )
            ]
        )
    ], id='main')

    return layout

# ------------------------------------------------------------------------

"""CALLBACK: A client callback to execute JS in a browser session to get the screen width and height.
TRIGGER: Upon page loading.
Results are put in the Store() viewport-container data property."""
app.clientside_callback(
    """
    function(href) {
        var w = screen.width;
        var h = screen.height;
        return {'height': h, 'width': w};
    }
    """,
    Output('viewport-container', 'data'),
    Input('url', 'href')
)

# ------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server()