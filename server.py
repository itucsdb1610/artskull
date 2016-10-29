from flask import Flask, render_template, redirect, url_for
import os
import json
import re
import psycopg2 as dbapi2

app = Flask(__name__)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        connection.commit()

    return redirect(url_for('home'))

@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """UPDATE COUNTER SET N = N+1"""
        cursor.execute(query)
        connection.commit()

        query = """SELECT N FROM COUNTER"""
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return "This page was accessed %d times" % count

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/content')
def content():
    return render_template('content.html')

@app.route('/admin')
def admin():
    return render_template('contentadmin.html')

@app.route('/search')
def search():
    return render_template('searchresult.html')

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephant_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant' host='localhost' port=54321 dbname='itucsdb1610'"""
    app.run(host='0.0.0.0', port=port, debug=debug)
    
