import time
from tasks import add
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class testApi(Resource):
    def post(self):
        res ={
            'queue':'',
            'sum':''
        }
        task = str(request.args.get('task'))
        queue =  str(request.args.get('queue'))
        a = int(request.args.get('a'))
        b = int(request.args.get('b'))
        
        res['queue'] =queue
        res['sum'] = c.get()
        res = jsonify(res)
        res.status_code = 200
        return res
api.add_resource(testApi,'/')

if __name__ == "__main__":
    app.run('0.0.0.0',port=8181)