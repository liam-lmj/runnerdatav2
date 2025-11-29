import json
import plotly
import plotly.express as px
import pandas as pd
from database.database_constants import lap_types, meters_to_miles, meters_to_kilometers, mileage_trend_axis, formatted_lap_types

def weekly_mileage_type_pie(data):
    pie_df = pd.DataFrame({
        'Types': ['Easy', 'LT1', 'LT2', 'Hard'],
        'Distance': [sum(activity.get(lap_type, 0) for activity in data) for lap_type in lap_types]
    })
    fig_pie = px.pie(pie_df, names="Types", values="Distance")
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    pie_chart = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    return pie_chart   

def mileage_trend_bar(data, unit, lap_type):
    if unit == "Miles":
        conversion = meters_to_miles
    elif unit == "Kilometers":
        conversion = meters_to_kilometers
    
    y_axis = mileage_trend_axis.get(lap_type, formatted_lap_types) if type(lap_type) == str else lap_type

    bar_df = pd.DataFrame({
        'Weeks': [week["week"] for week in data],
        'Easy Distance': [week["easy_distance"] * conversion for week in data],
        'Hard Distance': [week["hard_distance"] * conversion for week in data],
        'LT1 Distance': [week["lt1_distance"] * conversion for week in data],
        'LT2 Distance': [week["lt2_distance"] * conversion for week in data],
    })
    fig_bar = px.bar(bar_df, x="Weeks", y=y_axis)
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title=f"Distance {unit}", 
        legend_title="Run Types"
    )

    bar_chart = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    return bar_chart