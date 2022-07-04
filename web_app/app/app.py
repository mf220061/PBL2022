import os

from flask import Flask

"""
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        MYSQL_DATABASE_USER='root',
        MYSQL_DATABASE_PASSWORD='root',
        MYSQL_DATABASE_DB='blog',
        MYSQL_DATABASE_HOST='db',
        DATABASE=os.path.join(app.instance_path, 'blog.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app
"""

app = Flask(__name__)

from flaskext.mysql import MySQL

mysql = MySQL()
 
# MySQL configurations
app.config.from_mapping(
    MYSQL_DATABASE_USER='root',
    MYSQL_DATABASE_PASSWORD='root',
    MYSQL_DATABASE_DB='blog',
    MYSQL_DATABASE_HOST='db',
    #DATABASE=os.path.join(app.instance_path, 'blog.db'),
)
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'roytuts'
#app.config['MYSQL_DATABASE_HOST'] = 'db'
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

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
