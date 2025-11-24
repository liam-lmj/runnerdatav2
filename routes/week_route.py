from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_queries import get_week_data, get_weeks_active
from database.database_plots import weekly_mileage_type_pie
from database.database_helper_functions import format_time_as_hours

week_bp = Blueprint('week', __name__)

@week_bp.route("/week", methods=['GET', 'POST'])
def weekly_view():
    if not 'user_id' in session:
        return redirect("/")
    runner = session['user_id']     

    weeks_active, most_recent_week = get_weeks_active(runner)

    if request.method == "POST" and request.json["type"] == "week_change":
        week = request.json["selected_week"]
        data = get_week_data(week, runner)
    else:
        data = get_week_data(most_recent_week, runner)

    run_count = len(data)
    total_distance = sum(activity.get("activity_meters", 0) for activity in data)

    total_time_seconds = sum(activity.get("activity_seconds", 0) for activity in data)
    formated_total_time = format_time_as_hours(total_time_seconds)

    if total_time_seconds > 0:
        average_heartrate = round(sum(activity.get("activity_seconds", 0) * activity.get("heartrate_average", 0) for activity in data) / total_time_seconds, 2)
    else:
        average_heartrate = 0
    
    pie_chart = weekly_mileage_type_pie(data)

    if request.method == "POST" and request.json["type"] == "week_change":
        return jsonify({"success": True, 
                        "pie_chart": pie_chart,
                        "run_count": run_count,
                        "average_heartrate": average_heartrate,
                        "total_distance": total_distance,
                        "formated_total_time": formated_total_time,
                        "updated_data": data}) 

    return render_template("week.html",
                           weeks_active=weeks_active,
                           data=data,
                           run_count = run_count,
                           total_distance=total_distance,
                           formated_total_time=formated_total_time,
                           average_heartrate=average_heartrate,
                           pie_chart=pie_chart)