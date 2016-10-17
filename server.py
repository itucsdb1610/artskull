from flask import Flask
from flask import render_template, session, redirect
import os

app = Flask(__name__)
app.secret_key = "itucsdb1610"
# For Bluemix
port = int(os.getenv('VCAP_APP_PORT', 8080))

@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    session['logged_in'] = True
    return redirect(url_for('home'))

if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=port) #for bluemix
    app.run(host='localhost', port='5000') #comment this while publishing to bluemix
