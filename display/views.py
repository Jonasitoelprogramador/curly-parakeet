from django.shortcuts import JsonResponse
from services.wiki_api import format_api_response
# Create your views here.

def number_one(request):
    # note the por para list will come in as part of the request when it is properly set up
    difficult_words = ['por', 'para']
    final_sentences = format_api_response("https://es.wikipedia.org/api/rest_v1/page/html/caramelo", difficult_words)
    return JsonResponse(final_sentences)







