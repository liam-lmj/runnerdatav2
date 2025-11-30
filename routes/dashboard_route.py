from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_queries import get_weekly_trend, get_weeks_active
from database.database_plots import mileage_trend_bar, pace_trend_line, time_pie_chart, session_trend_bar
from database.database_helper_functions import format_time_as_hours, distance_conversion
from datetime import date

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/", methods=["GET", "POST"])
def dashboard():
    if not "user_id" in session:
        return redirect("/")
    
    unit = session["unit"]
    runner = session["user_id"]
    
    weeks_active, week = get_weeks_active(runner)

    weekly_data = get_weekly_trend(runner, False)

    if request.method == "GET":  
        all_data = get_weekly_trend(runner, True)
        current_year = str(__import__('datetime').datetime.now().year)

        yearly_activity_count = sum(week_dict.get("activity_count", 0) 
                                    for week_dict in all_data 
                                    if week_dict.get("week", 0).split("-")[1] == current_year) #week format is mm-yyyy
        
        yearly_session_count = sum(week_dict.get("activity_count", 0) - week_dict.get("easy_activity_count", 0) 
                                   for week_dict in all_data
                                   if week_dict.get("week", 0).split("-")[1] == current_year)
        
        yearly_distance = round(distance_conversion(unit) * sum(week_dict.get("total_distance", 0) - week_dict.get("easy_activity_count", 0) 
                            for week_dict in all_data
                            if week_dict.get("week", 0).split("-")[1] == current_year), 2)

        yearly_hours = format_time_as_hours(sum(week_dict.get("total_seconds", 0) - week_dict.get("easy_activity_count", 0) 
                                   for week_dict in all_data
                                   if week_dict.get("week", 0).split("-")[1] == current_year))

    mileage_trend_plot = mileage_trend_bar(weekly_data, unit, "All")
    pace_trend_plot = pace_trend_line(weekly_data, unit, "Easy Pace")
    time_plot = time_pie_chart(weekly_data, "All")
    run_count_plot = session_trend_bar(weekly_data, "All")

    if request.method == "POST":  
        request_json = request.json
        if request_json["type"] == "mileage_trend_change":
            updated_plot = mileage_trend_bar(weekly_data, unit, request_json["selected_type"])

        elif request_json["type"] == "pace_trend_change":
            updated_plot = pace_trend_line(weekly_data, unit, request_json["selected_type"])

        elif request_json["type"] == "pie_time_change":
            updated_plot = time_pie_chart(weekly_data, request_json["selected_type"])

        elif request_json["type"] == "bar_count_change":
            updated_plot = session_trend_bar(weekly_data, request_json["selected_type"])

        return jsonify({"success": True, 
                        "plot": updated_plot})

    return render_template("dashboard.html",
                           weeks_active=weeks_active,
                           mileage_trend_plot=mileage_trend_plot,
                           pace_trend_plot=pace_trend_plot,
                           time_plot=time_plot,
                           run_count_plot=run_count_plot,
                           yearly_session_count=yearly_session_count,
                           yearly_activity_count=yearly_activity_count,
                           yearly_distance=yearly_distance,
                           yearly_hours=yearly_hours,
                           unit=unit)