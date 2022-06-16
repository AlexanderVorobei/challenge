from django.urls import path, include

from .views import schemas


app_name = "data"

urlpatterns = [
    path("schemas/", schemas, name="schemas"),
]
