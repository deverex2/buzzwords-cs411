from flask import Flask
from flask import request
from flask import Response
from flask import redirect
import json
import MySQLdb

app = Flask(__name__)
@app.route('/')
def main():
    # db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    # cursor = db.cursor()
    # cursor.execute("""SHOW TABLES""")
    # data = cursor.fetchall()
    # return str(data)
    return redirect("https://kys2.gitlab.io/cs411_final/#/", code=302)

@app.route('/artist')
def artist():
    name = request.args.get('name')
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Artists WHERE name=%s""", (name,))
    data = cursor.fetchall()
    resp = Response(str(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
    
@app.route('/song')
def song():
    title = request.args.get('title')
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Songs WHERE title=%s""", (title,))
    data = cursor.fetchall()
    resp = Response(str(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/search')
def search():
    gram = request.args.get('gram')
    groupby = request.args.get('groupby')
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    if groupby=='year':
        cursor.execute("""SELECT year, SUM(l_freq) FROM ((SELECT * FROM Lyrics WHERE words = %s) S1 NATURAL JOIN (SELECT s_id, year FROM Songs) S2) GROUP BY year;""", (gram,))
    elif groupby=='artist':
        cursor.execute("""SELECT name, SUM(l_freq) FROM(((SELECT * FROM Lyrics WHERE words = %s) S1 NATURAL JOIN (SELECT s_id, a_id FROM Songs) S2 ) NATURAL JOIN (SELECT a_id, name FROM Artists) S3) GROUP BY name ;""", (gram,))
    elif groupby=='genre':
        cursor.execute("""SELECT genre, SUM(l_freq) FROM (((SELECT * FROM Lyrics WHERE words = %s) S1 NATURAL JOIN (SELECT * FROM Genre) S2 )) GROUP BY genre ;""", (gram,))
    else:
        return "-1"
    data = cursor.fetchall()
    data = {"items": [[x[0],int(x[1])] for x in data]}
    print(data)
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/testn')
def testn():
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM Lyrics""")
    data = cursor.fetchall()
    resp = Response(str(data))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
 

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
