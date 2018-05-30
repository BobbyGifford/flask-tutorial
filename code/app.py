from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'boots'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    # Filters req body to only take in 'price'. Strips all others
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be blank")

    @jwt_required()
    def get(self, name):
        for x in items:
            if x["name"] == name:
                return {'item': x}, 200 if x is not None else 404
            else:
                return {'message': "Sorry {} does not exist".format(name)}

    def post(self, name):
        for x in items:
            if x["name"] == name:
                return {'message': "Sorry {} already exists.".format(name)}

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        for x in items:
            if x["name"] == name:
                items.remove(x)
        return {'message': "item deleted"}

    def put(self, name):
        item = None

        data = Item.parser.parse_args()

        for x in items:
            if x["name"] == name:
                item = x

        if item is None:
            item = {'name': name, 'price': data["price"]}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


@app.route('/')
def hello_world():
    return 'Hello World!'


app.run(debug=True)
