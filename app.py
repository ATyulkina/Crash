from dash import Dash
import dash_bootstrap_components as dbc
from layouts import create_layout
from callbacks import register_callbacks

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = create_layout()
register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
