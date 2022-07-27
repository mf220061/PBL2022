from flask import jsonify, Flask
import os
import mysql.connector as mysql
from flask_bootstrap import Bootstrap

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_path='/app/instance')

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'test.db'),
    )

    bootstrap = Bootstrap(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    MYSQL_DATABASE_USER='root'
    MYSQL_DATABASE_PASSWORD='root'
    MYSQL_DATABASE_DB='blog'
    MYSQL_DATABASE_HOST='db'

    import db

    @app.route('/dev')
    def users():
        """
        connect = mysql.connect(
            user=MYSQL_DATABASE_USER,
            database=MYSQL_DATABASE_DB,
            password=MYSQL_DATABASE_PASSWORD,
            host=MYSQL_DATABASE_HOST,
            #port=MYSQL_DATABASE_PORT,
        )
        """
        
        connection = db.get_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user")

        rows = cursor.fetchall()
        #row = cursor.fetchone()

        #cursor.close()
        #db.close_db()
        cursor.close()
        #connection.close()

        resp = jsonify(rows)
        
        return resp

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    import auth
    app.register_blueprint(auth.bp)

    import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

app = create_app()

"""
if __name__ == "__main__":
    app = create_app()
    app.run()
"""
