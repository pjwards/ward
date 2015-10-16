from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import logging

from urllib.request import urlopen
import lxml.html

from . import tasks
from .local_settings import get_feed_query
from .models import Group
from .fb_request import FBRequest

logger = logging.getLogger(__name__)


def store(request, group_id):
    tasks.store_group_feed.delay(group_id, get_feed_query(10, 100))
    return HttpResponse("Send")


def groups(request):
    if request.method == "GET":
        latest_group_list = Group.objects.order_by('name')
        error = None
        if 'error' in request.GET:
            error = 'error'
    elif request.method == "POST":
        fb_request = FBRequest()

        group_data = fb_request.group(request.POST['id'])

        if group_data is None:
            return redirect(reverse('archive:groups') + '?error=error1')

        if Group.objects.filter(id=group_data.get('id')).exists():
            return redirect(reverse('archive:groups') + '?error=error2')

        group = Group()
        group.id = group_data.get('id')
        group.name = group_data.get('name')
        group.description = group_data.get('description')
        group.updated_time = group_data.get('updated_time')
        group.privacy = group_data.get('privacy')

        group.save()
        logger.info('Saved group: %s', group.id)

        return HttpResponseRedirect(reverse('archive:groups'))

    return render(
        request,
        'archive/group/list.html',
        {
            'latest_group_list': latest_group_list,
            'error': error,
        }
    )
