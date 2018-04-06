import markovify
import re
import spacy
from unidecode import unidecode
import json




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
        sentence_list = []
        for sentence in corpus.sents:
            sentence_list.append(sentence)

        return sentence_list

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

    def load_spacy(self, embedding):
        """
        Load the embedding we'll use with spacy
        """

        nlp = spacy.load(embedding)
        #This was required when I changed from 'en' to en_vectors_web_lg.
        #Not entirely sure why?
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
        spacy_corpus=nlp(text)
        sentences = self.sentence_split(spacy_corpus)
        passing = filter(self.test_sentence_input, sentences)
        runs = map(self.word_split, sentences)

        return runs



def load_text_from_txtfile(fname):

    # Get raw text as string.
    # Ensure the encoding is handled properly!
    import io
    with io.open(fname, "r", encoding="utf-8") as f:
        text = f.read() 

    return text

def load_text_from_db(text_iterable):

    all_texts=list(text_iterable)
    return all_texts


def make_markov_model(text, textClass=SpacyText, savename=None):

    """
    Build a Markovify text model, using either the base Text class
    or a custom one
    """
    if textClass is None:
        textClass=markovify.Text

    text_model = textClass(text)
    
    if savename:
        model_json = text_model.to_json()
        with open(savename, 'w') as outfile:
            json.dump(model_json, outfile)

    return text_model


def load_markov_model(fname):

    with open(markov_model_fname_to_load, 'r') as f:
        markov_model=json.load(f)
    text_model = SpacyText.from_json(markov_model)

    return text_model



def generate_text(text_model, n_sentences, **kwargs):
    # return five randomly-generated sentences
    sentences=[]
    for i in range(n_sentences):
        sentences.append((text_model.make_sentence(**kwargs)))

    return sentences



if __name__=='__main__':

    #Filename of the markov model we'll load
    #and whether to generate it again
    markov_model_fname_to_load='saved_models/text_model.txt'
    generate_Markov_Model=False


    
    #Do we want to save our model?
    save=True
    savename='saved_models/text_model.json'

    text=load_text_from_txtfile(fname='../example_corpus/abstracts.txt')

    if generate_Markov_Model:
        text_model=make_markov_model(text, savename=None, simple_testing=True)
    else:
        text_model=load_markov_model(markov_model_fname_to_load)

    sentences=generate_text(text_model, n_sentences=5, tries=100)

    for s in sentences:
        print u'{}'.format(s)
        print '\n'