#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import current_user
from app.models.agent import AgentModel
from app.util.encoder import AlchemyEncoder
from app.models.mission import MissionModel
import json
from app.util.fonction import getMonId
# from app.util.fonction import login_faciale
from app.util.logz import create_logger



class AgentLogin(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('code_name', type=str, required=True,
                        help='This field cannot be left blank')
    parser.add_argument('password', type=str, required=True,
                        help='This field cannot be left blank')
    

    def post(self):
        data = AgentLogin.parser.parse_args()
        code_name = data['code_name']
        password = data['password']

        agent = AgentModel.query.filter_by(code_name=code_name).one_or_none()
        if not agent or not agent.check_password(password):
            return json.dumps({'access_token': None}), 401
        access_token = create_access_token(

            identity=json.dumps(agent, cls=AlchemyEncoder), additional_claims={"roles": "admin"})
        return jsonify(access_token=access_token)

class AgentReconnaissance(Resource):
    def __init__(self):
        self.logger = create_logger()

    parser = reqparse.RequestParser()
    parser.add_argument('photo', type=str, required=True,
                        help='This field cannot be left blank')


    def post(self):
        # data = AgentReconnaissance.parser.parse_args() 
        # photo = data['photo']

        # users = AgentModel.query.all()
        # agent = login_faciale(users, photo)
        # if agent is None:
        #     return json.dumps({'access_token':None}), 401
        # else:
        #     access_token = create_access_token(
        #         identity=json.dumps(agent, cls=AlchemyEncoder), additional_claims={"roles": "admin"})
        #     return jsonify(access_token=access_token)
        return 0


class AgentList(Resource):
    def get(self):
        return {'agents': [agent.json() for agent in AgentModel.query.all()]}



class MissionByAgent(Resource):
    @jwt_required()
    def get(self):
        myid = getMonId()
        ag = AgentModel.find_by_id(myid)
        missions = MissionModel.query.all()
        mis = []
        for mission in missions:
            for agent in mission.agents:
                if agent.id == myid:
                    mis.append(mission)
                    break
        return {'missions': [mi.json() for mi in mis],'agent':ag.json()}, 200