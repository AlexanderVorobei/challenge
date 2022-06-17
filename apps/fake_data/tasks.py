import os
from celery import shared_task

from .models import DataSet


@shared_task
def update_dataset(data_set_id: int):
    data_set = DataSet.objects.get(id=data_set_id)
    data_set.update_dataset()
    data_set.save()
    if data_set.file:
        data_set.status = DataSet.Status.READY
        data_set.save()
