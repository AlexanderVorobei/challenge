from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied

from .models import Schema, ColumnGenerator, DataSet
from .tasks import update_dataset


@login_required
def schema_list(request):
    context = {"schemas": Schema.objects.filter(user=request.user).all()}
    return render(request, "fake_data/schema_list.html", context)


@require_http_methods(["GET", "POST"])
@login_required
def schema_create(request):
    if request.method == "GET":
        context = {
            "column_separator": Schema.Delimiter.choices,
            "string_characters": Schema.Quote.choices,
            "column_types": ColumnGenerator.choices(),
        }
        return render(request, "fake_data/schema_create.html", context)

    q = request.POST.dict()
    q.pop("csrfmiddlewaretoken")
    schema = Schema(
        user=request.user,
        name=q.pop("name"),
        column_separator=q.pop("column_separator"),
        string_character=q.pop("string_character"),
    )
    schema_json = {"schema": []}
    for i in range(len(q) // 3):
        column = int([k for k in q if q[k] == str(i)][0].removesuffix("__order"))
        name = q.get(f"{column}__name")
        data_type = q.get(f"{column}__type")
        schema_json["schema"].append({"name": name, "type": data_type})
    schema.columns = schema_json
    schema.save()
    return redirect(reverse("data:list"))


@require_http_methods(["GET", "POST"])
@login_required
def schema_update(request, pk: int):
    if request.method == "GET":
        context = {
            "schema": get_object_or_404(Schema, id=pk),
            "column_types": ColumnGenerator.choices(),
        }
        return render(request, "fake_data/schema_update.html", context)

    q = request.POST.dict()
    q.pop("csrfmiddlewaretoken")
    schema = get_object_or_404(Schema, id=pk)
    if schema.user != request.user:
        raise PermissionDenied
    schema.name = q.pop("name")
    schema.column_separator = q.pop("column_separator")
    schema.string_character = q.pop("string_character")
    schema_json = {"schema": []}
    for i in range(len(q) // 3):
        column = int([k for k in q if q[k] == str(i)][0].removesuffix("__order"))
        name = q.get(f"{column}__name")
        data_type = q.get(f"{column}__type")
        schema_json["schema"].append({"name": name, "type": data_type})
    schema.columns = schema_json
    schema.save()
    return redirect(reverse("data:list"))


@require_http_methods(["GET"])
@login_required
def schema_delete(request, pk: int):
    schema = get_object_or_404(Schema, id=pk)
    if schema.user != request.user:
        raise PermissionDenied
    schema.delete()
    return redirect(reverse("data:list"))


@require_http_methods(["GET"])
@login_required
def datasets_list(request, schema_id: int):
    schema = get_object_or_404(Schema, id=schema_id)
    context = {"datasets": schema.datasets_schema.all(), "schema": schema}
    if schema.user != request.user:
        raise PermissionDenied
    return render(request, "fake_data/dataset_list.html", context)


@require_http_methods(["POST"])
@login_required
def dataset_create(request, schema_id: int):
    schema = get_object_or_404(Schema, id=schema_id)
    if schema.user != request.user:
        raise PermissionDenied
    rows = int(request.POST.get("rows"))
    data_set = DataSet(schema=schema, rows=rows)
    data_set.save()
    update_dataset.delay(data_set.id)
    return redirect(reverse("data:dataset_list", args=[schema_id]))
