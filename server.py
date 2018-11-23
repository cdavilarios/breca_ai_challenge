from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from json import dumps
import pymssql
from datetime import datetime

conn = pymssql.connect(server = 'brein.c75yaa9tpxts.us-east-2.rds.amazonaws.com', user = 'BREIN', password = 'Rachel123456')
cursor = conn.cursor()

app = Flask(__name__)
api = Api(app)



class Employees(Resource):
    def post(self):
        req = request.get_json(silent = True, force = True)
        params = req.get('queryResult').get('parameters')
        metric = params.get('metric')
        hotel = params.get('company')

        periodo = params.get('company')

        if not hotel:
            hotel = 'ALL' 
            
        print('******************************************')
        print(hotel)
        print('******************************************')

        segment = 'RETAIL'
        query = "SELECT BREIN.DBO.PRUEBA_4('20/11/2018','01/11/2018','30/11/2018','%s','%s')" % (segment, hotel)
        cursor.execute(query)
        row = cursor.fetchone()

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