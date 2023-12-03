from django.shortcuts import render, JsonResponse
from services.wiki_api import call_api
# Create your views here.

def number_one(request):
    # note the por para list will come in as part of the request when it is properly set up
    difficult_words = ['por', 'para']
    para_objects = call_api("https://es.wikipedia.org/api/rest_v1/page/html/caramelo", difficult_words)
    for o in para_objects:
        o.por_search()
        o.para_search()
        if o.por_sentences:
            print(o.por_sentences)
        if o.para_sentences:
            print(o.para_sentences)
    return JsonResponse(data)







for o in para_objects:
    o.por_search()
    o.para_search()
    if o.por_sentences:
        print(o.por_sentences)
    if o.para_sentences:
        print(o.para_sentences)