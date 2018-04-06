import subprocess

from pymongo import MongoClient
import spacy

import ads_to_mongodb
import train_embedding

# ensure no running process
# subprocess.call(
#     [
#         'mongo',
#         'use admin',
#         'db.shutdownServer'
#      ], shell=True)

# assume already running
# start Daemon mongodb instance saving to dbpath with log at logpath
# mongod = subprocess.call('mongod --dbpath ~/mongodb/data/db', shell=True)
# mongod.terminate()

embedding_save_loc = 'galaxies_embedding.txt'

fresh_download = False
fresh_embedding = True


# connect
client = MongoClient()  # default host/port

# # create/connect to instance database
db = client.test_database
ads_papers = db.ads_papers  # collection

if fresh_download:
    ads_to_mongodb.save_ads_to_collection(ads_papers, query_max_rows=2000)

# check there's something in mongodb
# TODO use assert
print(ads_papers.find_one())

if fresh_embedding:
    corpus = train_embedding.Corpus(papers=ads_papers)  # save the collection in a corpus object with yield method
    embedding = train_embedding.get_vectors(corpus, save_loc=embedding_save_loc)

db.eval("db.shutdownServer()")

# TODO
# nlp = spacy.load(embedding_save_loc)
# tokens = nlp(u'galaxy star globular metallicity')
# for token in tokens:
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)
