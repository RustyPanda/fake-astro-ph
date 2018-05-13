
import numpy as np
import spacy


def load_word2vec_as_dict(embedding_loc):
    embedding_dict = {}
    with open(embedding_loc) as f:
        content = f.readlines()
        for row in content[1:]:  # skip first line, it's word2vec metadata
            elements = row.split()
            word = elements[0]
            values = elements[1:]
            embedding_dict[word] = np.array(values).astype(float)
    return embedding_dict


def load_spacy_nlp_from_word2vec(word2vec_loc, save_loc=None):
    nlp = spacy.blank('en')
    vocab_dict = load_word2vec_as_dict(word2vec_loc)
    for word, vector in vocab_dict.items():
        nlp.vocab.set_vector(word, vector)

    if save_loc is not None:
        nlp.to_disc(save_loc)

    return nlp
