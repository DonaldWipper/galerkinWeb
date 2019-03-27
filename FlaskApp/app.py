from flask import Flask, render_template, make_response
#from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sql
from flask import request, flash
import json
import requests
import csv
from datetime import date
from datetime import datetime

import sympy
import latex

db = None

settings = {"sql_host":"us-iron-auto-dca-04-a.cleardb.net", 
            "sql_user":"b1df3776b2b56c",
            "sql_passwd":"2153543acdac76f",
            "sql_db":"heroku_0c1d0ea4e380413"
           }

points = []
equations = []
rates = []

app = Flask(__name__)
app.config.from_object(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True






def init_data():
    global db, points, equations
    # id, id_problem_params, dxi, fx, gx, dti, time_modif
    id_problem_params = 4
    dti = 69; 
    db = sql.database(settings['sql_host'],  settings['sql_user'],  settings['sql_passwd'], settings['sql_db'])
    equations = db.getDictFromQueryRes("equations", None)  
    fluxes = db.getDictFromQueryRes("fluxes", None)  
    print(equations)
def render():
    global equations 
    return render_template("formula2.html", equations = equations)




#get settings

def read_params(fn): 
    d ={} 
    try:
        with open(fn, 'r',encoding="utf-8") as file: 
            d = json.load(file) 
    except FileNotFoundError:
         print ("Error. Can't find file " + fn)
         d = {}
    return d 



@app.route("/", methods=['GET'])
def main():
    init_data()
    return render()
    

if __name__ == "__main__":
    app.run(debug = True)
