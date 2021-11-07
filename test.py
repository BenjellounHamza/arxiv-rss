import json
import os
from jsonmerge import merge


namefiles = []

for root, dirs, files in os.walk("./database"):
    for name in files:
        if name.endswith((".json")) and "merged" not in name:
          namefiles.append(root + "/" + name)
          #print(root + name)


def merge_JsonFiles(filename):
    result = {}
    for f1 in filename:
        with open(f1) as infile:
            data = json.loads(infile.read())
            print(data[33])
            #result = merge(result, json.load(infile))
            break
    #print(result)
    #with open('./database/merged/data.json', 'w') as output_file:
    #    json.dump(result, output_file)

merge_JsonFiles(namefiles)