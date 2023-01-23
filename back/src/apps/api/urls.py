from django.urls import path

from src.apps.api.v1 import GenerateWorldView

app_name = 'api'

urlpatterns = [
    path('next_generation/', GenerateWorldView.as_view(), name='next_generation'),
]
