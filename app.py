import os
from flask import Flask
from dotenv import load_dotenv
from routes.login_routes import login_bp
from routes.week_route import week_bp
from routes.activity_route import activity_bp
from routes.dashboard_route import dashboard_bp
from routes.gear_route import gear_bp
from routes.training_route import training_bp
from routes.plan_route import plan_bp


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("secret_key")

app.register_blueprint(login_bp)
app.register_blueprint(week_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(gear_bp)
app.register_blueprint(training_bp)
app.register_blueprint(plan_bp)


if __name__ == "__main__":
    app.run(debug=True)