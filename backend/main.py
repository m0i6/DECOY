from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version="1.0", title="My API",
          description="Decoy app backend api")

alerts = api.namespace("alerts", description="Alerts operations")

ITEMS = []

@alerts.route("/")
class AlertList(Resource):
    def get(self):
        """List all alerts"""
        return ITEMS

    def post(self):
        """Create a new alert"""
        item = {"id": len(ITEMS) + 1, "name": f"Alert {len(ITEMS)+1}"}
        ITEMS.append(item)
        return item, 201

@alerts.route("/<int:id>")
class Alert(Resource):
    def get(self, id):
        """Get an alert by ID"""
        for item in ITEMS:
            if item["id"] == id:
                return item
        api.abort(404, f"Alert {id} not found")

if __name__ == "__main__":
    app.run(debug=True)
