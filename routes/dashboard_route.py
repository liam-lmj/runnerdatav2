from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_queries import get_weekly_trend
from database.database_plots import mileage_trend_bar, pace_trend_line

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard/", methods=["GET", "POST"])
def dashboard():
    if not "user_id" in session:
        return redirect("/")
    
    unit = session["unit"]
    runner = session["user_id"]
    
    weekly_data = get_weekly_trend(runner)

    mileage_trend_plot = mileage_trend_bar(weekly_data, unit, "All")
    pace_trend_plot = pace_trend_line(weekly_data, unit, "Easy Pace")

    if request.method == "POST":  
        request_json = request.json
        if request_json["type"] == "mileage_trend_change":
            updated_plot = mileage_trend_bar(weekly_data, unit, request_json["selected_type"])
        if request_json["type"] == "pace_trend_change":
            updated_plot = pace_trend_line(weekly_data, unit, request_json["selected_type"])

        return jsonify({"success": True, 
                        "plot": updated_plot})


    return render_template("dashboard.html",
                           mileage_trend_plot=mileage_trend_plot,
                           pace_trend_plot=pace_trend_plot)