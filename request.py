from requests import exceptions
from pathlib import Path
import progressbar
import argparse
import requests
import cv2
import os
 
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
ap.add_argument("-k", "--key", required=True,
	help="bing api key")
ap.add_argument("-m", "--max_results", default=250,
	help="maximum images to download | default=250")
ap.add_argument("-g", "--group_size", default=50,
	help="results per request | default=50")
args = vars(ap.parse_args())

API_KEY = args["key"]
MAX_RESULTS = int(args["max_results"])
GROUP_SIZE = int(args["group_size"]) 
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

output = Path(args["output"])
output.mkdir(parents=True, exist_ok=True)

query = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": query, "offset": 0, "count": GROUP_SIZE}
 
print("[INFO] searching Bing API for '{}'".format(query))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()
 
results = search.json()
numResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(numResults, query))
 
total = 0

# TODO: verify pep 8
bar = progressbar.ProgressBar(maxval=numResults, \
                              widgets=[progressbar.Bar('=', 
                                       '[', ']'), 
                                       ' ', 
                                       progressbar.Percentage()
                                       ]
                              )
bar.start()
for offset in range(0, numResults, GROUP_SIZE):
    params["offset"] = offset
    search = requests.get(URL, headers=headers, params=params)
    search.raise_for_status()
    results = search.json()

    for value in results["value"]:
        try:
            req = requests.get(value["contentUrl"], timeout=30)

            ext = value["contentUrl"][value["contentUrl"].rfind("."):]
            path = os.path.sep.join([args["output"], "{}{}.jpg".format(
                str(total).zfill(8), ext.slipt(".jpg")[0])])

            f = open(path, "wb")
            f.write(req.content)
            f.close()

        # TODO: verify pep 8
        except Exception as e:
            if type(e) in [IOError,
                           FileNotFoundError,
                           exceptions.RequestException,
                           exceptions.HTTPError,
                           exceptions.ConnectionError,
                           exceptions.Timeout
                          ]:
                print("[INFO] skipping: {}".format(value["contentUrl"]))
                continue
        
        image = cv2.imread(path)

        if image is None:
            print("[INFO] deleting: {}".format(path))
            os.remove(path)
            continue

        total += 1
        bar.update(total)
print("[INFO] Done!")