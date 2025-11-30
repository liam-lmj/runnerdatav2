import json
import plotly
import plotly.express as px
import pandas as pd
from database.database_constants import lap_types, meters_to_miles, meters_to_kilometers, mileage_trend_axis, formatted_lap_types, y_axis_label_count
from database.database_helper_functions import format_pace
import math

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

def pace_trend_line(data, distance_unit, pace_type):
    line_df = pd.DataFrame({
        'Weeks': [week["week"] for week in data],
        'Easy Pace': [week["easy_distance"] / week["easy_seconds"]
                      if week["easy_seconds"] > 0 
                      else None 
                      for week in data],
        'Hard Pace': [week["hard_distance"] / week["hard_seconds"]
                      if week["hard_seconds"] > 0 
                      else None 
                      for week in data],
        'LT1 Pace': [week["lt1_distance"] / week["lt1_seconds"]
                      if week["lt1_seconds"] > 0 
                      else None 
                      for week in data],
        'LT2 Pace': [week["lt2_distance"] / week["lt2_seconds"]
                      if week["lt2_seconds"] > 0 
                      else None 
                      for week in data]
    })

    y_axis = line_df[pace_type]

    ticktexts = [format_pace(distance_unit, pace) for pace in y_axis]

    clean_y_axis_values = list(filter(lambda x: not (isinstance(x, float) and math.isnan(x)) , y_axis)) # for computing ranges etc - main ticktext needs none for plotting

    fig_line = px.line(line_df, x="Weeks", y=y_axis)

    fig_line.update_traces(mode='markers+lines',
                           connectgaps=True)

    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(
            range=[min(clean_y_axis_values), max(clean_y_axis_values)],   
            tickvals=y_axis,
            ticktext=ticktexts,
            title=dict(
                text="Pace",
                standoff=55 
            ),            
            showticklabels=False
            )
    )

    y_annotation(fig_line, clean_y_axis_values, distance_unit)

    line_chart = json.dumps(fig_line, cls=plotly.utils.PlotlyJSONEncoder)
    return line_chart

def y_annotation(fig, y_axis, distance_unit):
    gap = max(y_axis) - min(y_axis)
    values = [min(y_axis) + i * (gap / (y_axis_label_count - 1)) for i in range(y_axis_label_count)]
    values_formatted = [format_pace(distance_unit, value) for value in values]

    for i in range(y_axis_label_count):      
        fig.add_annotation(
            xref="paper", yref="y",
            x=0, y=values[i],
            text=values_formatted[i],
            showarrow=False,
            xanchor="right",
            align="right"
        )