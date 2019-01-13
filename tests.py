from flask import request, jsonify
from flask_restful import Resource, fields, marshal_with
import os
import numpy as np
from sklearn.externals import joblib


path = os.path.dirname(os.path.realpath(__file__))
analytics_path = os.path.join(path, 'analytics')
sentiment_model_file = os.path.join(analytics_path, 'sentiment_model.pkl')
iris_model_file = os.path.join(analytics_path, 'iris_model.pkl')

# si estas sentencias se ponen acá, los objetos se cargan en la memoria del servidor al momento de iniciar la API,
# esto hace que las respuestas a las peticiones sean más rápidas
# si se ponen dentro de la función o clase, los objetos se leen del disco cada vez que se invoca el endpoint,
# lo que es más lento, pero reduce el uso de memoria del servidor
sentiment_model = joblib.load(sentiment_model_file)
iris_model = joblib.load(iris_model_file)

test_fields = {
    'test_url': fields.Url('test1', absolute=True)  # url del recurso test1
}


class Welcome(Resource):
    def get(self):
        return jsonify(message='Hola, esto es una API de prueba')


class Test1(Resource):
    def get(self):
        req = str(request.args)          # parámetros GET
        return jsonify(datos=req)

    def post(self):
        reqpars = str(request.args)      # parámetros GET
        reqjson = request.get_json()     # datos de una petición POST application/json
        reqform = str(request.form)      # datos de una petición tipo formulario application/x-www-form-urlencoded
        reqval = str(request.values)     # combina datos de formulario y parámetros GET
        reqstr = str(request.data)       # original en string (si mimetype no es reconocido)
        return jsonify(get=reqpars, json=reqjson, formulario=reqform, values=reqval, str=reqstr)


class Test2(Resource):
    @marshal_with(test_fields, envelope='data')
    def get(self):
        return {}                        # retorna test_fields


class Mathematics(Resource):
    def get(self):
        pars = request.args
        a = int(pars.get('a', 0))
        b = int(pars.get('b', 0))
        return jsonify(value=a+b)


class Sentiment(Resource):

    def scorer(self, text, classifier):
        pred = classifier.predict(text)[0]
        ppred = np.max(classifier.predict_proba(text)[0])
        return jsonify(sentiment=int(pred), probability=float(ppred))

    def post(self):
        jdata = request.get_json()
        text = [jdata.get('text')]
        result = self.scorer(text=text, classifier=sentiment_model)
        return result


class Iris(Resource):

    def scorer(self, data, classifier):
        try:
            sepal_length, sepal_width = float(data['sepal_length']), float(data['sepal_width'])
            petal_length, petal_width = float(data['petal_length']), float(data['petal_width'])
            # deben ir en el mismo orden en que se estimó el modelo
            data_p = [[sepal_length, sepal_width, petal_length, petal_width]]
            pred = classifier.predict(data_p)[0]
            ppred = round(np.max(classifier.predict_proba(data_p)), 4)
            return jsonify(predicted=pred, probability=float(ppred), message='success')
        except:
            return jsonify(predicted=None, probability=None, message='There was an error')

    def get(self):
        reqdata = request.args
        result = self.scorer(data=reqdata, classifier=iris_model)
        return result

    def post(self):
        reqdata = request.get_json()
        result = self.scorer(data=reqdata, classifier=iris_model)
        return result

