from flask import Blueprint, render_template, session, redirect, request, jsonify

gear_bp = Blueprint("gear", __name__)

@gear_bp.route("/gear", methods=["GET", "POST"])
def weekly_view():
    if not "user_id" in session:
        return redirect("/")
    runner = session["user_id"]     

    data = [{
        "gear_id": 1,
        "gear_name": "Tempus 2",
        "distance": 500,
        "default_type": "Easy",
        "active": "Active"
    }, 
    {
        "gear_id": 2,
        "gear_name": "Metaspeed",
        "distance": 100,
        "default_type": "Session",
        "active": "Active"
    }]
    return render_template("gear.html", data=data)