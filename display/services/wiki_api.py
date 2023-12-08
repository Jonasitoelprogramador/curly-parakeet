import requests
from bs4 import BeautifulSoup

from objects import Paragraph

# Define the URL for the Wikimedia REST API for the 'Caramel' page

def format_api_response(api_url, words):
    # Initialize variables
    para_dicts = []
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
                initial_para.format_final_structure(words)
                if initial_para.final_structure:
                    para_dicts.append(initial_para.final_structure)

        for dicto in para_dicts:
            for value in dicto.values():
                final_sentences.append(value)

    return final_sentences

if __name__ == "__main__":
    final_sentences = format_api_response("https://es.wikipedia.org/api/rest_v1/page/html/caramelo", ['por', 'para'])
    print(final_sentences)
