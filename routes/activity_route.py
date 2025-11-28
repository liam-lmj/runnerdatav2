from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_queries import get_lap_data, get_activity_plot
from database.database_helper_functions import map_html, lap_data_summary_fields, get_lap_types, filter_lap_data, format_unit

activity_bp = Blueprint("activity", __name__)

@activity_bp.route("/activity/<int:activity_id>", methods=["GET", "POST"])
def weekly_view(activity_id):
    if not "user_id" in session:
        return redirect("/")
    unit = format_unit(session["unit"])

    lap_data = get_lap_data(activity_id)
    activity_lap_types = get_lap_types(lap_data)

    if request.method == "POST" and request.json["type"] == "lap_change" and request.json["selected_type"] != "All":
        lap_data = filter_lap_data(lap_data, request.json["selected_type"])

    total_distance, formated_total_time, average_heartrate, cadence = lap_data_summary_fields(lap_data)
    plot = get_activity_plot(activity_id) 
    map = map_html(plot)



    if request.method == "POST" and request.json["type"] == "lap_change":
        return jsonify({"success": True, 
                        "updated_data": lap_data,
                        "total_distance": total_distance,
                        "formated_total_time": formated_total_time,
                        "average_heartrate": average_heartrate,
                        "cadence": cadence,
                        "unit": unit}) 
    
    return render_template("activity.html", 
                           map=map, 
                           lap_data=lap_data,
                           activity_lap_types=activity_lap_types,
                           total_distance=total_distance,
                           formated_total_time=formated_total_time,
                           average_heartrate=average_heartrate,
                           cadence=cadence,
                           unit=unit)
