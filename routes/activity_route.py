from flask import Blueprint, render_template, session, redirect, request, jsonify

activity_bp = Blueprint("activity", __name__)

@activity_bp.route("/activity/<int:activity_id>", methods=["GET", "POST"])
def weekly_view(activity_id):
    if not "user_id" in session:
        return redirect("/")
    runner = session["user_id"]     

    return render_template("activity.html")
