from flask import templating, render_template, request, Blueprint, current_app


################################################################################
# Storing something like a counter is really a job for redis or something
# like that - but I didn't want to introduce extra dependencies in this example.
# Don't use application context for real storage!
################################################################################

# GET method demos, with parameters in the URL path (converted to ints for us)

def get_counter():
    return str(current_app.counter)


def set_counter(value):
    current_app.counter = int(value)
    return str(current_app.counter)


def increment_counter_get(amount):
    current_app.counter = current_app.counter + amount
    # return render_template('counter_changed.html', change_type="incremented", amount=amount, counter=current_app.counter)
    return current_app.counter


def decrement_counter_get(amount):
    current_app.counter = current_app.counter - amount
    # return render_template('counter_changed.html', change_type="decremented", amount=amount, counter=current_app.counter)
    return current_app.counter


# POST method demos

def increment_counter_post():
    # amount = int(request.form.get('amount'))
    # current_app.counter = current_app.counter + amount
    # return render_template('counter_changed.html', change_type="incremented", amount=amount, counter=current_app.counter)
    current_app.counter = current_app.counter + 1
    return current_app.counter


def decrement_counter_post():
    # amount = int(request.form.get('amount'))
    # current_app.counter = current_app.counter - amount
    # return render_template('counter_changed.html', change_type="decremented", amount=amount, counter=current_app.counter)
    current_app.counter = current_app.counter - 1
    return current_app.counter
# Note: GET and POST demos could also be combined to single increment and decrement functions, with `request.method == 'POST'` used to determine GET or POST data.
