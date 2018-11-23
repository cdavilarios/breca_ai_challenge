# Librerias 
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from json import dumps
from datetime import datetime, timedelta
import calendar
import pyodbc

# Conexion local sql server
conn = pyodbc.connect("DSN=BREINLOCAL")
cursor = conn.cursor()

app = Flask(__name__)
api = Api(app)

month_number = {
    "ENERO":1,
    "FEBRERO":2,
    "MARZO":3,
    "ABRIL":4,
    "MAYO":5,
    "JUNIO":6,
    "JULIO":7,
    "AGOSTO":8,
    "SEPTIEMBRE":9,
    "OCTUBRE":10,
    "NOVIEMBRE":11,
    "DICIEMBRE":12
}

metricas = {
    'La tarifa promedio': 'REVENUE',
    'El pickup': 'REVENUE',
    'La ocupacion': 'OCUPACION'
}

def get_metrica(metrica):
    return metricas[metrica]

def get_period(period):
    today = datetime.today()
    yesterday = datetime.today() - timedelta(days = 1)
    date_range = calendar.monthrange(today.year,today.month)
    cut_day = yesterday
   
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

        # Inicio del Post  
        print('********************')
        print('INICIO')

        # Inputs de Dialogflow 
        req = request.get_json(silent = False, force = True)
        params = req.get('queryResult').get('parameters')

        metric = params.get('metric')
        metric_std = get_metrica(metric)
        hotel = params.get('company')
        segment = params.get('segment')
        periodo = params.get('period').upper()

        intent = req.get('queryResult').get('intent').get('displayName')
        
        print(metric)
        print(hotel)
        print(segment)
        print(periodo)
        
        # Extraer fechas del periodo 
        init_day, end_day, cut_day = get_period(periodo)
        
        print(init_day)
        print(end_day)
        print(cut_day)

        mensaje = metric

        for key, value in month_number.items():
            if value == init_day.month:
                nombre_mes = key

        if not hotel:
            hotel = 'ALL'
            mensaje = mensaje + " general"
        else:
            mensaje = mensaje + " de " + hotel

        if not segment:
            segment = 'ALL'

        mensaje = mensaje + " en " + nombre_mes + " del " + str(init_day.year) + ": "

        cut_day = cut_day.strftime('%d/%m/%Y')
        init_day = init_day.strftime('%d/%m/%Y')
        end_day = end_day.strftime('%d/%m/%Y')
        
        ### Query
        
        print('LLAMADA A QUERY')
        query = "SELECT DBO.FMASTER_2('%s','%s','%s','%s','%s','%s')" % (metric_std, cut_day, init_day, end_day, segment, hotel)
        cursor.execute(query)
        row = cursor.fetchone()
        
        # Valor extraido de Query 
        print(row)

        ### Respuesta Dialogflow 
        mensaje = mensaje + str(row[0])
        response = {
            "fulfillmentText": mensaje
        }

        print('FIN')

        return make_response(jsonify(response))

# Crear servicio 
api.add_resource(Employees, '/employees') # Route_1

if __name__ == '__main__':
     app.run(port='8080')