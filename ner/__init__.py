"""
Module to find Named entities
using pattern and nltk
"""
from . import ner_es
from . import ner_en

valid_langs = ['es', 'en']

by_lang_class = {
    'es': ner_es.SpanishNER,
    'en': ner_en.EnglishNER,
}

by_lang_created_ners = {}


def get_ner(lang):
    """
    create a new Ner class if its not already created
    """
    if lang not in by_lang_created_ners:
        by_lang_created_ners[lang] = by_lang_class.get(lang)() 
    return by_lang_created_ners[lang]


def find_entities(text, lang):
    """
    Return the list of possible named entities found in the passed text, as
    a nested list of strings (list of token lists)
    The lang argument is used to use the submodule for that lang.

    Each lang module may use diferent libs / techniques but all should return
    the expected list of list of tokens
    """
    ner = get_ner(lang)
    return ner.find_entities(text)
