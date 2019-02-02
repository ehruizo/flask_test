from flask import request, jsonify
from flask_restful import Resource, fields, marshal_with


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


test_fields = {
    'test_url': fields.Url('test1', absolute=True)  # url absoluta del recurso test1 (similar a url_for(...))
}


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
