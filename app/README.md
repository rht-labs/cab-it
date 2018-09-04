# Labs Flask Skeleton

This is a simple counter API built as a demo of a minimal Flask app. It simply uses application context for storing the counter. __Do not do that in production__.

You should be able to develop using `docker-compose up`, with live reloading thanks to Flask's debug mode. The app will be available on http://localhost:5000

It is recommended to have virtualenv running in another terminal for the purpose of isolating dependencies and running tests. If you don't have the virtualenv tool installed, pip can install it with `python3 -m pip install --user virtualenv`. Then, `python3 -m virtualenv env && source env/bin/activate && pip3 install -r requirements.txt` should initialize virtualenv for first use.

You can exit the virtualenv at any time with `deactivate`, and reenter it later simply with `source env/bin/activate`. (The `env` directory is excluded from source control and is generated when you initialize virtualenv for the first time.)

If you modify any dependencies inside of the virtualenv and need to create a new `requirements.txt` file, use `pip3 freeze >>> requirements.txt`.

To test, run `pytest` or `pytest -v` in your virtualenv.