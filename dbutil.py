__author__ = 'thihara'

import sqlite3
from contextlib import closing
from flask import Flask

#Class containing two database functionalities, initializing database and obtaining a connection.
class DBUtil:
    flask = Flask(__name__)

    #Loads the configurations from the app_configs.py file.
    flask.config.from_pyfile('app_configs.py', False)

    #Drops existing tables and create new ones.
    def init_db(self):
        with closing(self.connect_db()) as db:
            with self.flask.open_resource('dbschema.sql', mode='r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    #Obtain and return a connection to the database
    def connect_db(self):
        return sqlite3.connect(self.flask.config['DATABASE'])

#initialize the database if run from the command line directly
if __name__ == '__main__':
    print("Initializing database...")
    DBUtil().init_db()
    print("Done.")