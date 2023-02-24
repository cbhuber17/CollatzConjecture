"""TBD module description"""

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
from plot_cc import plot_line, do_cc
import collatz_conjecture as cc

app = dash.Dash(__name__, assets_folder='assets', title='Collatz Conjecture', update_title='Please wait...',
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True  # Dynamic layout

# TODO: Clear plot on new number
# TODO: A way of manually stopping plotting interval?  Or just entering a number does this?
# TODO: Remove starting coordinate [0,0]
# TODO: Double check x-axis range and y-axis range
# TODO: Dark mode

server = app.server

cc_stats = []
df_cc_stats = pd.DataFrame({'Starting Number': [0], 'Processing time (us)': [0], '# Steps': [0]})

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

@app.callback(
        # [
        # Output('line-cc', 'figure'),
        Output('table', 'data'),
        # ],
        [Input('dark-mode-switch', 'value'), Input('input-num-cc', 'value')],
        State('table', 'data'), State('table', 'columns'))
def update_table(dark_mode, n, rows, columns):
    """CALLBACK: Updates the line charts based on the dark mode selected.
    TRIGGER: Upon page load, toggling the dark mode switch, or changing x-axis timeline by button or zoom.
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :param: n (int) Starting seed for collatz-conjecture
    :return: (go.Figure), (go.Figure) objects that will be dynamically updated"""

    global cc_stats

    if not n:
        raise PreventUpdate

    n = cc.check_number(n)

    # TODO; Don't think can use this for clinentside callback, however can still extract processing time
    step_num, conjecture, processing_time = do_cc(n)

    cc_stats.append([n, "{:.2f}".format(processing_time*1e6), len(step_num)])
    df_cc_stats = pd.DataFrame(cc_stats, columns=['Starting Number', 'Processing time (us)', '# Steps'])

    # fig = plot_line(step_num, conjecture, processing_time, False, False)

    # return fig, df_cc_stats.to_dict('records')
    return df_cc_stats.to_dict('records')

# ------------------------------------------------------------------------

def get_table_container(df_cc_stats, dark_mode):
    """Provides an HTML container for centering a statistics table for each stats dataframe.
    :param: df_cc_stats (pandas.df) Stats data frame
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :return dbc.Container containing the HTML code for displaying the table."""

    stats_table = html.Div(
        [
            dash_table.DataTable(data=df_cc_stats.to_dict('records'), id='table',
                                 style_header={
                                     'fontWeight': 'bold',
                                    #  'color': COLOR_MODE_DASH['font_color'][dark_mode]
                                    },
                                 style_cell={'textAlign': 'center',
                                             'height': 'auto',
                                             'padding-right': '10px',
                                             'padding-left': '10px',
                                             'whiteSpace': 'normal',
                                            #  'backgroundColor': COLOR_MODE_DASH['bg_color'][dark_mode],
                                            #  'color': COLOR_MODE_DASH['font_color'][dark_mode],
                                             },
                                #  fill_width=False,
                                #  style_table={'overflowX': 'auto'},
                                #  style_as_list_view=True,
                                 columns=[{"name": i, "id": i} for i in df_cc_stats.columns],
                                 ),
        ],
    )

    container = dbc.Container([
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown(""), xs=12, sm=12, md=3, lg=3, xl=3,
                ),
                dbc.Col(
                    stats_table, xs=12, sm=12, md=6, lg=6, xl=6
                ),
                dbc.Col(
                    dcc.Markdown(""), xs=12, sm=12, md=3, lg=3, xl=3,
                )
            ]
        )

    ])

    return container

# ------------------------------------------------------------------------

def main_layout(dark_mode):
    """Returns the main/default (index) layout of the page.
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :return: dash HTML layout"""

    layout = html.Div([
        # html.Header(
        #     [

        #     ]
        # ),
        html.Div(
            [
                daq.ToggleSwitch(id='dark-mode-switch',
                                 label={'label': 'View Page in Dark Mode:',
                                         'style': {'fontSize': '20px'} 
                                         },
                                 value=dark_mode,
                                 size=50,
                                 color='orange'),
                html.Hr(),
                html.Div([
                        "Enter integer number to start the Collatz-Conjecture: ",
                        dcc.Input(id='input-num-cc', type='number', min=1, step=1, debounce=True),
                        ], id='cc-div'),
                html.Hr(),
                html.Div([
                        "Plotting speed 25-1000 (ms): ",
                        dcc.Input(id='input-interval-ms', type='number', value=250, min=25, max=1000, step=1, debounce=True),
                        ], id='plotting-speed-div')
            ], id='page-settings'
        ),
        html.Hr(),
        dcc.Graph(id="line-cc",
                  responsive='auto',
                  figure=plot_line([0], [0], 0, False, True)), #TODO: Remove as default?
        dcc.Interval(id='interval', disabled=True, interval=250, max_intervals=10000),
        dcc.Store(id='current-num', data=0),  #TODO: May not need to start at 0?
        html.Hr(),
        get_table_container(df_cc_stats, dark_mode),
        html.Hr(),
        html.Footer(
            [
                html.Div(
                    ['This page was created using python apps: Plotly and Dash'],
                    id='footer-note'
                ),
                html.Div(
                    ['Created by: Colin Huber 2023'],
                    id='copyright'
                )
            ]
        )
    ], id='main')

    return layout

# ------------------------------------------------------------------------

# TODO:: Remove?
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

# Pass interval speed to interval object
'''
TBD
'''
app.clientside_callback(
    """
    function intervalSpeed(interval_speed) {
    
        return interval_speed;
    }
    """,
    Output('interval', 'interval'),
    Input('input-interval-ms', 'value'),
    prevent_initial_call=True
)

# ------------------------------------------------------------------------

'''
TBD
'''
app.clientside_callback(
    """
    function singleCollatzConjecture(input_n, n, n_intervals) {
    
        if (n == null || n === 0) {
        n = input_n;
        }

        if (n % 2 === 0) {
        n /= 2;
        } else {
        n = 3 * n + 1;
        }

        disable_interval = n === 1 ? true : false;

        return [[{x: [[n_intervals]], y: [[n]]}], disable_interval, n];

}
    """,
    Output('line-cc', 'extendData'),
    Output('interval', 'disabled'),
    Output('current-num', 'data'),
    Input('input-num-cc', 'value'),
    Input('current-num', 'data'),
    Input('interval', 'n_intervals'),
    prevent_initial_call=True
)
# ------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)  #TODO: Remove debug