from database.database_constants import seconds_to_hours, seconds_to_minutes, units_dict, pace_conversion_dict, meters_to_miles, meters_to_kilometers, new_plan_values
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta
import polyline
import folium
import math
import ast

def try_decimal(value):
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return False

def filter_training_hub_data(data, filter):
    if filter == "All":
        return data
    
    output = []
    if filter == "Pending":
        for plan in data:
            if plan["outcome"] == "Pending":
                output.append(plan)
    else:
        for plan in data:
            if plan["outcome"] != "Pending":
                output.append(plan)

    return output

def format_training_hub_data(plans, weeks, unit):
    date = datetime.now()
    current_week_year = date.strftime("%W-%Y")
    current_week, current_year = [part for part in current_week_year.split("-")]

    conversion = distance_conversion(unit)

    upcoming_plans = 0
    upcoming_distance = 0

    complete_plans = 0
    successful_plans = 0

    for plan in plans:
        plan_week_year = plan.get("week","99-9999")
        plan_week, plan_year = [part for part in plan_week_year.split("-")]
        pending = (current_year, current_week) < (plan_year, plan_week)

        am_values = ast.literal_eval(plan.get("am_values"))
        pm_values = ast.literal_eval(plan.get("pm_values"))
        total_distance = sum(am_values) + sum(pm_values)

        sessions = ast.literal_eval(plan.get("sessions"))
        session_count = len(sessions)

        plan["converted_distance"] = round(conversion * total_distance, 2)
        plan["formatted_distance"] = f"{plan["converted_distance"]} {format_unit(unit)}"
        plan["session_types"] = (", ").join(set([session.get("session_type", "") for session in sessions]))

        if pending:
            outcome = "Pending"
            upcoming_distance += plan["converted_distance"]
            upcoming_plans += 1
        else:
            real_week = None
            for week in weeks:
                week_year = week.get("week", "99-999")
                if week_year == plan_week_year:
                    real_week = week
                    break
            if real_week:
                complete_plans += 1
                real_session_count = real_week.get("activity_count") - real_week.get("easy_activity_count")
                real_distance = real_week.get("total_distance")

                if real_session_count >= session_count and real_distance >= total_distance:
                    outcome = "Success"
                    successful_plans += 1
                else:
                    outcome = "Failed"

        plan["outcome"] = outcome

    ordered_plans = sorted(plans, key=lambda d: (d["week"].split("-")[1], d["week"].split("-")[0])) #format ww-yyyy 

    return round(upcoming_plans, 2), round(upcoming_distance, 2), complete_plans, successful_plans, ordered_plans

def next_five_weeks_plan(existing_plans):
    next_five_weeks = []
    i = 0
    date = datetime.now()

    while i < 5:
        date += timedelta(days=7)
        week_year = date.strftime("%W-%Y")

        if not week_year in existing_plans:
            next_five_weeks.append(week_year)
            i += 1

    return next_five_weeks


def set_inital_plan_values():
    am_values = new_plan_values.get("am_values")
    pm_values = new_plan_values.get("pm_values")
    session_count = new_plan_values.get("session_count")
    sessions = new_plan_values.get("sessions")

    return am_values, pm_values, session_count, sessions

def lap_data_summary_fields(data):
    total_time = sum(lap.get("lap_seconds", 0) for lap in data)
    formated_total_time = format_time_as_hours(total_time)

    total_distance = sum(lap.get("lap_meters", 0) for lap in data)

    if total_time > 0:
        average_heartrate = round(sum((lap.get("lap_seconds") * lap.get("lap_heartrate_average")) for lap in data) / total_time, 2)
        cadence = round(sum((lap.get("lap_seconds") * lap.get("lap_cadence")) for lap in data) / total_time, 2)
    else:
        average_heartrate = 0
        cadence = 0
    return total_distance, formated_total_time, average_heartrate, cadence
    
def get_lap_types(data):
    return {lap.get("lap_type") for lap in data}

def filter_lap_data(data, lap_type):
    filtered_data = []
    for lap in data:
        if lap.get("lap_type") == lap_type:
            filtered_data.append(lap)
    return filtered_data

def format_time_as_hours(total_seconds):
    total_hours = total_seconds * seconds_to_hours
    formatted_time = f"{int(total_hours)}h {round(60 * (total_hours - int(total_hours))):02d}m"
    return formatted_time

def format_time_as_minutes(total_seconds):
    total_hours = total_seconds * seconds_to_minutes
    formatted_time = f"{int(total_hours)}m {round(60 * (total_hours - int(total_hours))):02d}s"
    return formatted_time

def map_html(plot):
    coords = polyline.decode(plot)
    map = folium.Map(location=coords[0], zoom_start=15)
    folium.PolyLine(coords, weight=5).add_to(map)
    map.fit_bounds([min(coords, key=lambda x: x[0]),
              max(coords, key=lambda x: x[0])])
    map_html = map._repr_html_()
    return map_html

def format_unit(unit):
    return  units_dict.get(unit)

def format_pace(unit, lap_pace):
    if not lap_pace or (isinstance(lap_pace, float) and math.isnan(lap_pace)):
        return None
    conversion = pace_conversion_dict.get(unit, 1)
    converted_lap_pace = conversion / lap_pace
    formatted_lap_pace = f"{int(converted_lap_pace)}:{round(60 * (converted_lap_pace - int(converted_lap_pace))):02d} /{format_unit(unit)}"
    return formatted_lap_pace

def distance_conversion(unit):
    if unit == "Miles":
        conversion = meters_to_miles
    elif unit == "Kilometers":
        conversion = meters_to_kilometers
    return conversion