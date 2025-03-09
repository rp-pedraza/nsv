#!/usr/bin/env python3

from time import sleep
import requests
import sys

try:
    uri = sys.argv[1]
except IndexError:
    print("URI not specified.", file=sys.stderr)
    exit(1)

print(f"Waiting for valid response from '{uri}'.")

serviceReady = False
while not serviceReady:
    try:
        response = requests.get(uri)
        serviceReady = response.status_code == 200
    except Exception:
        sleep(1)
        pass
