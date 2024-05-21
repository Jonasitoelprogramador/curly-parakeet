import re

class GetMatches():
    def __init__(self, sentence, keyword_objects):
        self.sentence = sentence
        self.fragments = []
        self.keyword_objects = keyword_objects
        escaped_words = [re.escape(word.form) for word in keyword_objects]
        self.pattern = r'\b(?:' + '|'.join(escaped_words) + r')\b'
        self.matched_words = []

    def split_sentence(self):
        split_sentence = self.sentence
        while re.search(self.pattern, split_sentence):
            match = re.search(self.pattern, split_sentence)
            new_fragment = split_sentence[:match.start()]
            next_fragment = split_sentence[match.end():]
            self.fragments.append(new_fragment)
            self.add_matches(match)
            split_sentence = next_fragment
        self.fragments.append(split_sentence)
        self.split_sentence = split_sentence

    def add_matches(self, match):
        self.matched_words.append(match.group().strip())
    
    def get_matching_objects(self):
        self.matching_objects = []
        for word in self.matched_words:
            current_matching_objects = [obj for obj in self.keyword_objects if obj.form == word]
            try:
               current_matching_object = current_matching_objects[0] 
            except ValueError:
                pass
            self.matching_objects.append(current_matching_object)

    def process(self):
        self.split_sentence()
        self.get_matching_objects()
        return self.fragments, self.matching_objects


'''class SentenceStringToFragments(SentenceStringToFragmentsBase):
    def __init__(self, sentence, words_for_matching):
        super().__init__(sentence)
        escaped_words = [re.escape(word) for word in words_for_matching]
        self.pattern = r'\b(?:' + '|'.join(escaped_words) + r')\b'
        self.matching_words = []

    def process_match(self, match):
        self.matching_words.append(match.group().strip())

    def get_sentence_representation(self):
        return self.fragments, self.matching_words
'''

'''# infintives_and_conjugations are the infinitives used to get the conjugation objects from the library
# ...as well as the objects that contain all the verb forms.    
class SentenceStringToFragmentsConjugations(SentenceStringToFragmentsBase):
    def __init__(self, sentence, infinitives_and_keyword_objects):
        super().__init__(sentence)
        self.found_conjugations = []
        all_escaped_words = []
        for infinitive_and_conjugation_object in infinitives_and_keyword_objects:
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
        return self.split_sentence, self.fragments, self.found_conjugations
'''