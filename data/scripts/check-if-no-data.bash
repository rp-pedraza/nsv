#!/usr/bin/env bash

# This script would check if the current ElasticSearch instance has no
# data yet.

ELASTICSEARCH_ADDRESS=${1-http://nsv-es:9200}
ELASTICSEARCH_INDEX_ADDRESS=${ELASTICSEARCH_ADDRESS}/nmap_scans
ELASTICSEARCH_INDEX_TYPE_ADDRESS=${ELASTICSEARCH_INDEX_ADDRESS}/default
PROCESSED_DATA_LOCATION='./data.processed'

echo "Checking if ${ELASTICSEARCH_INDEX_ADDRESS} already exists."

CODE=$(curl "${ELASTICSEARCH_INDEX_ADDRESS}" -w'%{http_code}' -o/dev/null 2>/var/tmp/check-if-no-data.error)

case ${CODE} in
200)
	echo "It does."
	# It exists already.  Return "false".
	exit 1
	;;
404)
	echo "It doesn't yet."
	# It doesn't exist.  Return "true".
	exit 0
	;;
*)
	echo "An unexpected error occurred.  Returned code was ${CODE}."
	echo "Error message was \"$(</var/tmp/check-if-no-data.error)\"."
	# We're not sure about this.  Return anything other than 0 or 1.
	# Any script calling this script should consider aborting the
	# operation.
	exit 255
	;;
esac
