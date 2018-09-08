"""
API REST example
"""
from flask import Flask, request, jsonify, abort
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from tests import Welcome, Test1, Test2, Mathematics, Sentiment, Iris


# flask configs
app = Flask(__name__)
app.config.from_object('settings')

# crea la API
api = Api(app)

# base de datos
meta = MetaData(schema=app.config['DB_SCHEMA'])
db = SQLAlchemy(app, metadata=meta)


# modelos de datos

class Conversor(db.Model):
    __tablename__ = 'conversor'
    __table_args__ = {'autoload': True, 'autoload_with': db.engine}


# vistas

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


class Portales(Resource):
    def get(self):
        portals = [i[0] for i in Conversor.query.with_entities(Conversor.portal).distinct().order_by(Conversor.portal)]
        return jsonify(count=len(portals), portals=portals)


class UserData(Resource):
    @marshal_with(user_fields, envelope='data')
    def get(self, rsa_userid):
        result = Conversor.query.filter_by(rsa_userid=rsa_userid).all()
        return result


class UserDataPost(Resource):
    @marshal_with(doc_fields)
    def post(self):
        try:
            documento = request.get_json()['documento']
        except:
            abort(400)
        else:
            result = Conversor.query.filter_by(documento=documento).all()
            return {'matches': len(result), 'users': result}


# endpoints

SITE_PREFIX = app.config['SITE_PREFIX']
api.add_resource(Welcome, '{}/'.format(SITE_PREFIX))
api.add_resource(Test1, '{}/test1'.format(SITE_PREFIX))
api.add_resource(Test2, '{}/test2'.format(SITE_PREFIX))
api.add_resource(Mathematics, '{}/sum'.format(SITE_PREFIX))
api.add_resource(Portales, '{}/portales'.format(SITE_PREFIX))
api.add_resource(UserData, '{}/user/<string:rsa_userid>'.format(SITE_PREFIX))
api.add_resource(UserDataPost, '{}/doc'.format(SITE_PREFIX))
api.add_resource(Sentiment, '{}/sentiment'.format(SITE_PREFIX))
api.add_resource(Iris, '{}/iris'.format(SITE_PREFIX))


if __name__ == '__main__':
    app.run(debug=True)
