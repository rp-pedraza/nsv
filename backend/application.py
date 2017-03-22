from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
import requests
import json
import sys

from config import config

app = Flask(__name__)
CORS(app) # Prevent 'Cross Origin Requests Blocked'
api = Api(app)

parser = reqparse.RequestParser()

def is_string(s):
    if sys.version_info[0] >= 3:
        return isinstance(s, str)
    else:
        return isinstance(s, basestring)

def do_query(url, query):
    resp = requests.post(url, data = json.dumps(query))
    return resp.json()

class Root(Resource):
    def get(self):
        return {}

class Scans(Resource):
    def get(self):
        query = {
            'query': {
                'match_all': {}
            },
            'size': 100
        }

        data = do_query(config['es-search-url'], query);
        scans = []

        for hit in data['hits']['hits']:
            scan = hit['_source']
            scan['id'] = hit['_id']
            scans.append(scan)

        return scans

class Scan(Resource):
    def get(self, scan_id):
        url = config['es-base-url'] + '/' + scan_id
        resp = requests.get(url)
        data = resp.json()
        scan = data['_source']
        scan['id'] = scan_id
        return scan

class Search(Resource):
    def get(self):
        for arg in ['query', 'identity', 'address', 'hostname', 'state', 'tcpports', 'udpports']:
            parser.add_argument(arg)

        arguments = parser.parse_args()

        if (config['debug-mode']):
            print("Search arguments: " + json.dumps(arguments))

        subqueries = []

        if is_string(arguments['query']) and arguments['query']:
            subqueries.append({
                'bool' : {
                    'should' : [
                        {
                            'multi_match' : {
                                'fields' : ['identity', 'addresses.*', 'tcp.*.*', 'udp.*.*'],
                                'query' : arguments['query']
                            }
                        },
                        {
                            'nested' : {
                                'path' : 'hostnames',
                                'query' : {
                                    'match' : {
                                        'hostnames.name' : arguments['query']
                                    }
                                }
                            }
                        }
                    ]
                }
            })

        if is_string(arguments['identity']) and arguments['identity']:
            subqueries.append({
                'match' : {
                    'identity' : arguments['identity']
                }
            })

        if is_string(arguments['address']) and arguments['address']:
            subqueries.append({
                'match' : {
                    'addresses.*' : arguments['address']
                }
            })

        if is_string(arguments['hostname']) and arguments['hostname']:
            subqueries.append({
                'nested' : {
                    'path' : 'hostnames',
                    'query' : {
                        'match' : {
                            'hostnames.name' : arguments['hostname']
                        }
                    }
                }
            })

        if is_string(arguments['state']) and arguments['state']:
            subqueries.append({
                'match' : {
                    'status.state' : arguments['state']
                }
            })

        if is_string(arguments['tcpports']) and arguments['tcpports']:
            ports = arguments['tcpports'].split()

            subsubqueries = []

            for port in ports:
                subsubqueries.append({
                    'exists' : {
                        'field' : 'tcp.' + port
                    }
                })

            subqueries.append({
                'bool' : {
                    'must' : subsubqueries
                }
            })

        if is_string(arguments['udpports']) and arguments['udpports']:
            ports = arguments['udpports'].split()

            subsubqueries = []

            for port in ports:
                subsubqueries.append({
                    'exists' : {
                        'field' : 'tcp.' + port
                    }
                })

            subqueries.append({
                'bool' : {
                    'must' : subsubqueries
                }
            })

        scans = []

        # Only do query if there has been at least one valid search parameter.

        if subqueries:
            query = {
                'query': {
                    'bool' : {
                        'must' : subqueries
                    }
                },
                'size': 100
            }

            if (config['debug-mode']):
                print("Query string: " + json.dumps(query))

            data = do_query(config['es-search-url'], query)

            for hit in data['hits']['hits']:
                scan = hit['_source']
                scan['id'] = hit['_id']
                scans.append(scan)

        return scans

class PortsFrequency(Resource):
    def get(self):
        query = {
            '_source': ['tcp', 'udp'],
            'query': {
                'match_all': {}
            },
            'size': 100
        }

        data = do_query(config['es-search-url'], query)

        frequency = {'tcp': {}, 'udp': {}}

        for hit in data['hits']['hits']:
            source = hit['_source']

            for key in ['tcp', 'udp']:
                if key in source and type(source[key]) is dict:
                    for port in source[key]:
                        frequency[key][port] = frequency[key].get(port, 0) + 1

        return frequency

class Activity(Resource):
    def get(self):
        query = {
            '_source': ['identity', 'tcp', 'udp', 'datetime'],
            'query': {
                'match_all': {}
            },
            'size': 100
        }

        data = do_query(config['es-search-url'], query)
        activity = []

        for hit in data['hits']['hits']:
            source = hit['_source']
            count = 0

            for key in ['tcp', 'udp']:
                if key in source and type(source[key]) is dict:
                    count += len(source[key])

            activity.append({ 'id': hit['_id'], 'identity': source['identity'],
                    'level': count, 'datetime': source['datetime'] })

        return activity

api.add_resource(Root, '/')
api.add_resource(Scans, '/scans')
api.add_resource(Scan, '/scans/<scan_id>')
api.add_resource(Search, '/search')
api.add_resource(PortsFrequency, '/ports-frequency')
api.add_resource(Activity, '/activity')

if __name__ == '__main__':
    app.run(host: 'localhost', port: '5000', debug = True)
