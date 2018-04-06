import markovify
import re
import spacy
from unidecode import unidecode





class POSifiedText(markovify.Text):


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

    def generate_corpus(self, text):
        """
        Given a text string, returns a list of lists; that is, a list of
        "sentences," each of which is a list of words. Before splitting into 
        words, the sentences are filtered through `self.test_sentence_input`
        """
        nlp = spacy.load('en_vectors_web_lg')
        corpus=nlp(text)
        sentences = self.sentence_split(corpus)
        passing = filter(self.test_sentence_input, sentences)
        runs = map(self.word_split, sentences)

        return runs



def load_text(fname):

    # Get raw text as string.
    import io
    with io.open(fname, "r", encoding="utf-8") as f:
        text = f.read() 

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


    fname='../example_corpus/abstracts.txt'
    text=load_text(fname)

    


    # Build the model.
    text_model=build_model(text, textClass=POSifiedText)

    #print sentences
    sentences=make_sentences(n_sentences=5, text_model=text_model, tries=100, test_output=True)

    for s in sentences:
        print s


