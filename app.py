from dash import Dash, html, dcc, Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd
import numpy as np


# Setup app and layout/frontend
app = Dash(__name__,  external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.title = "RadioItems / Checklist comparison"
server = app.server

app.layout = html.Div([
    html.H1('RadioItems / Checklist comparison'),
    html.Iframe(
        id = 'iframe',
        style={'border-width': '0', 
        'width': '100%',
        'height': '400px',
        "top": "50%",
        "left": "50%",}),
    html.H3('Checklist'),
    html.P('The user can visualize multiple options at the same time'),
    dcc.Checklist(
        id = 'check',
        options = ['A', 'B', 'C'], 
        value = ['A', 'B', 'C']),
    html.H3('RadioItems'),
    html.P('The user can select only one option (the options are mutually exclusive )'),
    dcc.RadioItems(id = 'radio',
        options = ['set1', 
                   'set2', 
                   'tableau10',
                   'accent' ,
                   'dark2'],
        value =  'set1')])


# Set up callbacks/backend
@app.callback(
    Output('iframe', 'srcDoc'),
    Input('check', 'value'),
    Input('radio', 'value')
)
def plot_altair(cat, color):
  np.random.seed(42)
  source = pd.DataFrame(np.cumsum(np.random.randn(100, 3), 0).round(2),
                    columns=['A', 'B', 'C'], index=pd.RangeIndex(100, name='x'))
  source = source.reset_index().melt('x', var_name='category', value_name='y')
  source = source[source["category"].isin(cat)]
  line = alt.Chart(source).mark_line(interpolate='basis').encode(
  x='x:Q',
  y='y:Q',
  color='category:N').configure_range(
  category={'scheme': color})
  return line.to_html()


if __name__ == '__main__':
    app.run_server(debug=True)
