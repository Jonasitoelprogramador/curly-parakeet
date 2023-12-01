from django.urls import path
from . import views

urlpatterns = [
    path("", views.number_one, name="number_one")
]