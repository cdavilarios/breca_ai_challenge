from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from json import dumps
import pymssql

conn = pymssql.connect(server = 'brein.c75yaa9tpxts.us-east-2.rds.amazonaws.com', user = 'BREIN', password = 'Rachel123456')
cursor = conn.cursor()
query = "SELECT BREIN.DBO.PRUEBA_4('20/11/2018','01/11/2018','30/11/2018','RETAIL','Westin')"
cursor.execute(query)
row = cursor.fetchone()

app = Flask(__name__)
api = Api(app)

class Employees(Resource):
    def post(self):
        req = request.get_json(silent = True, force = True)
        params = req.get('queryResult').get('parameters')
        metric = params.get('metric')
        msg = 'El ' + metric + ' es ' + str(row[0])
        response = {
        "fulfillmentText": msg
        }

        return make_response(jsonify(response))

api.add_resource(Employees, '/employees') # Route_1
#api.add_resource(Tracks, '/tracks') # Route_2
#api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3

if __name__ == '__main__':
     app.run(port='8080')