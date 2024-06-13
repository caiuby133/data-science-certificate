import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

# Create app

app = dash.Dash(__name__)

# Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
df = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv"
)

# Extract year and month from the date column

df["Month"] = pd.to_datetime(
    df["Date"]
).dt.month_name()  # used for the names of the months
df["Year"] = pd.to_datetime(df["Date"]).dt.year

regions = df["Region"].unique().tolist()
years = df["Year"].unique().tolist()

app.layout = html.Div(
    children=[
        html.H1(
            "Australia Wildfire Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        html.H3(
            "Select Region:",
            style={"textAlign": "left", "color": "#503D36", "font-size": 40},
        ),
        dcc.RadioItems(
            id="region-radio",
            options=regions,
            value=regions[0],
            style={"textAlign": "left"},
            inline=True,
        ),
        html.H3(
            "Select Year:",
            style={"textAlign": "left", "color": "#503D36", "font-size": 40},
        ),
        dcc.Dropdown(id="year-dropdown", options=years, value=years[0]),
        html.Div(
            style={"display": "flex"},
            children=[
                dcc.Graph(id="monthly-fire-area-pie"),
                dcc.Graph(id="monthly-fire-bar"),
            ],
        ),
    ]
)

# TASK 2.2: Add the radio items and a dropdown right below the first inner division
# outer division starts

# Second Inner division for adding 2 inner divisions for 2 output graphs
# TASK 2.3: Add two empty divisions for output inside the next inner division.


# layout ends
# TASK 2.4: Add the Ouput and input components inside the app.callback decorator.
# Place to add @app.callback Decorator
@app.callback(
    [
        Output(component_id="monthly-fire-area-pie", component_property="figure"),
        Output(component_id="monthly-fire-bar", component_property="figure"),
    ],
    [
        Input(component_id="region-radio", component_property="value"),
        Input(component_id="year-dropdown", component_property="value"),
    ],
)


# TASK 2.5: Add the callback function.
# Place to define the callback function .
def reg_year_display(input_region, input_year):

    # data
    region_data = df[df["Region"] == input_region]
    y_r_data: pd.DataFrame = region_data[region_data["Year"] == input_year]
    monthlyEstFireArea = y_r_data.groupby("Month", as_index=False)[
        "Estimated_fire_area"
    ].mean()
    # Plot one - Monthly Average Estimated Fire Area
    fig1 = px.pie(
        data_frame=monthlyEstFireArea,
        names="Month",
        values="Estimated_fire_area",
        title="{} : Monthly Average Estimated Fire Area in year {}".format(
            input_region, input_year
        ),
    )

    # Plot two - Monthly Average Count of Pixels for Presumed Vegetation Fires

    firesPerMonth = y_r_data.groupby("Month", as_index=False)["Count"].sum()
    firesTotal = firesPerMonth["Count"].sum()
    firesPerMonth["Percentage"] = firesPerMonth["Count"] / firesTotal * 100
    fig2 = px.bar(
        data_frame=firesPerMonth,
        x="Month",
        y="Percentage",
        title="{} : Average Count of Pixels for Presumed Vegetation Fires in year {}".format(
            input_region, input_year
        ),
    )

    return [fig1, fig2]


if __name__ == "__main__":
    app.run_server()
