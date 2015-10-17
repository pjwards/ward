from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

import logging

from . import tasks
from .local_settings import get_feed_query
from .models import Group
from .fb_request import FBRequest

logger = logging.getLogger(__name__)
fb_request = FBRequest()

store_group_feed = lambda group_id: tasks.store_group_feed.delay(group_id, get_feed_query(10, 100))
update_group_feed = lambda group_id: tasks.update_group_feed.delay(group_id, get_feed_query(10, 100))


def groups(request):
    if request.method == "GET":
        latest_group_list = Group.objects.order_by('name')
        error = None
        if 'error' in request.GET:
            error = 'error'
    elif request.method == "POST":
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

        store_group_feed(group.id)

        return HttpResponseRedirect(reverse('archive:groups'))

    return render(
        request,
        'archive/group/list.html',
        {
            'latest_group_list': latest_group_list,
            'error': error,
        }
    )


def group_store(request, group_id):
    store_group_feed(group_id)
    return HttpResponse("Send")


def group_update(request, group_id):
    updated_time = fb_request.group(group_id).get('updated_time')
    group = Group.objects.filter(id=group_id)[0]

    if group.is_updated(updated_time):
        group.updated_time = updated_time
        group.save()
        logger.info('Update group updated_time: %s', group.id)

        update_group_feed(group_id)
        return HttpResponseRedirect(reverse('archive:groups'))
    else:
        return redirect(reverse('archive:groups') + '?error=error3')

