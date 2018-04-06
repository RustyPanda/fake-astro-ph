import subprocess

from pymongo import MongoClient

import functools

import ads_to_mongodb
import train_embedding
import generate_sentences

embedding_save_loc = 'word2vec_embeddings/all_arxiv_embedding.txt'
markov_model_loc = 'saved_models/text_model.txt'  # markov model we'll load

fresh_download = True
fresh_embedding = True
fresh_markov_model = True

# connect
client = MongoClient()  # default host/port

# # create/connect to instance database
db = client.all_arxiv_database
ads_papers = db.ads_papers  # collection

if fresh_download:
    ads_to_mongodb.save_ads_to_collection(ads_papers, query_max_rows=2000)

# check there's something in mongodb
# TODO use assert
# print(ads_papers.find_one())

corpus = train_embedding.Corpus(papers=ads_papers)  # save the collection in a corpus object with yield method
if fresh_embedding:
    embedding = train_embedding.get_vectors(corpus, save_loc=embedding_save_loc)

if fresh_markov_model:
    text_model = generate_sentences.make_markov_model(
        functools.reduce(lambda current, next: next + '. ' + current, corpus.titles),
        savename=markov_model_loc)
else:
    text_model = generate_sentences.load_markov_model(markov_model_loc)

sentences = generate_sentences.generate_text(text_model, n_sentences=20, tries=100)

for s in sentences:
    print(u'{}'.format(s).capitalize())
    print('\n')

db.eval("db.shutdownServer()")