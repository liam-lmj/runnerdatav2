from flask import Blueprint, render_template, session, redirect, request, jsonify

settings_bp = Blueprint("settings", __name__)
    
@settings_bp.route("/settings", methods=["GET", "POST"])
def settings():
    if not "user_id" in session:
        return redirect("/")
    runner = session["user_id"]  
    unit = session["unit"]

    if request.method == "POST" and request.json["type"] == "gear_change":
        pass

    if request.method == "POST":
        return jsonify({"success": True}) 

    return render_template("settings.html")

