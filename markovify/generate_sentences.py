import markovify
import re
import spacy
from unidecode import unidecode
import json




class SpacyText(markovify.Text):
    """
    A class to integrate Spacy with Markovify. Mostly taken from
    https://joshuanewlan.com/spacy-and-markovify with a few edits
    """

    @classmethod
    def from_dict(cls, obj, **kwargs):
        return cls(
            None,
            state_size=obj["state_size"],
            chain=markovify.Chain.from_json(obj["chain"]),
            parsed_sentences=obj.get("parsed_sentences")
        )

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))


    def sentence_split(self, corpus):
        """
        Splits full-text string into a list of sentences.
        """
        sentence_list = []
        for sentence in corpus.sents:
            sentence_list.append(sentence)

        return sentence_list

    def word_split(self, sentence):
        """
        Splits a sentence into a list of words.
        """
        return ["::".join((word.orth_,word.pos_)) for word in sentence]

    def word_join(self, words):
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

    def load_spacy(self, embedding):


        nlp = spacy.load(embedding)
        nlp.add_pipe(nlp.create_pipe('sentencizer'))

        
        return nlp

    def generate_corpus(self, text):
        """
        Given a text string, returns a list of lists; that is, a list of
        "sentences," each of which is a list of words. Before splitting into 
        words, the sentences are filtered through `self.test_sentence_input`
        """
        embedding='en_vectors_web_lg'
        nlp=self.load_spacy(embedding)
        corpus=nlp(text)
        sentences = self.sentence_split(corpus)
        passing = filter(self.test_sentence_input, sentences)
        runs = map(self.word_split, sentences)

        return runs



def load_text_from_txtfile(fname):

    # Get raw text as string.
    import io
    with io.open(fname, "r", encoding="utf-8") as f:
        text = f.read() 

    return text

def get_text_from_db(db):

    return text


def build_model(text, textClass=None):

    if textClass is None:
        textClass=markovify.Text

    text_model = textClass(text)

    return text_model


def make_sentences(text_model, n_sentences, **kwargs):
    # Print five randomly-generated sentences
    sentences=[]
    for i in range(n_sentences):
        sentences.append((text_model.make_sentence(**kwargs)))

    return sentences




if __name__=='__main__':


    markov_model_fname_to_load='text_model.txt'
    generate_Markov_Model=False

    simple_testing=True
    save=True
    savename='text_model.json'

    if generate_Markov_Model or markov_model_fname_to_load is None:

        
        if simple_testing:
            fname='../example_corpus/abstracts.txt'
            text=load_text_from_txtfile(fname)
        else:
            #TODO load text from DB
            text=None
            

        # Build the model.
        text_model=build_model(text, textClass=SpacyText)
        model_json = text_model.to_json()
        if save:
            with open(savename, 'w') as outfile:
                json.dump(model_json, outfile)


    else:
        with open(markov_model_fname_to_load, 'r') as f:
            markov_model=json.load(f)
        text_model = SpacyText.from_json(markov_model)


    #print sentences
    sentences=make_sentences(n_sentences=10, text_model=text_model, tries=100, test_output=True)

    for s in sentences:
        print u'{}/n'.format(s)