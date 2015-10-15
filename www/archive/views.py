from django.shortcuts import render
from django.http import  HttpResponse

from . import tasks


def store(request, group_id):
    tasks.store.delay(group_id)
    return HttpResponse("Send")
