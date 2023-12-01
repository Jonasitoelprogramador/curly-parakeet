import re
from functools import partial
from bs4 import NavigableString, Tag

class Paragraph:
    def __init__(self, paragraph, *args):
        self.sentences = paragraph
        for a in args:
            setattr(self, f'{a}_sentences', {})
            method = self.create_dynamic_method(a)
            bound_method = partial(method, self)
            setattr(self, f'{a}_search', bound_method)  
    
    def create_dynamic_method(self, search_term):  
        # Define the body of the new method
        def dynamic_method(self):
            sentences = {}
            for key, value in self.sentences.items():
                if re.search(rf'\b{search_term}\b', value, re.IGNORECASE):
                    sentences[key] = value
            setattr(self, f'{search_term}_sentences', sentences)
        return dynamic_method
    
    def calculate_characters(self):
        total_characters = sum(len(value) for value in self.sentences.values())
        return total_characters

class ApiResponsePara:
    def __init__(self, paragraph):
        # Define the URL for the Wikimedia REST API for the 'Caramel' page
        self.request_count = 0
        self.one_char_check = r"(?<!\b[a-z]{1})[!?.]"
        self.input_paragraph = paragraph
        self.output_paragraph = {}
        self.count = 1

    def separate_to_sentences(self):
        # overall, this returns a dictionary where each entry represents a sentence.  Each sentence contains both NavStrings and Tags
        # loops through the children of the para element
        for content in self.input_paragraph.contents:
            # if the child is a string and it contails punctuation 
            if isinstance(content, NavigableString):
                previous_index = 0  # Reset for each new NavigableString
                matches = re.finditer(self.one_char_check, str(content))
                found_punctuation = False

                # iterate through the punctuation matches
                for match in matches:
                    found_punctuation = True
                    # start a new sentence for each new match
                    if self.count not in self.output_paragraph:
                        self.output_paragraph[self.count] = []

                    # get the string pertaining to the current match
                    individual_sentence = content[previous_index:match.start() + 1]
                    # add this to the dictionary
                    self.output_paragraph[self.count].append(individual_sentence)
                    self.count += 1
                    previous_index = match.start() + 1

                # Handle the remaining part of the string
                # If there is no punctuation, the entire child is added
                if not found_punctuation:
                    if self.count not in self.output_paragraph:
                        self.output_paragraph[self.count] = []
                    self.output_paragraph[self.count].append(content)
                # if there is still text left after removing all sentences...
                elif previous_index < len(content):
                    if self.count not in self.output_paragraph:
                        self.output_paragraph[self.count] = []
                    # ...add the remaining bit to the dictionary
                    self.output_paragraph[self.count].append(content[previous_index:])

            elif isinstance(content, Tag):
                # Append tags to the current sentence
                if self.count not in self.output_paragraph:
                    self.output_paragraph[self.count] = []
                self.output_paragraph[self.count].append(content)

    def remove_link_entries(self):
        # This removes any entries from the dict if the sentences has a <a></a> tag
        for key in list(self.output_paragraph.keys()):
            for element in self.output_paragraph[key]:
                if isinstance(element, Tag) and (element.name == 'a' or element.find('a') is not None):
                    del self.output_paragraph[key]
                    break

    # outside of class here you need to check if paragraph is none

    def extract_text(self):
        for key in self.output_paragraph:
            self.output_paragraph[key] = ''.join(element.get_text() if isinstance(element, Tag) else str(element) for element in self.output_paragraph[key])
    
    def remove_short_sentences(self):
        for key in list(self.output_paragraph.keys()):
            if len(self.output_paragraph[key]) < 5:
                del self.output_paragraph[key]
    
    def remove_whitespace(self):
        for key in list(self.output_paragraph.keys()):
            self.output_paragraph[key] = self.output_paragraph[key].strip()
    
    def remove_unwanted_characters(self):
        for key in list(self.output_paragraph.keys()):
            if self.output_paragraph[key][-1:] not in ['.', '!', '?']:
                del self.output_paragraph[key]
