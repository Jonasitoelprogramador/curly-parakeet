import requests
from bs4 import BeautifulSoup

from beautiful_soup_paras_to_sentence_strings import BeautifulSoupParagraphToSentenceStrings
from sentences import sentence_constructor
from sentence_strings_to_fragments import GetMatches
from conjugations import get_formatter, get_conjugations, format_conjugations
from keywords import CreateKeywordObjects, AddContrastiveForms


import time


def get_objects(api_url, key_words, number, verb, language_code):
    # Initialize variables
    all_sentence_objects = []

    start_time = time.time()
    max_duration = 60

    # formatted_conjugations is a list where each element is a list of all of the conjugations with metadata
    # conjugations for matching is now a list of Conjugation objects
    keyword_objects = CreateKeywordObjects(key_words, language_code, verb, get_formatter, get_conjugations, format_conjugations).process()

    while len(all_sentence_objects) < number:
        if time.time() - start_time > max_duration:
            raise ValueError("Getting sentences took too long")

        # Send a GET request to the API
        response = requests.get(api_url)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            paragraphs = soup.find_all('p')

            for p in paragraphs:
                cleaned_sentences = BeautifulSoupParagraphToSentenceStrings(p, "(?<!\b[a-z]{1})[!?.]", 'a').extract_and_format()

                for s in cleaned_sentences.values():
                    fragments, matching_objects = GetMatches(s, keyword_objects).process()
                    if len(matching_objects) >= 1:
                        print(f"matching_objects: {matching_objects[0].form}")
                    if matching_objects:
                        matching_objects_with_contrastive_forms = AddContrastiveForms(matching_objects, key_words, language_code, get_conjugations, format_conjugations, get_formatter).get_contrastive_forms()
                        sentence_object = sentence_constructor(s, fragments, matching_objects_with_contrastive_forms)     
                        all_sentence_objects.append(sentence_object)
    print(f"all_sentence_objects: {all_sentence_objects}")
    return all_sentence_objects
    

class SentenceObjectToDict():
    def __init__(self, sentence_objects):
        self.sentence_objects = sentence_objects
    
    def object_to_dict(self, obj):
        """ Helper function to convert an object to a dictionary, including its inherited attributes. """
        '''if isinstance(obj, ConjugationKeyword):
            # Include attributes specific to ConjugationKeyword
            return {
                'form': obj.form,
                'verb': obj.verb,
                'infinitive': obj.infinitive,
                'mood': obj.mood,
                'tense': obj.tense,
                'person': obj.person,
                'contrastive_forms': obj.contrastive_forms
            }
        elif isinstance(obj, Keyword):
            # Include attributes specific to Keyword
            return {
                'form': obj.form,
                'verb': obj.verb,
                'contrastive_forms': obj.contrastive_forms
            }'''
        return {
                'form': obj.form,
                'verb': obj.verb,
                'contrastives': obj.contrastive_forms
            }


    def sentence_to_dict(self, sentence):
        """ Convert a Sentence object into a dictionary. """
        return {
            'text': sentence.text,
            'fragments': sentence.fragments,
            'keywords': [self.object_to_dict(kw) for kw in sentence.keyword_objects]
        }

    def process(self):
        sentence_dicts = [self.sentence_to_dict(sentence) for sentence in self.sentence_objects]
        return sentence_dicts


if __name__ == "__main__":
    all_sentence_objects = get_objects("https://it.wikipedia.org/api/rest_v1/page/random/html", ['sapere', 'conoscere'], 2, True, 'it')
    print(all_sentence_objects)

