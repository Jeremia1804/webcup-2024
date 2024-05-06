from app.db import db
from werkzeug.security import hmac
from app.associate import mission_agent
from app.models.mission import MissionModel

agent_specialite = db.Table('agent_specialite',
    db.Column('agent_id', db.Integer, db.ForeignKey('agents.id'), primary_key=True),
    db.Column('specialite_id', db.Integer, db.ForeignKey('specialites.id'), primary_key=True)
)


class AgentModel(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(10)) 
    nom = db.Column(db.String(30))
    prenom = db.Column(db.String(30))
    password = db.Column(db.String(80))
    photo = db.Column(db.String(80))
    contact = db.Column(db.String(80))
    rang = db.Column(db.Integer)

    specialites = db.relationship('SpecialiteModel', secondary=agent_specialite, backref='agents')

    def __init__(self, nom, prenom, code_name, password, contact, rang,photo):
        self.nom = nom
        self.prenom = prenom
        self.code_name = code_name
        self.contact = contact
        self.password = password
        self.rang = rang
        self.photo = photo

    def json(self):
        return {
            'id':self.id,
            'code_name':self.code_name,
            'nom':self.nom,
            'prenom':self.prenom,
            'photo':self.photo,
            'contact':self.contact,
            'specialites':[sp.json() for sp in self.specialites],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def get_my_mission(self):
        missions = MissionModel.query.all()
        mis = []
        for mission in missions:
            for agent in mission.agents:
                if agent.id == self.id:
                    mis.append(mission)
                    break
        return mis



    def check_password(self, password):
        return hmac.compare_digest(self.password, password)

    @classmethod
    def find_by_code(cls, code_name):
        return cls.query.filter_by(code_name=code_name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

