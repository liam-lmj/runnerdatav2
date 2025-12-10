from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_plots import plan_bar
import numpy as np


plan_bp = Blueprint("plan", __name__)

@plan_bp.route("/plan/", methods=["GET", "POST"])
def weekly_view():
    if not "user_id" in session:
        return redirect("/")
    unit = session["unit"]

    session_count = 0
    run_count = 0

    if request.method == "POST" and request.json["type"] == "plan_chage":
        am_values = request.json["am_values"]
        pm_values = request.json["pm_values"]

        totals = [am_values[i] + pm_values[i] for i in range(0, len(am_values))]

        run_count = np.count_nonzero(am_values) + np.count_nonzero(pm_values)

        bar_chart = plan_bar(totals, unit)
        return jsonify({"success": True,
                        "totals": totals,
                        "bar_chart": bar_chart,
                        "total_distance": f"{round(sum(totals), 2)} {unit}",
                        "average_distance": f"{round(sum(totals) / len(totals), 2)} {unit}",
                        "run_count": str(run_count) }) 
    
    return render_template("plan.html",
                           unit=unit,
                           session_count=session_count,
                           run_count=run_count)
