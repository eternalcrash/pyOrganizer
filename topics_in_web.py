"""
This module uses the goose lib to extract cleaned text from a web page.
Then tries to applie the functions in our NER
dbpedia module to extract
resouces mentioned in that page
(this could be used later for classification and other tasks)
"""
import ner
from dbpedia import dbpedia_find_by_name
from goose3 import Goose


# TODO extract lang from metadata
def topics_in_web(url, lang="es"):
    """
    Return the dbpedia resources found in the page from the passed URL
    """
    g = Goose()
    article = g.extract(url=url)
    text = article.cleaned_text
    entities = ner.find_entities(text, lang)
    # TODO for now since we are using dpbedia API , use only the first 4
    max_entities = 4
    found_entities = [
        dbpedia_find_by_name.find_by_name(entity, limit=1)
        for entity in entities[:max_entities]
    ]
    return list(zip(entities, found_entities))


if __name__ == "__main__":
    # main for test purposes
    results = topics_in_web.topics_in_web("https://www.vozpopuli.com/economia-y-finanzas/sanchez-coloca-jefa-seguridad-hipodromo-zarzuela_0_1220879023.html")
    for topic, entity in results:
        print(topic, "--->", entity)
