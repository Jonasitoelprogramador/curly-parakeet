import requests
from bs4 import BeautifulSoup

from .objects import Paragraph

def format_api_response(api_url, words):
    # Initialize variables
    all_sentence_objs = []
    final_sentences = []

    #while total_characters < 50000:
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

    [print(final_sentences)]
    return final_sentences

if __name__ == "__main__":
    final_sentences = format_api_response("https://es.wikipedia.org/api/rest_v1/page/html/caramelo", ['por', 'para'])

