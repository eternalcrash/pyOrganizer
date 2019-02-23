"""
Module to get the dbpedia URI from a given query string
using a SPARQL query with the dbo:wikiPageID
and a wikipedia api search (wikipedia uses elastic search)
https://github.com/goldsmith/Wikipedia

Needs the SPARQLWrapper lib
https://github.com/RDFLib/sparqlwrapper
"""
from SPARQLWrapper import SPARQLWrapper, JSON
import wikipedia


sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)


def find_by_name(name, limit=5):
    page = None
    try:
        page = wikipedia.page(name)
    except Exception as e:
        # No found results
        print(e)
        return None
    sparql.setQuery("""
        select ?entity
        where {{
            ?entity dbo:wikiPageID {pageid}.
        }}
    """.format(pageid=page.pageid))
    results = sparql.query().convert()
    return results['results']['bindings'][0]['entity']['value']


if __name__ == "__main__":
    # main for test purposes
    r = find_by_name("Barack")
    from pprint import pprint
    pprint(r)
    
