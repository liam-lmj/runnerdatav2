from flask import Blueprint, render_template, session, redirect, request, jsonify

gear_bp = Blueprint("gear", __name__)

@gear_bp.route("/gear", methods=["GET", "POST"])
def weekly_view():
    if not "user_id" in session:
        return redirect("/")
    runner = session["user_id"]     

    return render_template("gear.html")