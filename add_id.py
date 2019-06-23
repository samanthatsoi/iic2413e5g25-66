import json

with open("messages.json", "r") as jsonFile:
    data = json.load(jsonFile)
    
i = 0
for message in data:
    message["id"] = i
    i += 1

with open("messages.json", "w") as jsonFile:
    json.dump(data, jsonFile)