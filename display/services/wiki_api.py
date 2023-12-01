import requests
from bs4 import BeautifulSoup

from objects import Paragraph, ApiResponsePara

# Define the URL for the Wikimedia REST API for the 'Caramel' page

api_url = "https://es.wikipedia.org/api/rest_v1/page/html/caramelo"

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
        initial_para = ApiResponsePara(p)
        initial_para.separate_to_sentences()
        #print(f'this is the paragraph {initial_para.paragraph}')
        initial_para.remove_link_entries()
        if initial_para.output_paragraph:
            initial_para.extract_text()
            initial_para.remove_short_sentences()
            initial_para.remove_unwanted_characters()
            initial_para.remove_whitespace()
        else:
            continue
        if initial_para.output_paragraph:
            para_object = Paragraph(initial_para.output_paragraph, 'por', 'para')
            para_objects.append(para_object)
                

for o in para_objects:
    o.por_search()
    o.para_search()
    if o.por_sentences:
        print(o.por_sentences)
    if o.para_sentences:
        print(o.para_sentences)