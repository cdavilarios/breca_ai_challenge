from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from json import dumps
import pymssql
from datetime import datetime
import calendar

conn = pymssql.connect(host = 'BREIN16000122\SQLEXPRESS', database = 'INTURSA_DM')
cursor = conn.cursor()

app = Flask(__name__)
api = Api(app)

month_number = {
    "Enero":1,
    "Febrero":2,
    "Marzo":3,
    "Abril":4,
    "Mayo":5,
    "Junio":6,
    "Julio":7,
    "Agosto":8,
    "Septiembre":9,
    "Octubre":10,
    "Noviembre":11,
    "Diciembre":12
}

def get_period(period):
    today = datetime.today()
    date_range = calendar.monthrange(today.year,today.month)
    cut_day = today
   
    if not period:
        init_day = today.replace(day=1)
        end_day = today.replace(day=date_range[1])
    elif "pasado" in period: #anio
        cut_day = today.replace(year=today.year-1)
        init_day = today.replace(year=today.year-1,day=1)
        end_day = today.replace(year=today.year-1,day=date_range[1])
    else:
        # por mes y hoy
        month = month_number[period]
        init_day = today.replace(month=month,day=1)
        end_day = today.replace(month=month,day=date_range[1]) 

    return init_day, end_day, cut_day
    

class Employees(Resource):
    def post(self):
        req = request.get_json(silent = True, force = True)
        params = req.get('queryResult').get('parameters')
        metric = params.get('metric')
        hotel = params.get('company')
        periodo = params.get('period')

        init_day, end_day, cut_day = get_period(periodo)

        for key, value in month_number.items():
            if value == init_day.month:
                month_name = key

        msg = metric

        if not hotel:
            hotel = 'ALL'
            msg += " general"
        else:
            msg += " de " + hotel

        msg += " en "+month_name+" del "+str(init_day.year)": "

        cut_day = cut_day.strftime('%d/%m/%Y')
        init_day = init_day.strftime('%d/%m/%Y')
        end_day = end_day.strftime('%d/%m/%Y')
        
        segment = params.get('segment')
        if not segment:
            segment = 'ALL'


        ### Query
        query = "SELECT BREIN.DBO.PRUEBA_4('%s','%s','%s','%s','%s')" % (metric, cut_day, init_day, end_day, segment, hotel)
        cursor.execute(query)
        row = cursor.fetchone()


        msg += str(row[0])
        response = {
            "fulfillmentText": msg
        }

        return make_response(jsonify(response))

api.add_resource(Employees, '/employees') # Route_1
#api.add_resource(Tracks, '/tracks') # Route_2
#api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3

if __name__ == '__main__':
     app.run(port='8080')