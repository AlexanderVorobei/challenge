from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Schema


@login_required()
def schemas(request):
    schemas = Schema.objects.filter(user=request.user)
    context = {"schemas": schemas}
    return render(request, "fake_data/schemas.html", context)
