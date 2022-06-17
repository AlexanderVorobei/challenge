from django.urls import path, include

from .views import (
    schema_list,
    schema_create,
    schema_update,
    schema_delete,
    datasets_list,
    dataset_create,
)


app_name = "data"

urlpatterns = [
    path("list/", schema_list, name="list"),
    path("create/", schema_create, name="create"),
    path("<int:pk>/update/", schema_update, name="update"),
    path("<int:pk>/delete/", schema_delete, name="delete"),
    path("<int:schema_id>/datasets/", datasets_list, name="dataset_list"),
    path("<int:schema_id>/datasets/create/", dataset_create, name="dataset_create"),
]
