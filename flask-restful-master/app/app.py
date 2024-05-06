from flask import Flask, jsonify,redirect,url_for,request,send_file,g
from flask_jwt_extended import JWTManager
from flask_restful import Api, Resource
from flask_cors import CORS


from app.resources.agent import AgentLogin, AgentReconnaissance, AgentList, MissionByAgent
from app.resources.gadget import Gadget, GadgetList
from app.resources.specialite import Specialite, SpecialiteList
from app.resources.mission import Mission, MissionList, MissionGadget, MissionAgent
from app.resources.sos import SOSText, SOSVocal

from app.config import postgresqlConfig,mssqlConfig,mysqlConfig

print(__name__)
# app = Flask(__name__, static_folder='static')
app = Flask(__name__, static_folder='build', static_url_path='/')

CORS(app)

app.config['UPLOAD_FOLDER'] = 'uploads'

#About database
app.config['SQLALCHEMY_DATABASE_URI'] = postgresqlConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "Dese.Decent.Pups.BOOYO0OST"  # Change this!
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)
api = Api(app)

#Create all table before first request
# @app.before_first_request
def create_tables():
    from app.db import db
    db.init_app(app)
    db.create_all()

with app.app_context():
    app.before_request_funcs = [(None, create_tables())]
    pass

# jwt = JWT(app, authenticate, identity)  # Auto Creates /auth endpoint

#Route
api.add_resource(AgentLogin, '/auth/login/s')
api.add_resource(AgentReconnaissance, '/auth/login/f')
api.add_resource(Gadget,'/gadget', '/gadget/<string:name>')
api.add_resource(GadgetList, '/gadgets')
api.add_resource(Specialite, '/specialite','/specialite/<string:libelle>')
api.add_resource(SpecialiteList, '/specialites')
api.add_resource(Mission,'/mission', '/mission/<string:mission_id>')
api.add_resource(MissionList, '/missions')
api.add_resource(MissionGadget, '/miss_gadg')
api.add_resource(MissionAgent, '/miss_agent')
api.add_resource(SOSText, '/sos/txt')
api.add_resource(SOSVocal, '/sos/vo')
api.add_resource(AgentList, '/agents')
api.add_resource(MissionByAgent, '/mymission')

@app.errorhandler(404)
def page_not_found(e):
    return send_file('build/index.html')

@app.errorhandler(500)
def handle_internal_error(e):
    response = jsonify(error="Internal Server Error")
    response.status_code = 500
    return {'error':'Internal Server Error'}, 500


if __name__ == '__main__':
    # TODO: Add swagger integration
    app.run(host='0.0.0.0', port='5000', debug=True)  # important to mention debug=True
