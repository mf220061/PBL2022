from flask import jsonify, Flask
import os
import mysql.connector as mysql

app = Flask(__name__)

app.config.from_mapping(
    SECRET_KEY='dev',
)

MYSQL_DATABASE_USER='root'
MYSQL_DATABASE_PASSWORD='root'
MYSQL_DATABASE_DB='blog'
MYSQL_DATABASE_HOST='db'

@app.route('/')
def index():
    return 'Root'

@app.route('/dev')
def users():
    connect = mysql.connect(
            user=MYSQL_DATABASE_USER,
            database=MYSQL_DATABASE_DB,
            password=MYSQL_DATABASE_PASSWORD,
            host=MYSQL_DATABASE_HOST,
            #port=MYSQL_DATABASE_PORT,
        )
    
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM user")

    rows = cursor.fetchall()

    cursor.close()

    resp = jsonify(rows)
    
    return resp

@app.route('/hello')
def hello():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run()
