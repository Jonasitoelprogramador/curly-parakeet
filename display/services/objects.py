import re
from functools import partial
from bs4 import NavigableString, Tag

'''class ApiInput:
    def __init__(self, cleaned_sentences, difficult_words):
        self.sentences = cleaned_sentences
        for w in difficult_words:
            setattr(self, f'{w}_sentences', {})
            method = self.create_dynamic_method(w)
            bound_method = partial(method, self)
            setattr(self, f'{w}_search', bound_method)  
    
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
        return total_characters'''

class ApiInput:
    def __init__(self, cleaned_sentences, difficult_words):
        self.sentences = cleaned_sentences
        self.final_structure = {}

        for key, text in self.sentences.items():
            # Dictionary to hold the word occurrences
            occurrences = {}
            for word in difficult_words:
                pattern = r'\b' + re.escape(word) + r'\b'
                # Find all occurrences of the word
                indices = [m.span() for m in re.finditer(pattern, text)]
                if indices:
                    occurrences[word] = indices
            
            # Add to final structure only if there are occurrences
            if occurrences:
                self.final_structure[key] = [{word: indices} for word, indices in occurrences.items()], text
            
    def calculate_characters(self):
        total_characters = sum(len(value) for value in self.sentences.values())
        return total_characters

class Paragraph:
    def __init__(self, paragraph):
        # Define the URL for the Wikimedia REST API for the 'Caramel' page
        self.request_count = 0
        self.one_char_check = r"(?<!\b[a-z]{1})[!?.]"
        self.paragraph = paragraph
        self.cleaned_sentences = {}
        self.count = 1

    def separate_to_sentences(self):
        # overall, this returns a dictionary where each entry represents a sentence.  Each sentence contains both NavStrings and Tags
        # loops through the children of the para element
        for input_content in self.paragraph.contents:
            # if the child is a string and it contails punctuation 
            if isinstance(input_content, NavigableString):
                previous_index = 0  # Reset for each new NavigableString
                matches = re.finditer(self.one_char_check, str(input_content))
                found_punctuation = False

                # iterate through the punctuation matches
                for match in matches:
                    found_punctuation = True
                    # start a new sentence for each new match
                    if self.count not in self.cleaned_sentences:
                        self.cleaned_sentences[self.count] = []

                    # get the string pertaining to the current match
                    individual_sentence = input_content[previous_index:match.start() + 1]
                    # add this to the dictionary
                    self.cleaned_sentences[self.count].append(individual_sentence)
                    self.count += 1
                    previous_index = match.start() + 1

                # Handle the remaining part of the string
                # If there is no punctuation, the entire child is added
                if not found_punctuation:
                    if self.count not in self.cleaned_sentences:
                        self.cleaned_sentences[self.count] = []
                    self.cleaned_sentences[self.count].append(input_content)
                # if there is still text left after removing all sentences...
                elif previous_index < len(input_content):
                    if self.count not in self.cleaned_sentences:
                        self.cleaned_sentences[self.count] = []
                    # ...add the remaining bit to the dictionary
                    self.cleaned_sentences[self.count].append(input_content[previous_index:])

            elif isinstance(input_content, Tag):
                # Append tags to the current sentence
                if self.count not in self.cleaned_sentences:
                    self.cleaned_sentences[self.count] = []
                self.cleaned_sentences[self.count].append(input_content)

    def remove_link_entries(self):
        # This removes any entries from the dict if the sentences has a <a></a> tag
        for key in list(self.cleaned_sentences.keys()):
            for element in self.cleaned_sentences[key]:
                if isinstance(element, Tag) and (element.name == 'a' or element.find('a') is not None):
                    del self.cleaned_sentences[key]
                    break

    # outside of class here you need to check if paragraph is none

    def extract_text(self):
        for key in self.cleaned_sentences:
            self.cleaned_sentences[key] = ''.join(element.get_text() if isinstance(element, Tag) else str(element) for element in self.cleaned_sentences[key])
    
    def remove_short_sentences(self):
        for key in list(self.cleaned_sentences.keys()):
            if len(self.cleaned_sentences[key]) < 5:
                del self.cleaned_sentences[key]
    
    def remove_whitespace(self):
        for key in list(self.cleaned_sentences.keys()):
            self.cleaned_sentences[key] = self.cleaned_sentences[key].strip()
    
    def remove_unwanted_characters(self):
        for key in list(self.cleaned_sentences.keys()):
            if self.cleaned_sentences[key][-1:] not in ['.', '!', '?']:
                del self.cleaned_sentences[key]
