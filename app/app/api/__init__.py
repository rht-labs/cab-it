from flask import templating, render_template, request, Blueprint, current_app

api = Blueprint("api", __name__)

################################################################################
# Storing something like a counter is really a job for redis or something 
# like that - but I didn't want to introduce extra dependencies in this example.
# Don't use application context for real storage!
################################################################################

# GET method demos, with parameters in the URL path (converted to ints for us)

@api.route('/counter')
def get_counter():

    return str(current_app.config.counter)

@api.route('/set_counter/<int:value>', methods=['GET'])
def set_counter(value):

    current_app.config.counter = int(value)
    return str(current_app.config.counter)

@api.route('/increment_counter/<int:amount>', methods=['GET'])
def increment_counter_get(amount):

    current_app.config.counter = current_app.config.counter + amount
    return render_template('counter_changed.html', change_type="incremented", amount=amount, counter=current_app.config.counter)

@api.route('/decrement_counter/<int:amount>', methods=['GET'])
def decrement_counter_get(amount):

    current_app.config.counter = current_app.config.counter - amount
    return render_template('counter_changed.html', change_type="decremented", amount=amount, counter=current_app.config.counter)

# POST method demos

@api.route('/increment_counter', methods=['POST'])
def increment_counter_post():

    amount = int(request.form.get('amount'))
    current_app.config.counter = current_app.config.counter + amount
    return render_template('counter_changed.html', change_type="incremented", amount=amount, counter=current_app.config.counter)

@api.route('/decrement_counter', methods=['POST'])
def decrement_counter_post():

    amount = int(request.form.get('amount'))
    current_app.config.counter = current_app.config.counter - amount
    return render_template('counter_changed.html', change_type="decremented", amount=amount, counter=current_app.config.counter)

# Note: GET and POST demos could also be combined to single increment and decrement functions, with `request.method == 'POST'` used to determine GET or POST data.