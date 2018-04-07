import itertools

import gensim

class Corpus(object):


    def __init__(self, papers):
        self.papers = papers  # collection of papers
        self.abstracts = self.get_field_iterable('abstract')
        self.titles = self.get_field_iterable('title', fix_list=True)
        self.author = self.get_field_iterable('author')
        self.pubdate = self.get_field_iterable('pubdate')
        self.aff = self.get_field_iterable('aff')
        self.all_documents = itertools.chain(  # all abstracts then all titles, split into lists of words
            map(lambda x: list(gensim.utils.tokenize(x.lower())), self.abstracts),
            map(lambda x: list(gensim.utils.tokenize(x.lower())), self.titles)
        )


    def __iter__(self):
        # iterating over corpus is main use, will give list of list of title-words
        # TODO make this explicit
        cursor = self.papers.find({'title': {'$exists': True}})
        for paper_with_title in cursor:
            # [0] because ADS gives title as a list...
            yield paper_with_title['title'][0].lower().split()


    def get_field_iterable(self, field, arxiv_class=None, fix_list=False):
        query = {field: {'$exists': True}}
        if arxiv_class is not None:
            query.update({'keyword': arxiv_class })  # mongodb will check if 'keyword' list includes arxiv_class
        cursor = self.papers.find(query)
        for paper_with_field in cursor:
            if fix_list:
                assert len(paper_with_field[field]) == 1
                yield paper_with_field[field][0]  # full string if ADS API has wrapped in a list
            else:
                yield paper_with_field[field]  # original string, may include capitalisation


    def get_titles(self, ads_keyword=None):
        return self.get_field_iterable('title', arxiv_class=ads_keyword, fix_list=True)


def embed_corpus(corpus, save_loc=None):
    # see https://rare-technologies.com/word2vec-tutorial/
    # see https://radimrehurek.com/gensim/models/word2vec.html
    # all parameters: https://radimrehurek.com/gensim/models/word2vec.html#gensim.models.word2vec.Word2Vec
    print(next(corpus.all_documents))
    model = gensim.models.Word2Vec(corpus.all_documents, size=100, window=5, min_count=5, workers=4)
    if save_loc is not None:
        model.wv.save_word2vec_format(save_loc)
    return model
