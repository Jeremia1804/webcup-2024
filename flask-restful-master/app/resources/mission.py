from flask_restful import Resource, reqparse
from app.models.mission import MissionModel
from app.models.gadget import GadgetModel
from app.models.agent import AgentModel
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger
from app.db import db

class Mission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('titre', type=str, required=True, help='Le titre de la mission est requis.')
    parser.add_argument('description', type=str, required=True, help='La description de la mission est requise.')
    parser.add_argument('datedebut', type=str, required=True, help='La date de début de la mission est requise.')
    parser.add_argument('datefin', type=str, required=True, help='La date de fin de la mission est requise.')
    parser.add_argument('niveaudurgence', type=float, required=True, help='Le niveau d\'urgence de la mission est requis.')
    parser.add_argument('lieu', type=str, required=True, help='Le lieu de la mission est requis.')

    def __init__(self):
        self.logger = create_logger()

    def get(self, mission_id):
        mission = MissionModel.find_by_id(mission_id)
        if mission:
            return mission.json()
        return {'message': 'Mission not found'}, 404

    @jwt_required()  # Requiert un token JWT
    def post(self):
        data = Mission.parser.parse_args()
        titre = data['titre']
        description = data['description']
        datedebut = data['datedebut']
        datefin = data['datefin']
        niveaudurgence = data['niveaudurgence']
        lieu = data['lieu']

        if MissionModel.find_by_titre(titre):
            return {'message': f"Une mission avec le titre '{titre}' existe déjà."}, 400

        mission = MissionModel(titre, description, datedebut, datefin, niveaudurgence, lieu)
        try:
            mission.save_to_db()
        except:
            return {"message": "Une erreur est survenue lors de la création de la mission."}, 500

        return mission.json(), 201

    @jwt_required()  # Requiert un token JWT
    def delete(self, mission_id):
        mission = MissionModel.find_by_id(mission_id)
        if mission:
            mission.delete_from_db()

        return {'message': 'Mission supprimée'}

class MissionList(Resource):
    def get(self):
        return {'missions': [mission.json() for mission in MissionModel.query.all()]}

class MissionGadget(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mission_id', type=int, required=True, help='Le titre de la mission est requis.')
    parser.add_argument('gadget_id', type=int, required=True, help='Le titre de la mission est requis.')

    def post(self):
        data = MissionGadget.parser.parse_args()
        mission_id = data['mission_id']
        gadget_id = data['gadget_id']
        mission = MissionModel.find_by_id(mission_id)
        gadget = GadgetModel.find_by_id(gadget_id)
        mission.gadgets.append(gadget)
        db.session.commit()
        return {'message':'Create finished successfuly'}, 200


class MissionAgent(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('mission_id', type=int, required=True, help='Le titre de la mission est requis.')
    parser.add_argument('agent_id', type=int, required=True, help='Le titre de la mission est requis.')

    def post(self):
        data = MissionAgent.parser.parse_args()
        mission_id = data['mission_id']
        agent_id = data['agent_id']
        mission = MissionModel.find_by_id(mission_id)
        agent = AgentModel.find_by_id(agent_id)
        mission.agents.append(agent)
        db.session.commit()
        return {'message':'Create finished successfuly'}, 200