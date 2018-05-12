
import os

from flask import Flask, render_template, redirect, url_for, request

# import generate_sentences

app = Flask(__name__)


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]


@app.route("/waiting", methods=['GET', 'POST'])
def waiting():


    time_to_appointment = '12 - 16'

    html = render_template(
        'embed_simple.html',
        time_to_appointment=time_to_appointment
    )
    return html


@app.route("/", methods=['GET', 'POST'])
def login():

    error = None
    if request.method == 'POST':
        if request.form['username'] != 'demo' or request.form['date_of_birth'] != 'demo':
            # error = 'Invalid Credentials. Please try again.'
            return redirect(url_for('waiting'))
        else:
            return redirect(url_for('waiting'))
    return render_template('login.html', error=error)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

app.run(host='0.0.0.0', port=port)
