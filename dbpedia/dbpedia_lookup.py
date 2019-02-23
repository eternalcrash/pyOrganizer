"""
Module to get the dbpedia URI from a given query string
using the lookup DBPedia Lookup Service
    https://github.com/dbpedia/lookup

see dbpedia_lookup function below


Example:
http://lookup.dbpedia.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=berl


Could be use as cli script to get the 5 uris from the given string

Note: it seems to find only data from :
    DBpedia Lookup currently contains data from DBpedia 3.8. 
    Resources of redirect
"""

import sys
import requests
import logging
logging.basicConfig()

service_endpoint = "http://lookup.dbpedia.org/api/search/PrefixSearch"


def dbpedia_lookup(query_str, query_class='', max_hits=5):
    """
    Retrieves the [max_hits] matching URIs from DBPedia using
    Dbpedia Lookup Service
    query_class could be used to specify the class of the target resource
    """
    params = build_query_params(query_str, query_class, max_hits)
    response_dict = do_request(params)
    uris = [result['uri'] for result in response_dict['results']]
    return uris


def build_query_params(query_str, query_class, max_hits):
    """
        takes the input string, query_class (can be empty) and max_hits and
        returns a dict with the required GET paramets for the service

    """
    return {
        'QueryClass': query_class,
        'QueryString': query_str,
        'MaxHits': max_hits
    }


def do_request(params):
    """
        Perform the GET call using requests lib using the passed options
        and the default_headers defined in this module
    """
    default_headers = {'Accept': 'application/json'}
    r = requests.get(service_endpoint, params=params, headers=default_headers)
    return r.json()


def set_log_level(level):
    """
        Use this passing level=logging.DEBUG to see the actual requests
        sent to the endpoint
    """
    logging.getLogger().setLevel(level)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(level)
    requests_log.propagate = True


if __name__ == '__main__':
    if len(sys.argv) == 2:
        uris = dbpedia_lookup(sys.argv[1])
        print(uris)
    else:
        print('USAGE: python3 dbpedia_lookup.py [query]')
