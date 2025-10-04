from database.db import db
from sqlalchemy.types import TypeDecorator, String
from flask_restx import fields, Resource
from datetime import datetime


class ServerCategoryType(TypeDecorator):
    impl = String(20)

    def process_bind_param(self, value, dialect):
        allowed = {'web', 'database', 'application', 'other'}
        if value is not None and value not in allowed:
            raise ValueError(f"Invalid server category: {value}")
        return value

    def process_result_value(self, value, dialect):
        return value



class HoneyPotModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    server_category = db.Column(ServerCategoryType, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    creation_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(20), nullable=False, default="open")
    geolocation = db.Column(db.String(100), nullable=True)

    @classmethod
    def json_schema(cls):
        return {
                "id": fields.Integer(readonly=True),
                "title": fields.String(required=True, description="The incident title"),
                "category": fields.String(required=False, description="The incident category (network, hardware, software, other)"),
                "description": fields.String(required=False, description="The incident description"),
                "timestamp": fields.DateTime(required=False, description="The incident timestamp as unix timestamp"),
                "severity": fields.String(required=False, description="The incident severity (critical, moderate, low)"),
                "geolocation": fields.String(required=False, description="The incident geolocation"),
            }

def setup_routes(api):
    ns = api.namespace("HoneyPots", description="HoneyPots operations")

    honey_pot_model = api.model("HoneyPot",  HoneyPotModel.json_schema())

    @ns.route("/")
    class HoneyPotList(Resource):
        @ns.marshal_list_with(honey_pot_model)
        def get(self):
            return HoneyPotModel.query.all()

        @ns.expect(honey_pot_model)
        @ns.marshal_with(honey_pot_model, code=201)
        def post(self):
            data = api.payload
            try:
                if "creation_date" in data:
                    creation_date = datetime.fromtimestamp(int(data.get("creation_date")))
            except Exception as e:
                creation_date = datetime.utcnow()
            status = data.get("status")
            server_category = data.get("server_category")
            description = data.get("description")
            name = data.get("name")
            new_item = HoneyPotModel(name=name, creation_date=creation_date, status=status, server_category=server_category, description=description)
            db.session.add(new_item)
            db.session.commit()
            return new_item, 201