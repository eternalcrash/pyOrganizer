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
import logging

sparql_lang = {
    'en': SPARQLWrapper("http://dbpedia.org/sparql"),
    'es': SPARQLWrapper("http://es.dbpedia.org/sparql"),
}
for sparql in sparql_lang.values():
    sparql.setReturnFormat(JSON)


def find_by_name(name, limit=5, lang='en'):
    wikipedia.set_lang(lang)
    page = None
    try:
        page = wikipedia.page(name)
    except Exception as e:
        # No found results
        logging.debug(e)
        return None
    sparql = sparql_lang.get(lang)
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        select ?entity
        where {{
            ?entity dbo:wikiPageID {pageid}.
        }}
    """.format(pageid=page.pageid))
    results = sparql.query().convert()
    resources = results['results']['bindings']
    if resources:
        return resources[0]['entity']['value']
    return "wiki_pageid_not_found ({url}):{pageid}".format(
        url=page.url, pageid=page.pageid
    )


if __name__ == "__main__":
    # main for test purposes
    r = find_by_name("Barack")
    from pprint import pprint
    pprint(r)
