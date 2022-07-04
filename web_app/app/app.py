from flask import Flask, current_app

app = Flask(__name__)

from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
"""
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'roytuts'
app.config['MYSQL_DATABASE_HOST'] = 'db'
"""
app.config.from_mapping(
    MYSQL_DATABASE_USER='root',
    MYSQL_DATABASE_PASSWORD='root',
    MYSQL_DATABASE_DB='roytuts',
    MYSQL_DATABASE_HOST='db',
)
# mysql.init_app(app)でapp.configで設定したflaskの設定値をmysqlに渡す準備をしている感じ
mysql.init_app(app)

import pymysql
from flask import jsonify

@app.route('/')
def users():
    conn = mysql.connect()
    
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM user")

    rows = cursor.fetchall()

    resp = jsonify(rows)
    resp.status_code = 200
    
    return resp

"""
if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
"""
