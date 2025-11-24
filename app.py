import os
from flask import Flask
from dotenv import load_dotenv
from routes.login_routes import login_bp
from routes.week_route import week_bp

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("secret_key")

app.register_blueprint(login_bp)
app.register_blueprint(week_bp)

if __name__ == "__main__":
    app.run(debug=True)