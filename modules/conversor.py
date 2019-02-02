from flask import request, jsonify, abort
from flask_restful import Resource, fields, marshal_with
from models import Conversor


# formato de campos de salida

class DateFormat(fields.Raw):
    def format(self, value):
        return value.strftime('%Y-%m-%d')


user_fields = {
    'userid': fields.String(attribute="rsa_userid"),
    'documento': fields.String,
    'tipodocumento': fields.String,
    'grupo': fields.String,
    'portal': fields.String,
    'nombre': fields.String,
    'primerlogin': DateFormat,
    'ultimologin': DateFormat
}

doc_fields = {'matches': fields.Integer, 'users': fields.Nested(user_fields)}


# lógica

class Portales(Resource):
    def get(self):
        portals = [i[0] for i in Conversor.query.with_entities(Conversor.portal).distinct().order_by(Conversor.portal)]
        return jsonify(count=len(portals), portals=portals)


class UserData(Resource):
    @marshal_with(user_fields, envelope='data')
    def get(self, rsa_userid):
        result = Conversor.query.filter_by(rsa_userid=rsa_userid).all()
        return result


class DocumentData(Resource):
    @marshal_with(doc_fields)
    def post(self):
        try:
            documento = request.get_json()['documento']
        except:
            abort(400)
        else:
            result = Conversor.query.filter_by(documento=documento).all()
            return {'matches': len(result), 'users': result}
