from flask import Blueprint, render_template, session, redirect, request, jsonify, url_for
from database.database_plots import plan_bar
from database.database_helper_functions import set_inital_plan_values
import numpy as np


plan_bp = Blueprint("plan", __name__)

@plan_bp.route("/plan/<string:plan>", methods=["GET", "POST"])
def weekly_view(plan):
    if not "user_id" in session:
        return redirect("/")
    unit = session["unit"]

    if plan == "new":
        am_values, pm_values, session_count, sessions = set_inital_plan_values()

    total_values = [am_values[i] + pm_values[i] for i in range(0, len(am_values))]
    run_count = np.count_nonzero(am_values) + np.count_nonzero(pm_values)

    bar_chart = plan_bar(total_values, unit)

    if request.method == "POST" and request.json["type"] == "plan_change":
        am_values = request.json["am_values"]
        pm_values = request.json["pm_values"]

        total_values = [am_values[i] + pm_values[i] for i in range(0, len(am_values))]

        run_count = np.count_nonzero(am_values) + np.count_nonzero(pm_values)

        updated_bar_chart = plan_bar(total_values, unit)

        return jsonify({"success": True,
                        "totals": total_values,
                        "updated_bar_chart": updated_bar_chart,
                        "total_distance": f"{round(sum(total_values), 2)} {unit}",
                        "average_distance": f"{round(sum(total_values) / len(total_values), 2)} {unit}",
                        "run_count": str(run_count) }) 
    
    if request.method == "POST" and request.json["type"] == "plan_save":
        return jsonify({"success": True, "redirect": url_for("training.training")})
    
    return render_template("plan.html",
                           unit=unit,
                           session_count=session_count,
                           run_count=run_count,
                           bar_chart=bar_chart,
                           am_values=am_values,
                           pm_values=pm_values,
                           total_distance=f"{round(sum(total_values), 2)} {unit}",
                           average_distance=f"{round(sum(total_values) / len(total_values), 2)} {unit}",
                           sessions=sessions)
