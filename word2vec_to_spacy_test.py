import pytest

import word2vec_to_spacy


@pytest.fixture
def test_embedding_loc():
    return 'test_examples/test_embedding.txt'


def test_load_embedding_as_dict(test_embedding_loc):
    embedding_dict = word2vec_to_spacy.load_word2vec_as_dict(test_embedding_loc)
    print(embedding_dict)


def test_load_spacy_vocab_from_word2vec(test_embedding_loc):
    nlp = word2vec_to_spacy.load_spacy_nlp_from_word2vec(test_embedding_loc)
    print(nlp)

    tokens = nlp(u'of the in and')  # included in the example embed file
    for token in tokens:
        print(token.text, token.has_vector, token.vector_norm, token.is_oov)
