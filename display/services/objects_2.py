import re

from bs4 import NavigableString, Tag

import logging



class Sentence:
    def __init__(self, text, fragments, key_words):
        # Define the URL for the Wikimedia REST API for the 'Caramel' page
        self.text = text
        self.fragments = fragments
        self.key_words = key_words


class SentenceExtractor():
    def __init__(self, paragraph, extraction_string):
        self.one_char_check = extraction_string
        self.paragraph = paragraph
        self.extracted_sentences = {}
        self.count = 1

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

        return self.extracted_sentences
    

class RemoveEntry:
    def __init__(self, extracted_sentences, tag_name):
        self.extracted_sentences = extracted_sentences
        self.tag_removed_sentences = {}
        self.count = 0

        # This removes any entries from the dict if the sentences has the inputted tag
        for key in list(self.extracted_sentences.keys()):
            for element in self.extracted_sentences[key]:
                if isinstance(element, Tag) and (element.name == tag_name or element.find(tag_name) is None):
                    self.tag_removed_sentences[key] = self.extracted_sentences[key]
                    self.count += 1
                    break
                    
        logging.info(f'sentences removed: {self.count}')
        return self.tag_removed_sentences
        

class MarkupToText:
    def __init__(self, tag_removed_sentences):
        self.tag_removed_sentences = tag_removed_sentences
        self.text_sentences = {}
        # this goes through all of the elements in each of the "sentences" and if it is a Tag extracts the text and if not (i.e. it is a NavString), it extracts the string directly
        # In other words, it transforms lists of markup and navstrings representing sentences, into strings.
        for key in self.tag_removed_sentences:
            self.text_sentences[key] = ''.join(element.get_text() if isinstance(element, Tag) else str(element) for element in self.tag_removed_sentences[key])
    
        return self.text_sentences
    

class CleanedSentences:
    def __init__(self, text_sentences):
        self.text_sentences = text_sentences

        for key in list(self.text_sentences.keys()):
            if len(self.text_sentences[key]) < 5:
                del self.text_sentences[key]

        for key in list(self.text_sentences.keys()):
            self.text_sentences[key] = self.text_sentences[key].strip()

        for key in list(self.text_sentences.keys()):
            if self.text_sentences[key][-1:] not in ['.', '!', '?']:
                del self.text_sentences[key]

        return self.cleaned_sentences


# this takes a single sentence and returns the text, fragments and identified words (in order)
class SentenceSplitter:
    def __init__(self, text, words):
        self.text = text
        self.fragments = []
        self.word_order = []
        escaped_words = [re.escape(word) for word in words]
        print(escaped_words)
        self.pattern = r'\b(?:' + '|'.join(escaped_words) + r')\b'

        while re.search(self.pattern, self.text):
            # match is the search object returned when word is found
            match = re.search(self.pattern, self.text)
            # new_fragment is all the chracaters from the beginning to the first position of the match (exclusive)
            new_fragment = self.text[:match.start()]
            # all the chaaracters from the end of the match to the end
            next_fragment = self.text[match.end():]
            # add the new fragment to the fragments list
            self.fragments.append(new_fragment)
            # add the matched characters 
            self.word_order.append((match.group()).strip())
            self.text = next_fragment
        self.fragments.append(self.text)


class SentenceConstructor:
    def __init__(self, text, fragments, word_order):
        self.text = text
        self.fragments = fragments
        self.word_order = word_order 
        self.sentence = Sentence(self.text, self.fragments, self.word_order)
        


# think this is gonna require having pattern just connected to the sentence splitter then have sentenceconstructor not worry about any of the splitting stuff
        
if __name__ == "__main__":
    extracted_sentences = SentenceExtractor()