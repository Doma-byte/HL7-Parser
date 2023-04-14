import json
from datetime import datetime
import pymongo
import re

client = pymongo.MongoClient(
    "mongodb://localhost:27017/")
db = client["analyser_data"]
collection = db["Analyser_data_2"]

input_file = "new_data2.json"

with open(input_file, "r") as f:
    json_string = f.read()
    start_idx = json_string.find('"mydata": "') + len('"mydata": "')
    end_idx = json_string.find('}"', start_idx)
    mydata = json_string[start_idx:end_idx].replace('\\','')
    mydata = mydata.replace('"','')
    raw_data = json_string[:start_idx]+mydata+json_string[end_idx:]+'\n'

data = json.loads(raw_data)
mydata = data['mydata'][1:-1]
mydata = mydata.split(',')

formatted_data = []

unformatted_data = []

mydata1 = mydata[0]
result_parts = re.split(r'\||\|\||\|\|\||\|\|\|\|',mydata1)
unformatted_data.append(result_parts)

new_list = unformatted_data[0][:4]
parts = new_list[0].split("^")
parts1 = new_list[3].split("^")
test_code = parts[0]
test_name = parts[1]
system = parts[2]
result = new_list[2]
units = parts1[0]
units_system = parts1[1]+parts1[2]
formatted_data.append({
    'test_code': test_code,
    'test_name': test_name,
    'system': system,
    'result': result,
    'units': units,
    'units_system': units_system,
})

data = json.loads(raw_data)

data['mydata'] = formatted_data

now = datetime.now()
data['Date'] = now.strftime('%Y-%m-%d')
data['Time'] = now.strftime('%H:%M:%S')

del data['_id']

formatted_data = json.dumps(data, indent=4)
document = json.loads(formatted_data)

# #For inserting into database
result = collection.insert_one(document)

# #Printing the result
print(result.inserted_id)