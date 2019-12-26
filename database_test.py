# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017")
# db = client['botnet']
# bots = db.bots

# data = [
#     {'ip':'192.168.1.1','last-seen':'5 min'}    
# ]

# bots.insert_many(data)

from database_management import *
