from flask import Flask, templating, render_template, request
from api import api

app = Flask(__name__, template_folder='templates/')

################################################################################
# Storing something like a counter is really a job for redis or something
# like that - but I didn't want to introduce extra dependencies in this example.
# Don't use application context for real storage!
################################################################################

app.config.counter = 1


# Templating and template inheritance
@app.route('/')
def index():
    return render_template('index.html', counter=app.config.counter)

app.register_blueprint(api, url_prefix='/api')

if __name__ == "__main__":
    app.run(host='0.0.0.0')