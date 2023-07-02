import json
import glob

result = []
for f in glob.glob(r"C:\Users\rache\OneDrive\Documents\MScDissWork\Data\*.json"):
    with open(f, "rb") as infile:
        result.append(json.load(infile))

with open("merged2.json", "wb") as outfile:
     json.dump(result, outfile)