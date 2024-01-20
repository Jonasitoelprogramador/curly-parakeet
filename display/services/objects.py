import re

from bs4 import NavigableString, Tag


class Paragraph:
    def __init__(self, paragraph):
        # Define the URL for the Wikimedia REST API for the 'Caramel' page
        self.request_count = 0
        self.one_char_check = r"(?<!\b[a-z]{1})[!?.]"
        self.paragraph = paragraph
        self.cleaned_sentences = {}
        self.count = 1
        self.sentence_objs = []
        
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

        # This removes any entries from the dict if the sentences has a <a></a> tag
        for key in list(self.cleaned_sentences.keys()):
            for element in self.cleaned_sentences[key]:
                if isinstance(element, Tag) and (element.name == 'a' or element.find('a') is not None):
                    del self.cleaned_sentences[key]
                    break

        # outside of class here you need to check if paragraph is none
        for key in self.cleaned_sentences:
            self.cleaned_sentences[key] = ''.join(element.get_text() if isinstance(element, Tag) else str(element) for element in self.cleaned_sentences[key])

        for key in list(self.cleaned_sentences.keys()):
            if len(self.cleaned_sentences[key]) < 5:
                del self.cleaned_sentences[key]

        for key in list(self.cleaned_sentences.keys()):
            self.cleaned_sentences[key] = self.cleaned_sentences[key].strip()

        for key in list(self.cleaned_sentences.keys()):
            if self.cleaned_sentences[key][-1:] not in ['.', '!', '?']:
                del self.cleaned_sentences[key]

    def calculate_characters(self):
        total_characters = sum(len(value) for value in self.sentences.values())
        return total_characters
    
    def create_sentence_objs(self, words):
        if self.cleaned_sentences:   
            for text in self.cleaned_sentences.values():
                escaped_words = [re.escape(word) for word in words]
                pattern = r'\b(?:' + '|'.join(escaped_words) + r')\b'
                fragment = text
                next_fragment = ''
                fragments = []
                word_order = []
                while re.search(pattern, fragment):
                    match = re.search(pattern, fragment)
                    new_fragment = fragment[:match.start()]
                    next_fragment = fragment[match.end():]
                    fragments.append(new_fragment)
                    word_order.append((match.group()).strip())
                    fragment = next_fragment
                fragments.append(fragment)
                sentence = Sentence(text, fragments, word_order)
                self.sentence_objs.append(sentence)
        else:
            raise ValueError("Cleaned sentences cannot be null.")

class Sentence:
    def __init__(self, text, fragments, key_words):
        # Define the URL for the Wikimedia REST API for the 'Caramel' page
        self.text = text
        self.fragments = fragments
        self.key_words = key_words

  




