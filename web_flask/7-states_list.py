#!/usr/bin/python3

'''
a script that starts a Flask web application:
    /states_list: display a HTML page: (inside the tag BODY)
        H1 tag: “States”
        UL tag: with the list of all State objects present
        in DBStorage sorted by name (A->Z)
            LI tag: description of one State: <state.id>: <B><state.name></B>
'''
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def show_states():
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def close(self):
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
