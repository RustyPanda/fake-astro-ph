import pytest
import generate_sentences as G
import markovify
import os

@pytest.fixture
def get_fname():
    fname='../example_corpus/abstracts.txt'
    return fname

@pytest.fixture
def get_text_corpus():
    fname=get_fname()
    corpus=G.load_corpus(fname)
    return corpus

@pytest.fixture
def get_text_model():
    fname=get_fname()
    corpus=G.load_corpus(fname)
    model=G.build_model(corpus)

    return model


def test_if_exists(get_fname):
    assert os.path.exists(get_fname)

def test_load_corpus_type(get_fname):

    text=G.load_corpus(get_fname)
    assert type(text) is str

def test_build_model_type(get_text_corpus):

    text_model=G.build_model(get_text_corpus)

    assert type(text_model) is markovify.text.Text

def test_make_sentences(get_text_model):

    n_sentences=5
    sentences=G.make_sentences(get_text_model, n_sentences=n_sentences)

    assert len(sentences)==n_sentences







