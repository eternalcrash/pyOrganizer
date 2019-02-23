"""
Base Abstract class for a Named Entity Recognition
to be implemented in each lang (eg: ner_en.py)
"""

from abc import ABC, abstractmethod


class AbstractNER(ABC):

    @abstractmethod
    def find_entities(self, text):
        """
        This method should be implemented for each language
        """
        pass
