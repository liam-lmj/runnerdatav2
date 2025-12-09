from flask import Blueprint, render_template, session, redirect, request, jsonify

plan_bp = Blueprint("plan", __name__)

@plan_bp.route("/plan/", methods=["GET", "POST"])
def weekly_view():
    if not "user_id" in session:
        return redirect("/")
    unit = session["unit"]

    session_count = 0

    if request.method == "POST" and request.json["type"] == "session_change":
        return jsonify({"success": True,
                        "session_count": session_count}) 
    
    return render_template("plan.html",
                           unit=unit,
                           session_count=session_count)
