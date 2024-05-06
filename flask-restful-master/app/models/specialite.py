#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# standard python imports

from app.db import db

class SpecialiteModel(db.Model):
    __tablename__ = 'specialites'

    id = db.Column(db.Integer, primary_key=True)
    libelle = db.Column(db.String(100), unique=True)

    def __init__(self, libelle):
        self.libelle = libelle

    def json(self):
        return {'id': self.id, 'libelle': self.libelle}

    @classmethod
    def find_by_id(cls, specialite_id):
        return cls.query.filter_by(id=specialite_id).first()

    @classmethod
    def find_by_libelle(cls, libelle):
        return cls.query.filter_by(libelle=libelle).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()