import requests
from bs4 import BeautifulSoup

from .objects_2 import SentenceExtractor, RemoveEntry, MarkupToText, CleanedSentences, SentenceSplitter, SentenceConstructor
import time

def format_api_response(api_url, words, number):
    # Initialize variables
    final_sentences = []

    start_time = time.time()
    max_duration = 20

    while len(final_sentences) < number:
        if time.time() - start_time > max_duration:
            raise ValueError("Getting sentences took too long")

        
        # Send a GET request to the API
        response = requests.get(api_url)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            paragraphs = soup.find_all('p')

            for p in paragraphs:
                all_paragraph_sentences = []
                extracted_sentences = SentenceExtractor(p, "(?<!\b[a-z]{1})[!?.]")
                tag_removed_sentences = RemoveEntry(extracted_sentences, 'a')
                text_sentences = MarkupToText(tag_removed_sentences)
                cleaned_sentences = CleanedSentences(text_sentences)
                
                for s in cleaned_sentences.values():
                    split_sentence = SentenceSplitter(s, words)
                    sentence_obj = SentenceConstructor(split_sentence.text, split_sentence.fragments, split_sentence.word_order).sentence
                    all_paragraph_sentences.append(sentence_obj)

                for ob in all_paragraph_sentences:
                    if ob.word_order:
                        final_sentences.append((ob.fragments, ob.key_words))
                

    if len(final_sentences) > number:
        final_sentences = final_sentences[:5]

    if final_sentences:
        return final_sentences
    else:
        pass

if __name__ == "__main__":
    final_sentences = format_api_response("https://it.wikipedia.org/api/rest_v1/page/random/html", ['di', 'da'], 5)


