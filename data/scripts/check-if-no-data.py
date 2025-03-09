#!/usr/bin/env python3

# This script checks if the current ElasticSearch instance has no
# data yet.

import requests
import sys

ELASTICSEARCH_ADDRESS = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:9200"
ELASTICSEARCH_INDEX_ADDRESS = f"{ELASTICSEARCH_ADDRESS}/nmap_scans"
ELASTICSEARCH_INDEX_TYPE_ADDRESS = f"{ELASTICSEARCH_INDEX_ADDRESS}/default"
PROCESSED_DATA_LOCATION = './data.processed'

print(f"Checking if {ELASTICSEARCH_INDEX_ADDRESS} already exists.")

try:
    response = requests.head(ELASTICSEARCH_INDEX_ADDRESS)
    code = response.status_code

    if code == 200:
        print("It does.")
        exit(1)
    elif code == 404:
        print("It doesn't yet.")
        exit(0)
    else:
        print("An unexpected status code was returned: {code}", file=sys.stderr)
        exit(255)

except Exception as e:
    print(f"An error occurred:", file=sys.stderr)
    exit(255)
