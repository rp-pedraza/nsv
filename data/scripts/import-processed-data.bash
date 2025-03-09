#!/usr/bin/env bash

_elasticsearch_address='localhost:9200'
_elasticsearch_index_address=${_elasticsearch_address}/nmap_scans
_elasticsearch_index_type_address=${_elasticsearch_index_address}/default
_processed_data_location=()

function die {
	echo "$1" >&2
	exit "${2-1}"
}

function assign_default_processed_data_location {
	local location=${BASH_SOURCE-__invalid__}
	[[ ${location} == /* ]] || location=${PWD}/${location}
	_processed_data_location=$(cd "${location%/*/*}/data.processed" && pwd -P) || exit
}

function display_usage {
	assign_default_processed_data_location

	echo "Usage: import-processed-data [-h] [-d processed_data_location] [-y] [elasticsearch_address]

Imports processed NSV data to Elasticsearch instance

Positional arguments:
  elasticsearch_address  Defaults to 'localhost:9200'

Options:
  -d, --data location  Processed data location instead of '${_processed_data_location}'
  -h, --help           Show this help message and exit
  -y, --yes            Imply yes to all prompts"
}

function delete_existing_index {
	echo "Removing old index."
	echo "Please ignore 'no such index' error."
	curl -XDELETE "${_elasticsearch_index_address}" || die "Failed to delete existing index."
	echo
}

function setup_mappings {
    # See https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-nested-query.html
    # and https://www.elastic.co/guide/en/elasticsearch/reference/current/nested.html
    # for info about the "nested" type.

	echo "Setting up mappings."

	curl -XPUT "${_elasticsearch_index_address}" -d '{
		"mappings" : {
			"default" : {
				"properties" : {
					"datetime" : { "type" : "double" },
					"hostnames": { "type" : "nested" }
				}
			}
		}
	}' || die "Failed to setup mappings."

	echo
}

function upload_content {
	local data_file id=1 json_str

	for data_file do
		echo "Importing ${data_file}."
		json_str=$(<"${data_file}")

		# IDs can also be automatically generated.
		# See https://www.elastic.co/guide/en/elasticsearch/reference/5.6/docs-index_.html#index-creation

		curl -XPUT "${_elasticsearch_index_type_address}/${id}" -H'Content-Type: application/json' -d"${json_str}" || {
			die "Failed to upload data to index: "$'\n'"${json_str}"
			break
		}

		echo
		(( ++id ))
	done
}

function main {
	local args=() i json_str yes=false

	while [[ $# -gt 0 ]]; do
		case $1 in
		-d|--data)
			_processed_data_location=$2
			shift
			;;
		-y|--yes)
			yes=true
			;;
		-h|--help)
			display_usage
			return 1
			;;
		-*)
			die "Invalid option: $1"
			;;
		*)
			args+=("$1")
			;;
		esac

		shift
	done

	_elasticsearch_address=${args-localhost:9200}
	_elasticsearch_index_address=${_elasticsearch_address}/nmap_scans
	_elasticsearch_index_type_address=${_elasticsearch_index_address}/default

	[[ ${_processed_data_location+.} ]] || assign_default_processed_data_location || exit
	[[ -d ${_processed_data_location} ]] || die "${_processed_data_location} does not exist."

	data_files=("${_processed_data_location}"/*.json)
	[[ ${#data_files[@]} -gt 0 ]] || die "No data were found in '${_processed_data_location}'."

	if [[ ${yes} == true ]] ||
			{ read -p "This will delete existing data. Continue? [y/N] " && [[ ${REPLY} == [yY] ]]; }; then
		delete_existing_index
		setup_mappings
		upload_content "${data_files[@]}"
		echo "Done."
	fi
}

main "$@"
