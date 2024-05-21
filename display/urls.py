from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_sentences, name="get-sentences"),
    path('get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    path('get-languages-content/', views.get_languages_content, name='get-languages-content'),
    path('hello/', views.hello, name='hello')
]

