from app.db import db
from app.associate import mission_agent

mission_gadget = db.Table('mission_gadget',
    db.Column('mission_id', db.Integer, db.ForeignKey('missions.id'), primary_key=True),
    db.Column('gadget_id', db.Integer, db.ForeignKey('gadgets.id'), primary_key=True)
)

# mission_agent = db.Table('mission_agent',
#     db.Column('mission_id', db.Integer, db.ForeignKey('missions.id'), primary_key=True),
#     db.Column('agent_id', db.Integer, db.ForeignKey('agents.id'), primary_key=True)
# )


class MissionModel(db.Model):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(80))
    description = db.Column(db.Text)
    datedebut = db.Column(db.Date)
    datefin = db.Column(db.Date)
    niveaudurgence = db.Column(db.Float(precision=2))
    lieu = db.Column(db.String(100))

    gadgets = db.relationship('GadgetModel', secondary=mission_gadget, backref='missions')
    agents = db.relationship('AgentModel', secondary=mission_agent, backref='missions')

    def __init__(self, titre, description, datedebut, datefin, niveaudurgence, lieu):
        self.titre = titre
        self.description = description
        self.datedebut = datedebut
        self.datefin = datefin
        self.niveaudurgence = niveaudurgence
        self.lieu = lieu

    def json(self):
        return {
            'id': self.id,
            'titre': self.titre,
            'description': self.description,
            'datedebut': str(self.datedebut),
            'datefin': str(self.datefin),
            'niveaudurgence': self.niveaudurgence,
            'lieu': self.lieu,
            'gadgets':[g.json() for g in self.gadgets],
            'agents':[ a.json() for a in self.agents]
        }

    @classmethod
    def find_by_id(cls, mission_id):
        return cls.query.filter_by(id=mission_id).first()

    @classmethod
    def find_by_titre(cls, titre):
        return cls.query.filter_by(titre=titre).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
