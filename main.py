from flask import Flask
from flask import request
from flask import Response
from flask import redirect
from phrase_recommender.phrase_recommender import get_phrase_recommendation
from comparer import compareArtists
import json
import MySQLdb


app = Flask(__name__)
@app.route('/')
def main():
    return redirect("https://kys2.gitlab.io/cs411_final/#/", code=302)

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
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/phrase_recommend')
def phrase_recommend():
    genre = request.args.get('genre')
    year = request.args.get('year')
    data = get_phrase_recommendation(str(genre), str(year))
    data = set([x.replace('\"', '').replace('_', ' ') for x in data])
    if " " in data:
        data.remove(" ")
    if "" in data:
        data.remove("")
    data = {"phrases": list(data)}
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/artist_similarity')
def artist_similarity():
    a1 = request.args.get('artist1')
    a2 = request.args.get('artist2')
    data = compareArtists(a1, a2)
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/genres')
def genres():
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""SELECT DISTINCT genre FROM Genre""")
    data = cursor.fetchall()
    data = {"genres": [x[0] for x in data]}
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/remove_genre')
def remove_genre():
    genre = request.args.get('genre')
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""CALL delete_genre(%s)""",(genre,))
    cursor.execute("""SELECT DISTINCT genre FROM Genre""")
    data = cursor.fetchall()
    db.commit()
    data = {"genres": [x[0] for x in data]}
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/update_genre')
def update_genre():
    old = request.args.get('old')
    new = request.args.get('new')
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""PREPARE updategenrestatement FROM 'UPDATE Genre SET genre = ? WHERE genre = ?'""")
    cursor.execute("""SET @a = %s""" (old,))
    cursor.execute("""SET @b = %s""" (new,))
    cursor.execute("""EXECUTE updategenrestatement USING @a, @b""")
    cursor.execute("""SELECT DISTINCT genre FROM Genre""")
    data = cursor.fetchall()
    db.commit()
    data = {"genres": [x[0] for x in data]}
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/add_genre')
def add_genre():
    genre = request.args.get('genre')
    song = request.args.get('song')
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""SELECT s_id FROM Songs WHERE title=%s""",(song,))
    sid = cursor.fetchall()
    sid = [x[0] for x in sid]
    if len(sid)==1:
        sid = sid[0]
        cursor.execute("""INSERT INTO Genre(s_id, genre) VALUES (%s, %s)""", (sid, genre,))
    cursor.execute("""SELECT DISTINCT genre FROM Genre""")
    data = cursor.fetchall()
    db.commit()
    data = {"genres": [x[0] for x in data]}
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/years')
def years():
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""SELECT DISTINCT year FROM Songs""")
    data = cursor.fetchall()
    data = {"years": [x[0] for x in data]}
    resp = Response(json.dumps(data), mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
