from flask_restful import Resource, reqparse
from app.models.specialite import SpecialiteModel
from flask_jwt_extended import jwt_required
from app.util.logz import create_logger

class Specialite(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('libelle', type=str, required=True, help='Le libellé de la spécialité est requis.')

    def __init__(self):
        self.logger = create_logger()

    def get(self, libelle):
        specialite = SpecialiteModel.find_by_libelle(libelle)
        if specialite:
            return specialite.json()
        return {'message': 'Specialité not found'}, 404

    @jwt_required()  # Requiert un token JWT
    def post(self):
        data = Specialite.parser.parse_args()
        libelle = data['libelle']

        if SpecialiteModel.find_by_libelle(libelle):
            return {'message': f"Une spécialité avec le libellé '{libelle}' existe déjà."}, 400

        specialite = SpecialiteModel(libelle)
        try:
            specialite.save_to_db()
        except:
            return {"message": "Une erreur est survenue lors de la création de la spécialité."}, 500

        return specialite.json(), 201

    @jwt_required()  # Requiert un token JWT
    def delete(self, libelle):
        specialite = SpecialiteModel.find_by_libelle(libelle)
        if specialite:
            specialite.delete_from_db()

        return {'message': 'Specialité supprimée'}

class SpecialiteList(Resource):
    def get(self):
        return {'specialites': [specialite.json() for specialite in SpecialiteModel.query.all()]}
