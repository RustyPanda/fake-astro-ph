import subprocess

from pymongo import MongoClient


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

# # connect
client = MongoClient()  # default host/port
# #
# # create/connect to instance database
db = client.test_database
ads_papers = db.ads_papers # collection
# #
#
# #
db.eval("db.shutdownServer()")
