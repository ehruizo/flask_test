"""
API REST example
"""
from flask_restful import Api
from app import app
from modules.tests import Welcome, Test1, Test2, Mathematics
from modules.conversor import Portales, UserData, DocumentData
from modules.analytics import Sentiment, Iris


# objeto API
api = Api(app)


# endpoints
SITE_PREFIX = app.config.get('SITE_PREFIX', '')
api.add_resource(Welcome, '{}/'.format(SITE_PREFIX))
api.add_resource(Test1, '{}/test1'.format(SITE_PREFIX))
api.add_resource(Test2, '{}/test2'.format(SITE_PREFIX))
api.add_resource(Mathematics, '{}/sum'.format(SITE_PREFIX))
api.add_resource(Portales, '{}/portales'.format(SITE_PREFIX))
api.add_resource(UserData, '{}/user/<string:rsa_userid>'.format(SITE_PREFIX))
api.add_resource(DocumentData, '{}/doc'.format(SITE_PREFIX))
api.add_resource(Sentiment, '{}/sentiment'.format(SITE_PREFIX))
api.add_resource(Iris, '{}/iris'.format(SITE_PREFIX))


if __name__ == '__main__':
    app.run(debug=True)
