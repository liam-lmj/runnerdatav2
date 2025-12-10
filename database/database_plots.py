import json
import plotly
import plotly.express as px
import pandas as pd
from database.database_constants import lap_types, mileage_trend_axis, formatted_lap_types, y_axis_label_count, lap_types_seconds, all_run_types, day_map
from database.database_helper_functions import format_pace, format_time_as_hours, distance_conversion
import math

def plan_bar(totals, unit):
    bar_df = pd.DataFrame({
        'Day': list(day_map.values()),
        'Distance': totals
    })

    fig_bar = px.bar(bar_df, x="Day", y="Distance", color="Day")
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title=f"Distance {unit}", 
    )

    bar_chart = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    return bar_chart

def gear_pie(data):
    pie_df = pd.DataFrame({
        'Trainer': [gear["gear_name"] for gear in data],
        'Distance': [gear["total_distance"] for gear in data]
    })
    fig_pie = px.pie(pie_df, names="Trainer", values="Distance")
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    pie_chart = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    return pie_chart   

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
    conversion = distance_conversion(unit)

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

def time_pie_chart(data, week):
    if week != "All":
        data = [week_dict for week_dict in data if week_dict.get("week") == week]

    pie_df = pd.DataFrame({
        'Types': ['Easy Time', 'LT1 Time', 'LT2 Time', 'Hard Time'],
        'Time': [sum(week.get(lap_types_seconds, 0) for week in data) for lap_types_seconds in lap_types_seconds]
    })

    fig_pie = px.pie(pie_df, names="Types", values="Time")
    fig_pie.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig_pie.update_traces(
        hovertemplate=[format_time_as_hours(time) for time in pie_df['Time']],
        hoverlabel=dict(
                            font_size=20,
                            font_family="Arial",
                            bgcolor="lightyellow"
                        )
        )

    pie_chart = json.dumps(fig_pie, cls=plotly.utils.PlotlyJSONEncoder)
    return pie_chart 

def session_trend_bar(data, activity_type):
    if activity_type == "All":
        y_axis = all_run_types
    else:
        y_axis = [activity_type]

    bar_df = pd.DataFrame({
        'Weeks': [week["week"] for week in data],
        'Run Count': [week["activity_count"] for week in data],
        'Easy Run Count': [week["easy_activity_count"] for week in data],
        'Session Count': [week["activity_count"] - week["easy_activity_count"] for week in data]
    })

    fig_bar = px.bar(bar_df, x="Weeks", y=y_axis)
    
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis_title=f"Distance", 
        legend_title="Run Types"
    )

    bar_chart = json.dumps(fig_bar, cls=plotly.utils.PlotlyJSONEncoder)
    return bar_chart


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