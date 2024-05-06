from flask_restful import Resource, reqparse
from app.models.gadget import GadgetModel
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger

class Gadget(Resource):
    parser = reqparse.RequestParser()  # only allow price changes, no name changes allowed
    parser.add_argument('name', type=str, required=True,
                        help='This field cannot be left blank name')
    parser.add_argument('puissance', type=float, required=True,
                        help='This field cannot be left blank puissance')


    def __init__(self):
        self.logger = create_logger()

    def get(self, name):
        gadget = GadgetModel.find_by_name(name)
        if gadget:
            return gadget.json()
        return {'message': 'Gadget not found'}, 404

    @jwt_required()  # Requires JWT token
    def post(self):
        data = Gadget.parser.parse_args()
        name = data['name']
        puissance = data['puissance']

        if GadgetModel.find_by_name(name):
            return {'message': "A gadget with name '{}' already exists.".format(name)}, 400

        gadget = GadgetModel(name, puissance)
        try:
            gadget.save_to_db()
        except:
            return {"message": "An error occurred creating the gadget."}, 500

        return gadget.json(), 201

    @jwt_required()  # Requires JWT token
    def delete(self, name):
        gadget = GadgetModel.find_by_name(name)
        if gadget:
            gadget.delete_from_db()

        return {'message': 'Gadget deleted'}

class GadgetList(Resource):
    def get(self):
        return {'gadgets': [gadget.json() for gadget in GadgetModel.query.all()]}
