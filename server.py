from flask import Flask, render_template
import os
from handlers import site

# For Bluemix
port = int(os.getenv('VCAP_APP_PORT', 8080))

def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.secret_key = "itucsdb1610"
    app.register_blueprint(site)

    return app


def main():
    app = create_app()
    debug = app.config['DEBUG']
    port = app.config['PORT']
    #app.run(host='0.0.0.0', port=port) #for bluemix
    app.run(host='localhost', port=port, debug=debug) #comment this while publishing to bluemix


if __name__ == '__main__':
    main()
    
