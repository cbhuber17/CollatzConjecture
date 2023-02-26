"""An interactive Collatz Conjecture module using Dash."""

import pandas as pd
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
from plot_cc import plot_line 
import collatz_conjecture as cc

COLOR_MODE_DASH = {'font_color': ('black', 'white'),
                   'bg_color': ('#ffffd0', '#3a3f44')}

app = dash.Dash(__name__, assets_folder='assets', title='Collatz Conjecture', update_title='Please wait...',
                external_stylesheets=[dbc.themes.BOOTSTRAP])

app.config.suppress_callback_exceptions = True  # Dynamic layout

# TODO: Fill in a header HTML
# TODO: Step 1-2 not getting plotted

server = app.server

# Hold CC stats for table display
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

@app.callback(Output('dark-mode-value', 'data'), [Input('dark-mode-switch', 'value')])
def dark_mode_setting(dark_mode):
    """CALLBACK: Updates the global value of dark mode based on changes in the switch.
    TRIGGER: Upon page loading and toggling the dark mode switch.
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :return: (bool) Whether the plot is done in dark mode or not """
    return dark_mode

# ------------------------------------------------------------------------

@app.callback(Output('main', 'style'), [Input('dark-mode-switch', 'value')])
def update_layout(dark_mode):
    """CALLBACK: Updates layout based on the dark mode toggle switch selected.
    TRIGGER: Upon page loading and when selecting the toggle for dark mode
    :param: dark_mode (bool) If dark mode plotting is done (True), light mode plotting (False)
    :return: (dict) of styles to represent the main layout colors"""

    return {'fontFamily': 'Arial', 'fontSize': 18, 'color': COLOR_MODE_DASH['font_color'][dark_mode],
            'border': '4px solid skyblue', 'background-color': COLOR_MODE_DASH['bg_color'][dark_mode]}

# ------------------------------------------------------------------------

@app.callback(
        [Output('line-cc', 'figure'), Output('table', 'data')],
        [Input('dark-mode-switch', 'value'), Input('input-num-cc', 'value')],
        State('table', 'data'), State('table', 'columns'))
def update_table(dark_mode, n, rows, columns):
    """CALLBACK: Updates the line chart based on the dark mode and input number provided.
    TRIGGER: Upon page load, toggling the dark mode switch, or changing starting input number.
    :param: dark_mode (bool) Whether the plot is done in dark mode or not
    :param: n (int) Starting seed for collatz-conjecture
    :rows: n (int) A link to the table data
    :columns: n (int) A link to the table columns
    :return: (go.Figure), df.to_dict('records')"""

    global cc_stats

    if not n:
        raise PreventUpdate

    n = cc.check_number(n)

    # Extract python processing time
    # JS processing time (in the clientside_callback below) is not computed
    step_num, conjecture, processing_time = cc.do_cc(n)

    # CC stats for table population
    cc_stats.append([n, "{:.2f}".format(processing_time*1e6), len(step_num)])
    df_cc_stats = pd.DataFrame(cc_stats, columns=['Starting Number', 'Processing time (us)', '# Steps'])

    # Just get a basic figure object then wipe out the data when a new input number comes in
    fig = plot_line(step_num, conjecture, processing_time, False, True, dark_mode)

    # Clear the data when a new number comes in
    # Start with step 1 at input n
    fig.data[0]['x'] = [1] 
    fig.data[0]['y'] = [n] 

    return fig, df_cc_stats.to_dict('records')

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
                                     'color': COLOR_MODE_DASH['font_color'][dark_mode]
                                    },
                                 style_cell={'textAlign': 'center',
                                             'height': 'auto',
                                             'padding-right': '10px',
                                             'padding-left': '10px',
                                             'whiteSpace': 'normal',
                                             'backgroundColor': COLOR_MODE_DASH['bg_color'][dark_mode],
                                             'color': COLOR_MODE_DASH['font_color'][dark_mode],
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
                  figure=plot_line([0], [0], 0, False, True, dark_mode)),
        dcc.Interval(id='interval', disabled=True, interval=250, max_intervals=10000),
        dcc.Store(id='current-num', data=0),
        dcc.Store(id='step-num', data=1),
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

'''
A clientside callback to pass the interval speed to the interval object.
TRIGGER: Upon filling the input-interval-ms box.
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
A faster clientside callback to do the CC for one step at a time.
The interval object calls this at the speed provided from the callback from
the previous function.
TRIGGER: When an input is provided.  Then it:
- Appends the data to the plot
- Disables the interval if we've hit the end
- Keeps track fo the current number and step number in their dcc.Store objects.
'''
app.clientside_callback(
    """
    function singleCollatzConjecture(input_n, n, step_num, n_intervals) {
    
        // Very first number comes in
        if (n == null || n === 0) {
            n = input_n;
        }

        // A new number comes in
        if(n === 1) {
            n = input_n;
            step_num = 1;
        }

        step_num += 1;

        if (n % 2 === 0) {
            n /= 2;
            } else {
            n = 3 * n + 1;
        }

        // Stop the interval when 1 his hit
        disable_interval = n === 1 ? true : false;

        // TODO: Figure out why step # 2 is not plotted
        //console.log(step_num);
        //console.log(n);

        return [[{x: [[step_num]], y: [[n]]}], disable_interval, n, step_num];

}
    """,
    Output('line-cc', 'extendData'),
    Output('interval', 'disabled'),
    Output('current-num', 'data'),
    Output('step-num', 'data'),
    Input('input-num-cc', 'value'),
    Input('current-num', 'data'),
    Input('step-num', 'data'),
    Input('interval', 'n_intervals'),  # This is needed to keep the interval going
    prevent_initial_call=True
)
# ------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server()