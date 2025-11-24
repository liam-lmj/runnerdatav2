from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_queries import get_lap_data, get_activity_plot
from database.database_helper_functions import map_html

activity_bp = Blueprint("activity", __name__)

@activity_bp.route("/activity/<int:activity_id>", methods=["GET", "POST"])
def weekly_view(activity_id):
    if not "user_id" in session:
        return redirect("/")
    runner = session["user_id"]

    lap_data = get_lap_data(activity_id)
    plot = get_activity_plot(activity_id) 
    map = map_html(plot)
    return render_template("activity.html", map=map, lap_data=lap_data)
