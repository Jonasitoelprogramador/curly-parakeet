import re

from bs4 import NavigableString, Tag

import logging


class Sentence:
    def __init__(self, text, fragments, word_order):
        # Define the URL for the Wikimedia REST API for the 'Caramel' page
        self.text = text
        self.fragments = fragments
        self.word_order = word_order

# Maybe better to just make this into an entire object
# have one method at the end that runs all of the functions in one swoop
# Maybe split up long function        
class SentenceExtractor():
    """
    
    """
    def __init__(self, paragraph, extraction_string):
        self.one_char_check = extraction_string
        self.paragraph = paragraph
        self.extracted_sentences = {}
        self.count = 1

    def extract_sentences(self):
        # overall, this returns a dictionary where each entry represents a sentence.  Each sentence contains a list of NavStrings and Tags
        # loops through the children of the para element
        for input_content in self.paragraph.contents:
            # if the child is a string and it contails punctuation 
            if isinstance(input_content, NavigableString):
                # Reset for each new NavigableString
                previous_index = 0  
                # within the navegable string find the punctuation matches
                matches = re.finditer(self.one_char_check, str(input_content))
                found_punctuation = False

                # iterate through the punctuation matches
                for match in matches:
                    # found_punctuation is set to true if a punctuation mark is found
                    found_punctuation = True
                    # if the sentence count is not already a key in cleaned sentences, a new list is initialised 
                    if self.count not in self.extracted_sentences:
                        self.extracted_sentences[self.count] = []

                    # get the string pertaining to the current match
                    individual_sentence = input_content[previous_index:match.start() + 1]
                    # add this to the dictionary
                    self.extracted_sentences[self.count].append(individual_sentence)
                    self.count += 1
                    previous_index = match.start() + 1

                # Handle the remaining part of the string
                # If there is no punctuation, the entire child is added
                if not found_punctuation:
                    if self.count not in self.extracted_sentences:
                        self.extracted_sentences[self.count] = []
                    self.extracted_sentences[self.count].append(input_content)
                # if there is still text left after removing all sentences...
                elif previous_index < len(input_content):
                    if self.count not in self.extracted_sentences:
                        self.extracted_sentences[self.count] = []
                    # ...add the remaining bit to the dictionary
                    self.extracted_sentences[self.count].append(input_content[previous_index:])

            elif isinstance(input_content, Tag):
                # Append tags to the current sentence
                if self.count not in self.extracted_sentences:
                    self.extracted_sentences[self.count] = []
                self.extracted_sentences[self.count].append(input_content)

    def get_extracted_sentences(self):
        return self.extracted_sentences
    

class RemoveEntry:
    def __init__(self, extracted_sentences, tag_name):
        self.extracted_sentences = extracted_sentences
        self.tagless_sentences = {}
        self.count = 0
        self.tag_name = tag_name

    def remove_entries(self):
        # This removes any entries from the dict if the sentences has the inputted tag
        for key in list(self.extracted_sentences.keys()):
            for element in self.extracted_sentences[key]:
                if isinstance(element, Tag) and (element.name == self.tag_name or element.find(self.tag_name) is None):
                    self.tagless_sentences[key] = self.extracted_sentences[key]
                    self.count += 1
                    break
                    
        logging.info(f'sentences removed: {self.count}')
    
    def get_tagless_sentences(self):
        return self.tagless_sentences
        

class MarkupToText:
    def __init__(self, tag_removed_sentences):
        self.tag_removed_sentences = tag_removed_sentences
        self.text_sentences = {}
        
    def to_text(self):
        # this goes through all of the elements in each of the "sentences" and if it is a Tag extracts the text and if not (i.e. it is a NavString), it extracts the string directly
        # In other words, it transforms lists of markup and navstrings representing sentences, into strings.
        for key in self.tag_removed_sentences:
            self.text_sentences[key] = ''.join(element.get_text() if isinstance(element, Tag) else str(element) for element in self.tag_removed_sentences[key])

    def get_stringified_sentences(self):
        return self.text_sentences
    

class CleanedSentences:
    def __init__(self, text_sentences):
        self.text_sentences = text_sentences

    def clean_sentences(self):
        cleaned_sentences = self.text_sentences
        for key in list(self.text_sentences.keys()):
            if len(self.text_sentences[key]) < 5:
                del self.text_sentences[key]

        for key in list(self.text_sentences.keys()):
            self.text_sentences[key] = self.text_sentences[key].strip()

        for key in list(self.text_sentences.keys()):
            if self.text_sentences[key][-1:] not in ['.', '!', '?']:
                del self.text_sentences[key]

        self.cleaned_sentences = cleaned_sentences

    def get_cleaned_sentences(self):
        return self.cleaned_sentences


import re

class SentenceSplitterBase:
    def __init__(self, text):
        self.text = text
        self.fragments = []
        self.word_order = []
        self.tuple_order = []
        self.pattern = None

    def split_sentence(self):
        split_text = self.text
        while re.search(self.pattern, split_text):
            match = re.search(self.pattern, split_text)
            new_fragment = split_text[:match.start()]
            next_fragment = split_text[match.end():]
            self.fragments.append(new_fragment)
            self.process_match(match)
            split_text = next_fragment
        self.fragments.append(split_text)
        self.split_text = split_text

    def process_match(self, match):
        # This method will be overridden in derived classes
        pass

    def get_sentence_representation(self):
        pass


class SentenceSplitterString(SentenceSplitterBase):
    def __init__(self, text, words):
        super().__init__(text)
        escaped_words = [re.escape(word) for word in words]
        self.pattern = r'\b(?:' + '|'.join(escaped_words) + r')\b'

    def process_match(self, match):
        self.word_order.append(match.group().strip())

    def get_sentence_representation(self):
        return self.split_text, self.fragments, self.word_order


# infintives_and_conjugations are the infinitives used to get the conjugation objects from the library
# ...as well as the objects that contain all the verb forms.    
class SentenceSplitterTuple(SentenceSplitterBase):
    def __init__(self, text, infinitives_and_conjugation_objects):
        super().__init__(text)
        self.found_conjugations = []
        all_escaped_words = []
        for infinitive_and_conjugation_object in infinitives_and_conjugation_objects:
            escaped_words = [re.escape(infinitive) for infinitive in infinitive_and_conjugation_object[0]]
            all_escaped_words += escaped_words
            self.conjugations = [{"infinitive": infinitive_and_conjugation_object[0], "tense": toople[1], "form": toople[3]} for toople in infinitive_and_conjugation_object[1].iterate()]
        self.pattern = r'\b(?:' + '|'.join(all_escaped_words) + r')\b'

    def process_match(self, match):
        matched_word = match.group().strip()
        for conjugation_dict in self.conjugations:
            if conjugation_dict["form"] == matched_word:
                self.found_conjugations.append(conjugation_dict)

    def get_sentence_representation(self):
        return self.split_text, self.fragments, self.found_conjugations


class SentenceConstructor:
    def __init__(self, text, fragments, word_order):
        self.text = text
        self.fragments = fragments
        self.word_order = word_order 
        self.sentence = Sentence(self.text, self.fragments, self.word_order)


class FormatConjugations:
    def __init__(self, data, past_participle_name, expected_length):
        self.data = data
        self.past_participle_name = past_participle_name
        self.expected_length = expected_length

    # TUPLE X WILL EITHER BE ONE TUPLE OR AN ARRAY OF TUPLES!!!!

    # Check if there are tuples with 'past_participle_name' as index [1], if so create a list
    def check_tuple_x(self):
        participle_tuples = []
        self.participle_tuples = [participle_tuples.append(x) for x in self.data if x[1] == self.past_participle_name]
        if self.participle_tuples is None:
            raise ValueError(f"No tuple with {self.past_participle_name} found")

    def get_past_participles(self):
        self.past_participles = [x[-1] for x in self.participle_tuples]

    # Remove all tuples whose final index matches with tuple X's final index (but do not remove tuple X)
    def remove_matches(self):
        self.data = [x for x in self.data if x[-1] not in  self.past_participles or x in self.participle_tuples]

    def check_length(self):
        # Check that all tuples have given length and raise an error if not (unless it is tuple X)
        for x in self.data:
            if len(x) != self.expected_length and x != self.participle_tuples:
                raise ValueError(f"Tuple {x} has length {len(x)} != {self.expected_length}")

# Remove the class from inside of the Factory
# The factory should be a function rather than class
class FormatConjugationsFactory:
    
    @staticmethod
    def get_formatter(data, language_code):
        if language_code == "es":
            
            class SpanishConjugationFormatter(FormatConjugations):
                # If the only tuple with a length of less than given length is tuple X, remove it and create a new tuple with an empty string inserted at index [2]
                def create_new_tuple(self):
                    if len(self.participle_tuples) < self.expected_length:
                        self.data.remove(self.participle_tuples)
                        new_tuple = self.participle_tuples[:2] + ('',) + self.participle_tuples[2:]
                        print(f'new_tuple: {new_tuple}')
                        self.data.append(new_tuple)
            
            spanish_conjugation_formatter = SpanishConjugationFormatter(data, 'Participo Participo', 4)
            return spanish_conjugation_formatter
        
        if language_code == "pt":
            portuguese_conjugation_formatter = FormatConjugations(data, 'Particípio Particípio', 4)
            return portuguese_conjugation_formatter
        
        if language_code == "it":
            italian_conjugation_formatter = FormatConjugations(data, 'Participio Participio', 4)
            return italian_conjugation_formatter
        
        if language_code == "fr":
            french_conjugation_formatter = FormatConjugations(data, 'Participe Passé', 4)
            return french_conjugation_formatter


    
# think best idea here is maybe to add 