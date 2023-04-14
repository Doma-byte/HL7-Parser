import json
from datetime import datetime
import pymongo

client = pymongo.MongoClient(
    "mongodb://localhost:27017/")
db = client["analyser_data"]
collection = db["Analyser_data_1"]

input_file = "new_data1.json"

with open(input_file, "r") as f:
    json_string = f.read()
    start_idx = json_string.find('"mydata": "') + len('"mydata": "')
    end_idx = json_string.find('}"', start_idx)
    mydata = json_string[start_idx:end_idx].replace('\\','')
    mydata = mydata.replace('"','')
    raw_data = json_string[:start_idx]+mydata+json_string[end_idx:]+'\n'

data = json.loads(raw_data)
mydata = data['mydata'][1:-1]
mydata = mydata.split(",")
formatted_data = []

unformatted_data = []

mydata1 = mydata[6:28]
for result in mydata1:
    result_parts = result.split('|' or '||')
    unformatted_data.append(result_parts)

for i in range(4, 22):
    del unformatted_data[i][0]

for i in range(4, 22):
    del unformatted_data[i][0]

for i in range(4, 22):
    del unformatted_data[i][0]

for data in unformatted_data:
    parts = data[0].split("^")
    test_code = parts[0]
    name = parts[1]
    system = parts[2]
    result = data[2]
    units = data[3]
    normal_range = data[4]
    flag = data[5]
    formatted_data.append({
        'test_code': test_code,
        'name': name,
        'system': system,
        'result': result,
        'units': units,
        'normal_range': normal_range,
        'flag': flag,
    })

data = json.loads(raw_data)

data['mydata'] = formatted_data

now = datetime.now()
data['Date'] = now.strftime('%Y-%m-%d')
data['Time'] = now.strftime('%H:%M:%S')

del data['_id']

formatted_data = json.dumps(data, indent=4)

document = json.loads(formatted_data)

#For inserting into database
result = collection.insert_one(document)

#Printing the result
print(result.inserted_id)