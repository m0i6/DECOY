from flask_sqlalchemy import SQLAlchemy
from database.db import db
from sqlalchemy.types import TypeDecorator, String


class SeverityType(TypeDecorator):
    impl = String(20)

    def process_bind_param(self, value, dialect):
        allowed = {'critical', 'moderate', 'low'}
        if value is not None and value not in allowed:
            raise ValueError(f"Invalid severity: {value}")
        return value

    def process_result_value(self, value, dialect):
        return value

class CategoryType(TypeDecorator):
    impl = String(20)

    def process_bind_param(self, value, dialect):
        allowed = {'network', 'hardware', 'software', 'other'}
        if value is not None and value not in allowed:
            raise ValueError(f"Invalid category: {value}")
        return value

    def process_result_value(self, value, dialect):
        return value




class IncidentLogModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    category = db.Column(CategoryType, nullable=True)
    description = db.Column(db.String(200), nullable=True)
    timestamp = db.Column(db.DateTime, nullable=True)
    severity = db.Column(SeverityType, nullable=True)


    def __repr__(self):
        return f"<IncidentLog {self.title}>"
