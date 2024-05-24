from django.http import JsonResponse
from .services.get_and_convert_objects import get_objects, SentenceObjectToDict
from .services.languages_and_grammar import languages_list_content, find_language_and_point, get_language_code
# Create your views here.
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse

import json

from functools import lru_cache

from django.http import JsonResponse, StreamingHttpResponse
import json

'''@csrf_exempt
def get_sentences(request):
    try:
        id = json.loads(request.body)
        language, grammar_point, verb = find_language_and_point(id)
        language_code = get_language_code(language)
        difficult_words = grammar_point.split(' VS ')
        all_sentence_objects = get_objects(f"https://{language_code}.wikipedia.org/api/rest_v1/page/random/html", difficult_words, 5, verb, language_code)
        sentence_dicts = SentenceObjectToDict(all_sentence_objects).process()

        if not sentence_dicts:
            raise ValueError("No sentences found")

        # final sentences here is a list of tuples where 0 is fragments and 1 is word_order
        json_data = json.dumps(sentence_dicts)
        return JsonResponse(json_data, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)'''
    
@csrf_exempt
def get_sentences(request):
    def data_stream():
        try:
            # Send initial trivial data
            yield JsonResponse({"status":"processing"})

            id = json.loads(request.body)
            language, grammar_point, verb = find_language_and_point(id)
            language_code = get_language_code(language)
            difficult_words = grammar_point.split(' VS ')
            all_sentence_objects = get_objects(f"https://{language_code}.wikipedia.org/api/rest_v1/page/random/html", difficult_words, 5, verb, language_code)
            sentence_dicts = SentenceObjectToDict(all_sentence_objects).process()

            if not sentence_dicts:
                raise ValueError("No sentences found")

            # Send the actual data
            json_data = json.dumps(sentence_dicts)
            yield JsonResponse(json_data, safe=False)

        except Exception as e:
            # Send error message
            yield JsonResponse({"error": str(e)}, status=400)

    # Return a streaming response
    response = StreamingHttpResponse(data_stream(), content_type="text/event-stream")
    return response



@ensure_csrf_cookie
def get_csrf_token(request):
    # Your view logic here
    return JsonResponse({'message': 'CSRF protection is disabled for this view.'})


@ensure_csrf_cookie
def get_languages_content(request):
    # Your view logic here
    return JsonResponse({1: languages_list_content})
    
from django.http import HttpResponse

def hello(request):
    return HttpResponse("hello")


