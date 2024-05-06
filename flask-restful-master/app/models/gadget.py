#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from app.db import db


class GadgetModel(db.Model):
    __tablename__ = 'gadgets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    puissance = db.Column(db.Float(precision=2))

    def __init__(self, name, puissance):
        self.name = name
        self.puissance = puissance

    def json(self):
        return {'name': self.name, 'price': self.puissance}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self):  # Upserting data
        db.session.add(self)
        db.session.commit()  # Balla

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
