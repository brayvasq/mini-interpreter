from django.urls import path
from . import views

urlpatterns = [
    path('api/sentence',views.SentenceListCreate.as_view()),
]