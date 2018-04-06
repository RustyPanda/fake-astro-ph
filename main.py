import subprocess

from pymongo import MongoClient

import ads_to_mongodb

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

fresh_download = False

# connect
client = MongoClient()  # default host/port

# # create/connect to instance database
db = client.test_database
ads_papers = db.ads_papers  # collection

if fresh_download:
    ads_to_mongodb.save_ads_to_collection(ads_papers, query_max_rows=2000)

# check there's something in mongodb
print(ads_papers.find_one())


db.eval("db.shutdownServer()")
