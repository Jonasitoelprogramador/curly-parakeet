import requests
from bs4 import BeautifulSoup

from objects import Paragraph, ApiInput

# Define the URL for the Wikimedia REST API for the 'Caramel' page

def call_api(api_url):
    # Initialize variables
    para_objects = []

    #while total_characters < 50000:
        # Send a GET request to the API
    response = requests.get(api_url)

    if response.status_code == 200:
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        paragraphs = soup.find_all('p')

        for p in paragraphs:
            initial_para = Paragraph(p)
            initial_para.separate_to_sentences()
            #print(f'this is the paragraph {initial_para.paragraph}')
            initial_para.remove_link_entries()
            if initial_para.cleaned_sentences:
                initial_para.extract_text()
                initial_para.remove_short_sentences()
                initial_para.remove_unwanted_characters()
                initial_para.remove_whitespace()
            else:
                continue
            if initial_para.cleaned_sentences:
                para_objects.append(initial_para)
    
    return para_objects

para_objects = call_api("https://es.wikipedia.org/api/rest_v1/page/html/caramelo")

def format_for_view(para_objects):
    for o in para_objects:
        p = ApiInput(o.cleaned_sentences, ['por','para'])
        if p.final_structure:
            print(p.final_structure)

format_for_view(para_objects)

'''for p in para_objects:
    print(p.cleaned_sentences)'''
