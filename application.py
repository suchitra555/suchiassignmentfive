from flask import Flask
import os
import random
import time

import pyodbc
import pandas as pd
import redis as redis
from flask import Flask, render_template, request
import sqlite3 as sql

from math import radians, sin, cos, sqrt, atan2

myHostname = "azureassignment3.redis.cache.windows.net"
myPassword = "xw5S6heXPfqGZL4PfzatH+d7nnCawcY5dSMNTyWC+qQ="
server = 'mysqlserversuchitra.database.windows.net'
database = 'assignment3'
username = 'azureuser'
password = 'Geetha1963@'
driver= '{ODBC Driver 17 for SQL Server}'

app = Flask(__name__)
port = os.getenv('VCAP_APP_PORT','5000')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/q6')
def q6():
    return render_template('options.html')

@app.route('/q8')
def q8():
    return render_template('options1.html')


@app.route('/restrictedlat')
def restrictedlat():
    return render_template('lat.html')

@app.route('/list', methods = ['POST', 'GET'])
def list():
   con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
   cur = con.cursor()
   dep1 = float(request.form['dep1'])
   dep2 = float(request.form['dep2'])
   lon = float(request.form['lon'])
   cur.execute("select latitude,longitude,time,depthError from quake6 where longitude > ? and depthError between ? and ?",(lon,dep1,dep2))
   rows = cur.fetchall()
   con.close()
   return render_template("list.html",rows = rows)

@app.route('/options', methods=['POST', 'GET'])
def options():
    con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    start_time = time.time()
    num = int(request.form['num'])
    rows = []
    get = []
    c = []
    points = []
    points.append(['Mag','Query Count'])
    for i in range(num):
        val = round(random.uniform(2,5),1)
        cur = con.cursor()
        a = 'select * from all_month WHERE mag = '+str(val)
       #cur.execute("select * from all_month WHERE mag = ?" ,(val,))
        v = str(val)
        if r.get(a):
            print ('Cached')
            c.append('Cached')
            #print (r.get(a))
            rows.append(r.get(a))
        else:
            print('Not Cached')
            c.append('Not Cached')
            cur.execute("select count(*) from all_month WHERE mag = ?" ,(val,))
            get = cur.fetchone();
            rows.append(get)
            r.set(a,str(get))
        count = rows[i][0]
        #print (rows[0][0])
        points.append([val, count])
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", rows=[c], etime=elapsed_time, p=points)


@app.route('/optionspie', methods=['POST', 'GET'])
def optionspie():
    #con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    #r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    # start_time = time.time()
    # num = int(request.form['num'])
    # rows = []
    # get = []
    # c = []
    data=[]
    # points = []
    # points.append(['Mag','Query Count'])
    # for i in range(num):
    #     val = round(random.uniform(2,5),1)
    #     cur = con.cursor()
     #   a = 'select * from all_month WHERE mag = '+str(val)
    #     v = str(val)
    #     if r.get(a):
    #         c.append('Cached')
    #         rows.append(r.get(a))
    #     else:
    #         print('Not Cached')
    #         c.append('Not Cached')
    #         cur.execute("select count(*) from all_month WHERE mag = ?" ,(val,))
    #         get = cur.fetchone();
    #         rows.append(get)
    #         r.set(a,str(get))
    #     count = rows[i][0]
    #     points.append([str(val), count])
    # end_time = time.time()
    # elapsed_time = end_time - start_time
    return render_template("chart_pie.html")

@app.route('/histogram', methods=['POST', 'GET'])
def histogram():
    con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    start_time = time.time()
    num = int(request.form['num'])
    rows = []
    get = []
    c = []
    points = []
    points.append(['Mag','Query Count'])
    for i in range(num):
        val = round(random.uniform(2,5),1)
        cur = con.cursor()
        a = 'select * from all_month WHERE mag = '+str(val)
        v = str(val)
        if r.get(a):
            c.append('Cached')
            rows.append(r.get(a))
        else:
            print('Not Cached')
            c.append('Not Cached')
            cur.execute("select count(*) from all_month WHERE mag = ?" ,(val,))
            get = cur.fetchone();
            rows.append(get)
            r.set(a,str(get))
        count = rows[i][0]
        points.append([str(val), count])
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("barchart.html", rows=[c], etime=elapsed_time, p=points)

@app.route('/barchart', methods=['POST', 'GET'])
def barchart():
    con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)
    start_time = time.time()
    num = int(request.form['num'])
    rows = []
    get = []
    c = []
    points = []
    points.append(['Mag','Query Count'])
    for i in range(num):
        val = round(random.uniform(2,5),1)
        cur = con.cursor()
        a = 'select * from all_month WHERE mag = '+str(val)
        v = str(val)
        if r.get(a):
            c.append('Cached')
            rows.append(r.get(a))
        else:
            print('Not Cached')
            c.append('Not Cached')
            cur.execute("select count(*) from all_month WHERE mag = ?" ,(val,))
            get = cur.fetchone();
            rows.append(get)
            r.set(a,str(get))
        count = rows[i][0]
        points.append([str(val), count])
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("barcharts.html", rows=[c], etime=elapsed_time, p=points)





if __name__ == '__main__':
    app.run(debug=True)
