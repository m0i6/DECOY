from database.db import db
from sqlalchemy.types import TypeDecorator, String
from flask_restx import Resource, fields
from datetime import datetime


class SeverityType(TypeDecorator):
    impl = String(20)

    def process_bind_param(self, value, dialect):
        allowed = {'critical', 'moderate', 'low'}
        if value is not None and value not in allowed:
            raise ValueError(f"Invalid severity: {value}")
        return value

    def process_result_value(self, value, dialect):
        return value

class IncidentLogModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=True, default='other')
    description = db.Column(db.String(200), nullable=True, default="No description provided")
    timestamp = db.Column(db.DateTime, nullable=True, default=db.func.current_timestamp())
    severity = db.Column(SeverityType, nullable=True, default='low')
    honeypot_id = db.Column(db.Integer, db.ForeignKey('honey_pot_model.id'), nullable=True)


    def __repr__(self):
        return f"<IncidentLog {self.title}>"
    
    @classmethod
    def json_schema(cls):
        schema = {}
        for column in cls.__table__.columns:
            col_type = type(column.type).__name__
            if col_type == "Integer":
                field = fields.Integer(readonly=column.primary_key)
            elif col_type == "String":
                field = fields.String(required=not column.nullable, description=f"The incident {column.name}")
            elif col_type == "DateTime":
                field = fields.DateTime(required=not column.nullable, description=f"The incident {column.name} as unix timestamp")
            else:
                field = fields.String(required=not column.nullable, description=f"The incident {column.name}")
            schema[column.name] = field
        return schema



def setup_routes(api):
    ns = api.namespace("IncidentLogs", description="IncidentLogs operations")

    incident_log_model = api.model("IncidentLog",  IncidentLogModel.json_schema())

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
            timestamp = datetime.utcnow()
            honeypot_id = data.get("honeypot_id")
            new_item = IncidentLogModel(title=title, timestamp=timestamp, severity=severity, category=category, description=description, honeypot_id=honeypot_id)
            db.session.add(new_item)
            db.session.commit()
            return new_item, 201

