# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, callback, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Read the airline data into pandas dataframe
airline_data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv",
    encoding="ISO-8859-1",
    dtype={
        "Div1Airport": str,
        "Div1TailNum": str,
        "Div2Airport": str,
        "Div2TailNum": str,
    },
)
# Create a dash application
app = dash.Dash(__name__)


@callback(
    Output("line-plot", "figure"),
    Input("input-year", "value"),
)
def updateFigure(value: str):
    if not (airline_data["Year"].min() <= value <= airline_data["Year"].max()):
        raise PreventUpdate

    airline_year_data = airline_data[airline_data["Year"] == int(value)]
    line_data = airline_year_data.groupby("Month")["ArrDelay"].mean().reset_index()

    fig = go.Figure(
        data=go.Scatter(
            x=line_data["Month"],
            y=line_data["ArrDelay"],
            mode="lines",
            marker=dict(color="green"),
        )
    )
    fig.update_layout(
        title=f"Month vs Average Flight Delay Time ({value})",
        xaxis_title="Month",
        yaxis_title="ArrDelay",
    )

    return fig


fig = go.Figure(
    data=go.Scatter(
        x=airline_data["Month"],
        y=airline_data["ArrDelay"],
        mode="lines",
        marker=dict(color="green"),
    )
)
fig.update_layout(
    title="Month vs Average Flight Delay Time",
    xaxis_title="Month",
    yaxis_title="ArrDelay",
)

app.layout = html.Div(
    children=[
        html.H1(
            "Airline Performance Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        html.Div(
            [
                "Input Year: ",
                dcc.Input(
                    id="input-year",
                    value="2010",
                    type="number",
                    style={"height": "50px", "font-size": 35},
                ),
            ],
            style={"font-size": 40},
        ),
        html.Br(),
        html.Br(),
        html.Div(dcc.Graph(id="line-plot", figure=fig)),
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server()
