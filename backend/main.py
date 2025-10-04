from flask import Flask
from flask_restx import Api
from database.db import db
from database.models.IncidentLogModel import setup_routes as setup_incident_routes
from database.models.HoneyPotModel import setup_routes as setup_honeypot_routes



def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app, version="1.0", title="My API",
          description="Decoy app backend api")

    setup_incident_routes(api)
    setup_honeypot_routes(api)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
