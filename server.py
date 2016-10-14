from flask import Flask
from flask import render_template
import os

app = Flask(__name__)

# For Bluemix
port = int(os.getenv('VCAP_APP_PORT', 8080))

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port) #for bluemix
    #app.run(host='localhost', port='5000') #comment this while publishing to bluemix