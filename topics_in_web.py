"""
This module uses the goose lib to extract cleaned text from a web page.
Then tries to applie the functions in our NER
dbpedia module to extract
resouces mentioned in that page
(this could be used later for classification and other tasks)
"""
import sys
import ner
from dbpedia import dbpedia_find_by_name
import requests
from goose3 import Goose
from clint import arguments
from clint.textui import puts, indent, colored


# TODO extract lang from metadata
def topics_in_web(url, lang="es", max_entities=4):
    """
    Return the dbpedia resources found in the page from the passed URL
    """
    g = Goose()
    article = g.extract(url=url)
    text = article.cleaned_text
    entities = ner.find_entities(text, lang)
    found_entities = [
        dbpedia_find_by_name.find_by_name(entity, limit=1, lang=lang)
        for entity in entities[:max_entities]
    ]
    return list(zip(entities, found_entities))


def url_ok(url):
    r = requests.head(url)
    return r.status_code == 200


def usage():
    puts('Topics in web: script to get dbpedia resources from a web page')
    puts('USAGE:')
    with indent(4):
        puts('python topics_in_web.py URL [lang]')


if __name__ == "__main__":
    args = arguments.Args()
    if len(args) == 0:
        usage()
        sys.exit(0)  # end here after showing help if no url
    url = args.get(0)
    try:
        if not url_ok(url):
            raise
    except Exception:
        print("error getting URL: ", url)
        sys.exit(1)
    else:
        results = topics_in_web(url)
        for topic, entity in results:
            puts(str(topic))
            with indent(4):
                if entity:
                    puts(colored.green(entity))
                else:
                    puts(colored.red("None"))
