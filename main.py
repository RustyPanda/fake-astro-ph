import itertools
import io

from pymongo import MongoClient

from downloader import ads_to_mongodb
from embedder import train_embedding
from randomiser import generate_sentences

embedding_loc = 'data/word2vec_embeddings/all_arxiv_titles_abstracts_embedding.txt'
markov_model_loc = 'data/saved_models/all_arxiv_titles_abstracts_model.txt'

fresh_download = False
fresh_embedding = False
fresh_markov_model = False
cache_titles = True

# expects running mongodb instance
# In shell: mongod --dbpath ~/mongodb/data/db.

# connect
client = MongoClient()  # expects default host/port

# create/connect to instance database
db = client.all_arxiv_database
ads_papers = db.ads_papers  # collection

if fresh_download:
    ads_to_mongodb.save_ads_to_collection(ads_papers, query_max_rows=2000)

# check there's something in mongodb
# TODO use assert
# print(ads_papers.find_one())

corpus = train_embedding.Corpus(papers=ads_papers)  # save the collection in a corpus object with yield method
if fresh_embedding:
    embedding = train_embedding.embed_corpus(corpus, save_loc=embedding_loc)


if fresh_markov_model:
    n_titles = 10000000  # load in memory only n titles (for speed)
    selected_titles = itertools.islice(corpus.get_titles(ads_keyword='Astrophysics - Astrophysics of Galaxies'), n_titles)
    all_titles_string = '. '.join(selected_titles)
    markov_model = generate_sentences.make_markov_model(
        all_titles_string,
        save_loc=markov_model_loc,
    )

else:
    markov_model = generate_sentences.load_markov_model(markov_model_loc)

title_kwargs = dict(max_chars=700, min_chars=100, tries=100)
titles = generate_sentences.generate_text(markov_model, n_sentences=1000, sentence_params=title_kwargs)


if cache_titles:
    with io.open('data/cached_titles/titles.txt', mode='w') as f:
        f.write( '\n'.join(titles))
else:
    for s in titles:
        print(u'{}'.format(s))
        print('\n')

db.eval("db.shutdownServer()")
