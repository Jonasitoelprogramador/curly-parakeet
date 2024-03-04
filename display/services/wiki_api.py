import requests
from bs4 import BeautifulSoup

from .objects import Paragraph
import time

def format_api_response(api_url, words, number):
    # Initialize variables
    all_sentence_objs = []
    final_sentences = []

    start_time = time.time()
    max_duration = 10

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
                initial_para = Paragraph(p)
                if initial_para.cleaned_sentences:
                    initial_para.create_sentence_objs(words)
                    all_sentence_objs.extend(initial_para.sentence_objs)

            for ob in all_sentence_objs:
                if ob.key_words:
                    final_sentences.append((ob.fragments, ob.key_words))
            all_sentence_objs = []

    if len(final_sentences) > number:
        final_sentences = final_sentences[:5]

    if final_sentences:
        return final_sentences
    else:
        pass

if __name__ == "__main__":
    final_sentences = format_api_response("https://it.wikipedia.org/api/rest_v1/page/random/html", ['di', 'da'], 5)

