import sqlite3
import os
import json
import ast
from database.database_constants import distance_fields, meters_to_miles, meters_to_kilometers, activity_base_url, weeks_to_trend
from database.database_helper_functions import format_time_as_hours, format_time_as_minutes, format_pace
from database.database_classes.runner import Runner

def dict_factory(cursor, row): 
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def database_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'runner_data.db')
    return db_path

def get_all_existing_plans(runner, details):
    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory

    c = conn.cursor()
    c.execute("SELECT * FROM PLAN WHERE runner_id = ?", (runner,))
    plans = c.fetchall()
    conn.close  

    if details:
        return plans
    else:
        return [week.get("week") for week in plans]

def get_existing_plan_values(plan_week, runner, unit):
    if unit == "Miles":
        conversion = meters_to_miles
    elif unit == "Kilometers":
        conversion = meters_to_kilometers

    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory 

    c = conn.cursor()
    c.execute("SELECT * FROM PLAN WHERE week = ? AND runner_id = ?", (plan_week, runner))
    plan = c.fetchone()
    conn.close


    am_values = [round(value * conversion, 2) for value in json.loads((plan["am_values"]))]
    pm_values = [round(value * conversion, 2) for value in json.loads((plan["pm_values"]))]
    sessions = ast.literal_eval(plan["sessions"])
    session_count = len(sessions)

    return am_values, pm_values, session_count, sessions

def get_gear_data(runner, unit, active):
    sql = "SELECT * FROM GEAR WHERE runner_id = ?"
    params = [runner]
    if active != "All":
        sql += "AND active = ?"
        params.append(active)

    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute(sql, params)

    data = c.fetchall()
    conn.close()
    
    if unit == "Miles":
        conversion = meters_to_miles
    elif unit == "Kilometers":
        conversion = meters_to_kilometers
    
    for gear in data:
        gear["total_distance"] = round(gear["total_distance"] * conversion, 2)

    return data

def get_weekly_trend(runner, include_all_weeks):
    weeks_active, week = get_weeks_active(runner)

    if include_all_weeks:
        weeks_to_plot = weeks_active[:len(weeks_active)] 
    else:
        weeks_to_plot = weeks_active[:min(weeks_to_trend,len(weeks_active))]

    safe_placeholder = " ,".join("?" * len(weeks_to_plot))

    params = [runner] + weeks_to_plot

    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute(f"""
        SELECT 
            ACTIVITY.week,
            COUNT(DISTINCT ACTIVITY.activity_id) AS activity_count,
            COUNT(DISTINCT CASE 
                    WHEN NOT EXISTS (
                        SELECT 1 
                        FROM LAP AS L2
                        WHERE L2.activity_id = ACTIVITY.activity_id
                        AND L2.lap_type <> 'Easy'
                    ) THEN ACTIVITY.activity_id
                END) AS easy_activity_count,
            SUM(CASE WHEN LAP.lap_type = 'Easy' THEN LAP.lap_meters ELSE 0 END) AS easy_distance,
            SUM(CASE WHEN LAP.lap_type = 'LT1' THEN LAP.lap_meters ELSE 0 END) AS lt1_distance,
            SUM(CASE WHEN LAP.lap_type = 'LT2' THEN LAP.lap_meters ELSE 0 END) AS lt2_distance,
            SUM(CASE WHEN LAP.lap_type = 'Hard' THEN LAP.lap_meters ELSE 0 END) AS hard_distance,
            SUM(CASE WHEN LAP.lap_type = 'Easy' THEN LAP.lap_seconds ELSE 0 END) AS easy_seconds,
            SUM(CASE WHEN LAP.lap_type = 'LT1' THEN LAP.lap_seconds ELSE 0 END) AS lt1_seconds,
            SUM(CASE WHEN LAP.lap_type = 'LT2' THEN LAP.lap_seconds ELSE 0 END) AS lt2_seconds,
            SUM(CASE WHEN LAP.lap_type = 'Hard' THEN LAP.lap_seconds ELSE 0 END) AS hard_seconds,
            SUM(LAP.lap_meters) AS total_distance,
            SUM(LAP.lap_seconds) AS total_seconds
        FROM ACTIVITY
        INNER JOIN LAP ON ACTIVITY.activity_id = LAP.activity_id
        WHERE ACTIVITY.runner_id = ? AND ACTIVITY.week in ( {safe_placeholder} )
        GROUP BY ACTIVITY.week
        ORDER BY ACTIVITY.week
    """, params)

    data = c.fetchall()
    conn.close()
    return data

def get_runner(runner):
    db_path = database_path

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM RUNNER WHERE runner_id = ?", (runner,))
    runner = c.fetchone()
    conn.close

    return runner

def get_activity_plot(activity):
    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute("SELECT map_plot FROM ACTIVITY WHERE activity_id = ?", (activity,))
    data = c.fetchone()
    conn.close()
    plot = data["map_plot"]

    return(plot)

def get_lap_data(activity):
    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute("SELECT * FROM LAP WHERE activity_id = ?", (activity,))

    data = c.fetchall()
    conn.close()

    for lap in data:
        lap_pace = lap["lap_meters"] / lap["lap_seconds"]
        lap["lap_formatted_time"] = format_time_as_minutes(lap["lap_seconds"])
        lap["lap_cadence"] *= 2
        runner = Runner(lap["runner_id"])
        format_distances(runner, lap)
        lap["lap_pace"] = format_pace(runner.preferred_unit, lap_pace)

    return(data)

def get_week_data(week, runner):
    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute("""
        SELECT 
            ACTIVITY.activity_id,
            ACTIVITY.activity_date,
            ACTIVITY.week,
            ACTIVITY.day,
            ACTIVITY.heartrate_average,
            ACTIVITY.activity_meters,
            ACTIVITY.activity_seconds,
            substr(ACTIVITY.activity_date, 1, 10) AS formatted_date,
            GROUP_CONCAT(LAP.lap_type) AS run_type,
            SUM(CASE WHEN LAP.lap_type = 'Easy' THEN LAP.lap_meters ELSE 0 END) AS easy_distance,
            SUM(CASE WHEN LAP.lap_type = 'LT1' THEN LAP.lap_meters ELSE 0 END) AS lt1_distance,
            SUM(CASE WHEN LAP.lap_type = 'LT2' THEN LAP.lap_meters ELSE 0 END) AS lt2_distance,
            SUM(CASE WHEN LAP.lap_type = 'Hard' THEN LAP.lap_meters ELSE 0 END) AS hard_distance
        FROM ACTIVITY
        INNER JOIN LAP ON ACTIVITY.activity_id = LAP.activity_id
        WHERE ACTIVITY.week = ? AND ACTIVITY.runner_id = ?
        GROUP BY ACTIVITY.activity_id
        ORDER BY activity_date
    """, (week, runner))

    data = c.fetchall()
    conn.close()
    
    #clean up data
    for activity in data:
        run_types = set(activity["run_type"].split(","))
        if len(run_types) > 1 and "Easy" in run_types:
            run_types.remove("Easy") #run is not easy if it has any harder types
        activity["run_type"] = (", ").join(run_types)

        activity["run_description"] = f"{activity["day"]} {activity["run_type"]} Run"
        activity["formated_time"] = format_time_as_hours(activity["activity_seconds"])
        activity["activity_url"] = f"{activity_base_url}{activity["activity_id"]}"
        runner_obj = Runner(runner)
        format_distances(runner_obj, activity)

    return(data)

def get_weeks_active(runner):
    db_path = database_path()

    conn = sqlite3.connect(db_path)
    conn.row_factory = dict_factory 
    c = conn.cursor()
    c.execute("""
        SELECT DISTINCT week
        FROM ACTIVITY
        WHERE runner_id = ?
        ORDER BY activity_date DESC
    """, (runner,))

    data = c.fetchall()
    conn.close()
    
    weeks = [entry["week"] for entry in data]
    most_recent_week = weeks[0] if weeks else None
    return weeks, most_recent_week

def format_distances(runner, activity):
    units = runner.preferred_unit

    if units == "Miles":
        conversion = meters_to_miles
    elif units == "Kilometers":
        conversion = meters_to_kilometers

    for field in distance_fields:
        if activity.get(field):
            activity[field] = round(activity[field] * conversion, 2)