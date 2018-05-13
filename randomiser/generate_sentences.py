
import re
import json
from unidecode import unidecode

import markovify

from embedder import word2vec_to_spacy


class SpacyText(markovify.Text):
    """
    A class to integrate Spacy with Markovify. Mostly taken from
    https://joshuanewlan.com/spacy-and-markovify with a few edits

    Inherits from markovify.Text. generate_corpus loads in our text, 
    wraps it in the nlp-ness of of spacey and then calls the markovify
    functions. 
    """

    @classmethod
    def from_dict(cls, obj, **kwargs):
        """
        create a class from a dictionary
        # Expects obj to have state_size, json-format chain and parsed_sentences attributes
        """
        return cls(
            None,
            state_size=obj["state_size"],
            chain=markovify.Chain.from_json(obj["chain"]),
            parsed_sentences=obj.get("parsed_sentences")
        )

    @classmethod
    def from_json(cls, json_str):
        """
        Create this class from a JSON
        """
        return cls.from_dict(json.loads(json_str))


    def sentence_split(self, corpus):
        """
        Splits full-text string into a list of sentences. 
        Inputs:
            self:
            corpus: a spacey document corpus (a 'doc'), with a .sents attribute 
        """
        return [sentence for sentence in corpus.sents]


    def word_split(self, sentence):
        """
        Splits a sentence into a list of words, with their .orth_ and .pos_
        attributes
        """
        return ["::".join((word.orth_,word.pos_)) for word in sentence]


    def word_join(self, words):
        """
        Join words together, ignoring the .pos_ attributes after the double
        semi colon
        """

        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


    def test_sentence_input(self, sentence):
        """
        A basic sentence filter. This one rejects sentences that contain
        the type of punctuation that would look strange on its own
        in a randomly-generated sentence. 
        """
        sentence = sentence.text
        reject_pat = re.compile(r"(^')|('$)|\s'|'\s|[\"(\(\)\[\])]")
        # Decode unicode, mainly to normalize fancy quotation marks
        if sentence.__class__.__name__ == "str":
            decoded = sentence
        else:
            decoded = unidecode(sentence)

        # Sentence shouldn't contain problematic characters
        if re.search(reject_pat, decoded): return False
        return True


    # TODO hard-coded embedding loc is stupid and should be changed
    def generate_corpus(self, text):
        """
        Given a text string, returns a list of lists; that is, a list of
        "sentences," each of which is a list of words. Before splitting into 
        words, the sentences are filtered through `self.test_sentence_input`
        """
        # create an nlp with a vocab of the word2vec embedding
        nlp = word2vec_to_spacy.load_spacy_nlp_from_word2vec(
            'data/word2vec_embeddings/all_arxiv_titles_abstracts_embedding.txt')
        nlp.add_pipe(nlp.create_pipe('sentencizer'))

        spacy_corpus=nlp(text)
        sentences = self.sentence_split(spacy_corpus)
        safe_sentences = filter(self.test_sentence_input, sentences)
        runs = map(self.word_split, safe_sentences)

        return runs


def make_markov_model(text, textClass=SpacyText, save_loc=None):
    """
    Build a Markovify text model, using either the base Text class
    or a custom one
    """
    if textClass is None:
        textClass = markovify.Text

    text_model = textClass(text)

    if save_loc:
        model_json = text_model.to_json()
        with open(save_loc, 'w') as outfile:
            json.dump(model_json, outfile)

    return text_model


def load_markov_model(fname):
    with open(fname, 'r') as f:
        markov_model = json.load(f)
    return SpacyText.from_json(markov_model)


def generate_text(text_model, n_sentences, sentence_params):
    # return randomly-generated short sentences
    return [text_model.make_short_sentence(**sentence_params) for n in range(n_sentences)]
