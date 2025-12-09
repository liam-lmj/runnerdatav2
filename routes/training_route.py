from flask import Blueprint, render_template, session, redirect, request, jsonify

training_bp = Blueprint("training", __name__)

@training_bp.route("/training/", methods=["GET", "POST"])
def weekly_view():
    if not "user_id" in session:
        return redirect("/")
    unit = session["unit"]

    if request.method == "POST" and request.json["type"] == "lap_change":
        return jsonify({"success": True}) 
    
    return render_template("training.html",
                           unit=unit)
