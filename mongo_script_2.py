from os import fspath
import pymongo
import time
import subprocess
from pathlib import Path
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["0002_23_ana1"]
collection = db["0002_23_ana1"]

# Keep track of the most recent ID
most_recent_id = None

output_file = "new_data2.json"

while True:
    print("Running...")
    latest_doc = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
    if latest_doc['_id'] != most_recent_id:
        most_recent_id = latest_doc['_id']

        latest_doc['_id'] = str(latest_doc['_id'])

        with open(output_file,"w")as f:
            json.dump(latest_doc,f)
        
        subprocess.call(['python','Analyser_2.py'])

    # Wait for a bit before checking for new data again
    time.sleep(10)