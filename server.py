from flask import Flask, render_template
import os

app = Flask(__name__)

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

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
    
