"""
Module to find Named entities
using the ner from the spacy lib
(this is a wrapper for that lib)
Note: this lib also has models for spanish but the es_ner.py dont use
this lib (it uses other two libs for the task: pattern and nltk)
"""

import spacy
from . import ner

"""
* Type of named entities *

from https://spacy.io/api/annotation

Type	Description
PERSON	People, including fictional.
NORP	Nationalities or religious or political groups.
FAC	Buildings, airports, highways, bridges, etc.
ORG	Companies, agencies, institutions, etc.
GPE	Countries, cities, states.
LOC	Non-GPE locations, mountain ranges, bodies of water.
PRODUCT	Objects, vehicles, foods, etc. (Not services.)
EVENT	Named hurricanes, battles, wars, sports events, etc.
WORK_OF_ART	Titles of books, songs, etc.
LAW	Named documents made into laws.
LANGUAGE	Any named language.
DATE	Absolute or relative dates or periods.
TIME	Times smaller than a day.
PERCENT	Percentage, including "%".
MONEY	Monetary values, including unit.
QUANTITY	Measurements, as of weight or distance.
ORDINAL	"first", "second", etc.
CARDINAL	Numerals that do not fall under another type.
"""
# The ones that will be returned by this Ner:
target_entity_labels = {
    "PERSON",
    "FAC",
    "ORG",
    "GPE",
    "LOC",
    "PRODUCT",
    "EVENT",
    "WORK_OF_ART",
}


class EnglishNER(ner.AbstractNER):
    """
    English implementation of the class AbstractNER.
    This class implements the method find_entities for english.
    On object creation will load the required spacy model
    """
    def __init__(self):
        # Load English tokenizer, tagger, parser, NER and word vectors
        self.nlp = spacy.load('en_core_web_sm')

    def find_entities(self, text):
        """
        Return the list of possible named entities found in the passed text.
        It selects only some of the entities detected by Spacy
        """
        doc = self.nlp(text)
        # Find named entities, phrases and concepts
        entities = [
            entity.text for entity in doc.ents
            if entity.label_ in target_entity_labels
        ]
        return entities
