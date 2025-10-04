from flask import Flask
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version="1.0", title="My API",
          description="A simple Flask API with Swagger UI")

ns = api.namespace("items", description="Items operations")

ITEMS = []

@ns.route("/")
class ItemList(Resource):
    def get(self):
        """List all items"""
        return ITEMS

    def post(self):
        """Create a new item"""
        item = {"id": len(ITEMS) + 1, "name": f"Item {len(ITEMS)+1}"}
        ITEMS.append(item)
        return item, 201

@ns.route("/<int:id>")
class Item(Resource):
    def get(self, id):
        """Get an item by ID"""
        for item in ITEMS:
            if item["id"] == id:
                return item
        api.abort(404, f"Item {id} not found")

if __name__ == "__main__":
    app.run(debug=True)
