from app.db import db
mission_agent = db.Table('mission_agent',
    db.Column('mission_id', db.Integer, db.ForeignKey('missions.id'), primary_key=True),
    db.Column('agent_id', db.Integer, db.ForeignKey('agents.id'), primary_key=True)
)