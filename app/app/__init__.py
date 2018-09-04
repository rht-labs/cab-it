from flask import Flask, templating, render_template, request
from app.api import api

def create_app():

    app = Flask(__name__, template_folder='templates/')

    ################################################################################
    # Storing something like a counter is really a job for redis or something 
    # like that - but I didn't want to introduce extra dependencies in this example.
    # Don't use application context for real storage!
    ################################################################################

    app.config.counter = 1

    app.register_blueprint(api, url_prefix='/api')

    # Templating and template inheritance
    @app.route('/')
    def index():
        return render_template('index.html', counter=app.config.counter)

    return app
