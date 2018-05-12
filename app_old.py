
import os

from flask import Flask, render_template, redirect, url_for, request

import generate_sentences

app = Flask(__name__)


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]


@app.route("/", methods=['GET', 'POST'])
def tracker():
    """ Very simple embedding of a polynomial chart
    """

    # possible_products = ['Syringes', 'Cannulas', 'Needles', 'Catheters']
    # possible_hospitals = ['Western General', 'Royal Edinburgh Hospital']
    #
    # # Grab the inputs arguments from the URL
    # form = request.form
    #
    # product = getitem(form, 'product', 'Syringes').rstrip(' ') # mysterious right space appears
    # other_products = [item for item in possible_products if item != product]
    # products = [product] + other_products
    #
    # hospital = getitem(form, 'hospital', 'Western General').rstrip(' ') # mysterious right space appears
    # other_hospitals = [item for item in possible_hospitals if item != hospital]
    # hospitals = [hospital] + other_hospitals


    markov_model_loc = 'saved_models/text_model.txt'  # markov model we'll load
    text_model = generate_sentences.load_markov_model(markov_model_loc)
    fake_titles = generate_sentences.generate_text(text_model, n_sentences=4, tries=50)


    html = render_template(
        'embed_simple.html',
        # hospitals=hospitals,
        # products=products,
        # future_orders=future_orders,
        # selected_hospital=hospital,
        # selected_product=product
        fake_titles=fake_titles
    )
    return html


# @app.route("/", methods=['GET', 'POST'])
# def login():
#
#     error = None
#     if request.method == 'POST':
#         if request.form['username'] != 'demo' or request.form['password'] != 'demo':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('waiting'))
#     return render_template('login.html', error=error)
#

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

app.run(host='0.0.0.0', port=port)
