
import os
import io

import numpy as np
from flask import Flask, render_template
from latex2markdown import LaTeX2Markdown as latex2markdown

from randomiser import generate_sentences


app = Flask(__name__)


def getitem(obj, item, default):
    if item not in obj:
        return default
    else:
        return obj[item]


@app.route("/", methods=['GET', 'POST'])
def home():


    n_titles = 8
    cached = True


    if cached:
        with io.open('data/cached_titles/titles.txt', mode='r') as f:
            all_titles = f.readlines()
            fake_titles = np.random.choice(all_titles, n_titles)
    else:
        markov_model_loc = 'saved_models/text_model.txt'  # markov model we'll load
        text_model = generate_sentences.load_markov_model(markov_model_loc)
        fake_titles = generate_sentences.generate_text(text_model, n_sentences=n_titles, tries=100)

    fake_titles_markdown = [latex2markdown(title).to_markdown() for title in fake_titles]

    html = render_template(
        'embed_simple.html',
        fake_titles=fake_titles_markdown
    )

    return html


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))


app.run(host='0.0.0.0', port=port)
