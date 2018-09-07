from flask import Flask, request, redirect
import connexion
# from app import settings

# def configure_app(flask_app):
#     flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
#     # flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
#     # flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
#     flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
#     flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
#     flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
#     flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP

def create_app():
    app = connexion.App(__name__, port=8080, specification_dir='swagger/')
    app.add_api('counter.yml', arguments={'title': 'Counter Example'})
    # configure_app(app)

    ################################################################################
    # Storing something like a counter is really a job for redis or something
    # like that - but I didn't want to introduce extra dependencies in this example.
    # Don't use application context for real storage!
    ################################################################################

    # the Flask object is wrapped by connexion.App so it's now app.app.normal_flask_things
    app.app.counter = 1

    # Templating and template inheritance
    @app.route('/')
    def index():
        return redirect('/api/ui', code=302)

    return app


flask_app = create_app()
