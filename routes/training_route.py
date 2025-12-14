from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_queries import get_all_existing_plans, get_weekly_trend
from database.database_helper_functions import format_training_hub_data, filter_training_hub_data
from database.database_constants import plan_base_url
from database.database_plots import training_bar

training_bp = Blueprint("training", __name__)

#TODO make mi/ miles consitent accross pages 
#TODO bar chart

@training_bp.route("/training/", methods=["GET", "POST"])
def training():
    if not "user_id" in session:
        return redirect("/")
    unit = session["unit"]
    runner = session["user_id"]

    plans = get_all_existing_plans(runner, True)
    weeks = get_weekly_trend(runner, True)
    
    upcoming_plans, upcoming_distance, complete_plans, successful_plans, training_hub_data = format_training_hub_data(plans, weeks, unit)

    filtered_training_hub_data = filter_training_hub_data(training_hub_data, "Pending")

    bar_chart = training_bar(filtered_training_hub_data, unit)

    if upcoming_plans > 0:
        average_distance = round(upcoming_distance / upcoming_plans, 2)
    else:
        average_distance = 0

    if complete_plans > 0:
        success_rate = round(100 * (successful_plans / complete_plans), 2)
    else:
        success_rate = 0
    
    if request.method == "POST" and request.json["type"] == "training_change":
        updated_data = filter_training_hub_data(training_hub_data, request.json["selected_type"])
        bar_chart = training_bar(updated_data, unit)
        return jsonify({"success": True,
                        "updated_data": updated_data,
                        "bar_chart": bar_chart}) 
    
    return render_template("training.html",
                           unit=unit,
                           upcoming_plans=upcoming_plans,
                           upcoming_distance=upcoming_distance,
                           success_rate=success_rate,
                           average_distance=average_distance,
                           training_hub_data=filtered_training_hub_data,
                           plan_base_url=plan_base_url,
                           bar_chart=bar_chart)
