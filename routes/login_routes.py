from flask import Blueprint, render_template, redirect, request, session
from app_constants import auth_url
from database.stravaapi import load_runner, new_access_token, update_activities, get_additional_session_attributes
from database.database_classes.runner import Runner

login_bp = Blueprint("login", __name__)

@login_bp.route("/")
def authorise():
    return render_template("authorise.html", auth_url=auth_url)

@login_bp.route("/loaduser")
def loaduser():
    code = request.args.get("code")
    refresh_token, runner_id = load_runner(code)
    session["user_id"] = runner_id

    runner = Runner(runner_id)
    session["unit"] = runner.preferred_unit


    access_token = new_access_token(refresh_token)
    update_activities(access_token)

    name, photo = get_additional_session_attributes(access_token)
    session["user_name"] = name
    session["photo"] = photo

    return redirect("/dashboard")
