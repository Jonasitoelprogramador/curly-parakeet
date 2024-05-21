import re

from bs4 import NavigableString, Tag

import logging

# Maybe better to just make this into an entire object
# have one method at the end that runs all of the functions
# Maybe split up long function        
class BeautifulSoupParagraphToSentenceStrings():
    """
    
    """
    def __init__(self, paragraph, extraction_string, tag_name):
        self.one_char_check = extraction_string
        self.paragraph = paragraph
        self.tagless_sentences = {}
        self.extracted_sentences = {}
        self.text_sentences = {}
        self.tag_name = tag_name

    def remove_sentences(self):
        # overall, this returns a dictionary where each entry represents a sentence.  Each sentence contains a list of NavStrings and Tags
        # loops through the children of the para element
        count = 1
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
                    if count not in self.extracted_sentences:
                        self.extracted_sentences[count] = []

                    # get the string pertaining to the current match
                    individual_sentence = input_content[previous_index:match.start() + 1]
                    # add this to the dictionary
                    self.extracted_sentences[count].append(individual_sentence)
                    count += 1
                    previous_index = match.start() + 1

                # Handle the remaining part of the string
                # If there is no punctuation, the entire child is added
                if not found_punctuation:
                    if count not in self.extracted_sentences:
                        self.extracted_sentences[count] = []
                    self.extracted_sentences[count].append(input_content)
                # if there is still text left after removing all sentences...
                elif previous_index < len(input_content):
                    if count not in self.extracted_sentences:
                        self.extracted_sentences[count] = []
                    # ...add the remaining bit to the dictionary
                    self.extracted_sentences[count].append(input_content[previous_index:])

            elif isinstance(input_content, Tag):
                # Append tags to the current sentence
                if count not in self.extracted_sentences:
                    self.extracted_sentences[count] = []
                self.extracted_sentences[count].append(input_content)

    def remove_entries(self, tag_name):
        # This removes any entries from the dict if the sentences has the inputted tag
        count = 0
        for key in list(self.extracted_sentences.keys()):
            for element in self.extracted_sentences[key]:
                if isinstance(element, Tag) and (element.name == tag_name or element.find(tag_name) is None):
                    self.tagless_sentences[key] = self.extracted_sentences[key]
                    count += 1
                    break
                    
        logging.info(f'sentences removed: {count}')

    def markup_to_text(self):
        # this goes through all of the elements in each of the "sentences" and if it is a Tag extracts the text and if not (i.e. it is a NavString), it extracts the string directly
        # In other words, it transforms lists of markup and navstrings representing sentences, into strings.
        for key in self.tagless_sentences:
            self.text_sentences[key] = ''.join(element.get_text() if isinstance(element, Tag) else str(element) for element in self.tagless_sentences[key])
    
    def clean_sentences(self):
        for key in list(self.text_sentences.keys()):
            if len(self.text_sentences[key]) < 5:
                del self.text_sentences[key]

        for key in list(self.text_sentences.keys()):
            self.text_sentences[key] = self.text_sentences[key].strip()

        for key in list(self.text_sentences.keys()):
            if self.text_sentences[key][-1:] not in ['.', '!', '?']:
                del self.text_sentences[key]

        self.cleaned_sentences = self.text_sentences

    def extract_and_format(self):
        self.remove_sentences()
        self.remove_entries(self.tag_name)
        self.markup_to_text()
        self.clean_sentences()
        return self.cleaned_sentences






    
