from flask import Blueprint, render_template, session, redirect, request, jsonify
from database.database_queries import get_gear_data
from database.database_classes.gear import Gear
from database.database_helper_functions import try_decimal

gear_bp = Blueprint("gear", __name__)
    
@gear_bp.route("/gear", methods=["GET", "POST"])
def weekly_view():
    if not "user_id" in session:
        return redirect("/")
    runner = session["user_id"]     

    if request.method == "POST" and request.json["type"] == "gear_change":
        if try_decimal(request.json["total_distance"]) or try_decimal(request.json["total_distance"]) == 0:
            print("class called")
            gear = Gear(request.json["id"],
                        request.json["active"],
                        request.json["default_type"],
                        request.json["shoe"],
                        request.json["total_distance"],
                        runner)

    data = get_gear_data(runner)

    if request.method == "POST" and request.json["type"] == "gear_change":
        return jsonify({"success": True, 
                        "updated_data": data}) 

    return render_template("gear.html", data=data)

