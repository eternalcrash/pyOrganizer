"""
This file defines the class SpanishNER to find Named entities in Spanish
using pattern (for spanish: pattern.es)
(the goal is to find group of tokens that matches a nominal group)
"""
from . import ner
from . import tokenizer
import re
import pattern.es as pat_es


class SpanishNER(ner.AbstractNER):
    """
    Spanish implementation of the class AbstractNER.
    This class implements the method find_entities for spanish.
    On object creation will load a model 
    """
    def __init__(self):
        # tokenizers (loaded pickels with simple trained models)
        self.sent_tokenizer = tokenizer.SentenceTokenizer()
        self.word_tokenizer = self.sent_tokenizer.tokenizer

    def find_entities(self, text):
        """
        Return the list of possible named entities found in the passed text.
        The process is:
        - split the text in sentences and tokens
        - tag each sentence using pattern
        - use the defined tag grammar to match possible candidates
        - return the candidates with lenght <= 4
        """
        entity_candidates = []
        max_length = 4
        sentences = self.segment_text(text)
        for sentence in sentences:
            span_ls = self.find_entities_tokenls(sentence)
            found_ls = [
                    sentence[start:end] for start, end in span_ls
                    if end - start <= max_length
            ]
            entity_candidates.extend(found_ls)
        return entity_candidates

    def find_entities_tokenls(self, tokenls):
        """
            Return a list of tuples (start, end) of each
            chunk of the sentence that could be a named entity
        """
        token_tag_ls = self.pos_tag_tokenlist(tokenls)
        tagsequence = self.get_tag_sequence(token_tag_ls)
        # build chunks using regex of pos tags.
        # detailed pos tags in https://www.clips.uantwerpen.be/pages/MBSP-tags
        termpattern = re.compile(
            '(R.#)?(C.#)?(DT#)?(JJ#)?(((NN#){1,3}(EN#|IN#|PN#)(DT#)?'
            '(NN#|JJ#){0,3})'
            '|'
            '((NN#(- #)?)+(JJ#)*(CD#)*((RB#)?JJ#)*))')
        matches = termpattern.finditer(tagsequence)
        # builds tuples with start, end of the chunks (each postag has 3 chars)
        return [
            (
                int(match.start() / 3) + match.start() % 3,
                int(match.end() / 3) + match.end() % 3)
            for (match) in matches
        ]

    def get_tag_sequence(self, token_tag_tuple_list):
        """
            Get the part of speech tag of the tokens of the sentence
            Args:
                variations: if True, uses token annotations (variation fields)
            Returns:
                list of pos tags
        """
        tag_sequence = ""
        for token, tag in token_tag_tuple_list:
            # Consider IN "en" as EN
            if(str(token).lower() == "en" and tag == "IN"):
                tag_sequence += "EN#"
            # Consider IN "para" as PN (spanish only) #TODO
            elif(str(token).lower() == "para" and tag == "IN"):
                tag_sequence += "PN#"
            # Consider IN "por", "con" as CK
            elif(str(token).lower() in ["por", "con"] and tag == "IN"):
                tag_sequence += "CK#"
            # Consider / or - as / or -
            elif(str(token) in ("/", "-", "*") and tag == "."):
                tag_sequence += str(token) + " #"
            # Consider VBN as JJ
            elif tag == "VBN":
                tag_sequence += "JJ#"
            else:
                tag_sequence += tag[0] + (
                    tag[1] if len(tag) > 1 else " ") + "#"
        return tag_sequence

    def pos_tag_tokenlist(self, tokens):
        """
            Args:
                tokens: list of str tokens of the sentence
            Returns:
                A list of tuples of the form (word,pos_tag)
        """
        return pat_es.tag(tokens, tokenize=False)

    def segment_text(self, text):
        """
        return a list of tokens (ie nested lists of strings)
        the tokenization and segmentation uses a pre trained nltk model
        (see tokenizer.py).
        Also some dirty (perfectible) regex substitutions are used to improve
        """
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        text = re.sub(r'\.*\n\n', ".\n", text)
        text = re.sub(r';\n', ".\n", text)
        text = re.sub(r'(\.[\s\t]*)?[\s\t]*\n[\s\t]*[\-·\*•]', ".\n", text)
        text = re.sub(
            r'(\.[\s\t]*)?[\s\t]*\n[\s\t]*[0-9]+\.[0-9]+\s+', ".\n", text)
        text = re.sub(
            r'(\.[\s\t]*)?[\s\t]*\n[\s\t]*[0-9]+\s*[\.\-:]', ".\n", text)
        text = re.sub(
            r'([a-z1-9\)])[\s\t]*\n[\s\t]*([A-Z])', r"\1.\n\2", text)
        text = re.sub(
            r'((\s?-?[\w ]+\s?:\s?[a-z| |/]+)[;,])'
            r'((\s?-?[\w ]+\s?:\s?[a-z| |/]+)[;,]?)',
            r"\2" + ".\n" + r"\4" + ".\n", text)
        raw_sentences = self.sent_tokenizer.segment_text(text)
        return raw_sentences

    def word_tokenize(self, text, include_nl=False, include_whites=False):
        """
            Splits a string in a list of tokens
            Args:
                include_nl: include new line tokens
                include_whites: include white tokens
                retokenize: if True, retokenizes the sentence
        """

        tokens = self.word_tokenizer.tokenize(text)
        return [
            x for x in tokens if (
                (include_whites or not x.replace("\n", "a").isspace()) and
                (include_nl or not x == "\n")
                )
        ]
