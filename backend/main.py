from flask import Flask
from datetime import datetime
from flask_restx import Api, Resource, fields
from database.db import db
from database.IncidentLogModel import IncidentLogModel



def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app, version="1.0", title="My API",
          description="Decoy app backend api")
    ns = api.namespace("IncidentLogs", description="IncidentLogs operations")

    incident_log_model = api.model("IncidentLog", {
        "id": fields.Integer(readonly=True),
        "title": fields.String(required=True, description="The incident title"),
        "category": fields.String(required=False, description="The incident category (network, hardware, software, other)"),
        "description": fields.String(required=False, description="The incident description"),
        "timestamp": fields.DateTime(required=False, description="The incident timestamp as unix timestamp"),
        "severity": fields.String(required=False, description="The incident severity (critical, moderate, low)"),
    })

    @ns.route("/")
    class IncidentLogList(Resource):
        @ns.marshal_list_with(incident_log_model)
        def get(self):
            return IncidentLogModel.query.all()

        @ns.expect(incident_log_model)
        @ns.marshal_with(incident_log_model, code=201)
        def post(self):
            data = api.payload
            try:
                if "timestamp" in data:
                    timestamp = datetime.fromtimestamp(int(data.get("timestamp")))
            except Exception as e:
                timestamp = datetime.utcnow()
            severity = data.get("severity")
            category = data.get("category")
            description = data.get("description")
            title = data.get("title")
            new_item = IncidentLogModel(title=title, timestamp=timestamp, severity=severity, category=category, description=description)
            db.session.add(new_item)
            db.session.commit()
            return new_item, 201

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
