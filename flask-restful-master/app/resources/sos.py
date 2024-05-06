from flask_restful import Resource, reqparse
from app.util.chat import sosText
from app.models.agent import AgentModel
from app.models.gadget import GadgetModel
from app.db import db
from flask import request
from io import BytesIO

class SOSText(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('texte', type=str, required=True, help='Le sos est requis')

    def post(self):
        data = SOSText.parser.parse_args()
        agents = AgentModel.query.all()
        gadgets = GadgetModel.query.all()
        mission, agens, gadgs = sosText(data['texte'], agents, gadgets)
        mission.save_to_db()
        for agent in agens:
            mission.agents.append(agent)
        
        for g in gadgs:
            mission.gadgets.append(g)

        db.session.commit()
        
        return {'message':'good'}, 200

class SOSVocal(Resource):

    def post(self):
        return {'message':'mauvais'}, 401

    