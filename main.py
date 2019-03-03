from flask import Flask
import MySQLdb

app = Flask(__name__)
@app.route('/')
def main():
    db = MySQLdb.connect(host="localhost",user="root", passwd="",db="Project")
    cursor = db.cursor()
    cursor.execute("""SELECT * FROM members""")
    data = cursor.fetchall()
    return str(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
