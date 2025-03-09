#!/usr/bin/env python3

import argparse
import json
import os
import requests
import sys

def die(message, *extra_args):
    print(message, *extra_args, file=sys.stderr)
    sys.exit(1)

def report_caught_status_code(response):
    print(f"Caught status code: {response.status_code}", file=sys.stderr)

def do_request(method_name, *args, **opts):
    method = getattr(requests, method_name.lower())

    try:
        response = method(*args, **opts)
    except requests.exceptions.ConnectionError as error:
        die("Connection error:", error)

    return response

def delete_existing_index(elasticsearch_index_address):
    print("Removing old index.")
    print("Please ignore 'no such index' error.")

    response = do_request("DELETE", elasticsearch_index_address)
    if response.status_code != 200 and response.status_code != 404:
        report_caught_status_code(response)
        die(f"Failed to delete existing index.")

def setup_mappings(elasticsearch_index_address):
    # See https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html
    # and https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html
    # for info about the "nested" type.

    print("Setting up mappings.")

    mapping_data = {
        "mappings": {
            "default": {
                "properties": {
                    "datetime": {"type": "double"},
                    "hostnames": {"type": "nested"}
                }
            }
        }
    }

    response = do_request("PUT", elasticsearch_index_address, json=mapping_data)
    if response.status_code != 200:
        report_caught_status_code(response)
        die("Failed to setup mappings.")

def upload_content(processed_data_location, filenames, elasticsearch_index_type_address):
    for i, file in enumerate(filenames):
        file_path = os.path.join(processed_data_location, file)
        print(f"Importing {file_path}.")

        with open(file_path, "r") as f:
            json_str = f.read()

        # IDs can also be automatically generated.
        # See https://www.elastic.co/guide/en/elasticsearch/reference/5.6/docs-index_.html#index-creation

        response = do_request("PUT",
                              f"{elasticsearch_index_type_address}/{i + 1}",
                              headers={"Content-Type": "application/json"},
                              data=json_str)

        if response.status_code != 201:
            report_caught_status_code(response)
            die(f"Failed to upload data to index: \n{json_str}")

def main():
    default_processed_data_location = os.path.join(os.path.dirname(__file__), "..", "data.processed")

    parser = argparse.ArgumentParser(prog="import-processed-data",
                                     description="Imports processed NSV data to Elasticsearch instance")
    parser.add_argument("elasticsearch_address", nargs="?", default="http://localhost:9200",
                        help="Defaults to 'http://localhost:9200'")
    parser.add_argument("-d", "--data",
                        help=f"Processed data location instead of '{default_processed_data_location}'",
                        nargs=1, default=default_processed_data_location, dest="processed_data_location")
    parser.add_argument("-y", "--yes", help="Imply yes to all prompts", action="store_true", dest="yes")
    args = parser.parse_args()

    elasticsearch_address = args.elasticsearch_address
    elasticsearch_index_address = elasticsearch_address + "/nmap_scans"
    elasticsearch_index_type_address = elasticsearch_index_address + "/default"

    processed_data_location = args.processed_data_location

    if not os.path.isdir(processed_data_location):
        die(f"{processed_data_location} does not exist.")

    filenames = [f for f in os.listdir(processed_data_location) if f.endswith(".json")]
    if not filenames:
        die(f"No data were found in '{processed_data_location}'.")

    if args.yes or input("This will delete existing data. Continue? [y/N] ").lower() == "y":
        delete_existing_index(elasticsearch_index_address)
        setup_mappings(elasticsearch_index_address)
        upload_content(processed_data_location, filenames, elasticsearch_index_type_address)
        print("Done.")

if __name__ == "__main__":
    main()
