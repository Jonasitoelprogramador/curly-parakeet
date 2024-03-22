from django.http import JsonResponse
from .services.wiki_api import format_api_response as api_response
from .services.caramelo_wiki_api import format_api_response as caramelo_api_response
from .services.languages_and_grammar import languages_list_content, find_language_and_point, get_language_code
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse

import json

from functools import lru_cache

from django.http import JsonResponse
import json

@csrf_exempt
def get_sentences(request):
    try:
        id = json.loads(request.body)
        language, grammar_point = find_language_and_point(id)
        language_code = get_language_code(language)
        difficult_words = grammar_point.split(' VS ')
        final_sentences = api_response(f"https://{language_code}.wikipedia.org/api/rest_v1/page/random/html", difficult_words, 5)
        
        if not final_sentences:
            raise ValueError("No sentences found")

        security_dict = {1: final_sentences, 2: difficult_words}
        return JsonResponse(security_dict)

    except Exception as e:
        # Return an error response with a custom message and a 400 status code
        # The Exception in this case refers to the ValuError above
        # The dictionary below basically puts the message from the ValueError as a string
        # This is the accesible in error.response.data.error
        return JsonResponse({"error": str(e)}, status=400)



@ensure_csrf_cookie
def get_csrf_token(request):
    # Your view logic here
    return JsonResponse({'message': 'CSRF protection is disabled for this view.'})


@ensure_csrf_cookie
def get_languages_content(request):
    # Your view logic here
    return JsonResponse({1: languages_list_content})
    




