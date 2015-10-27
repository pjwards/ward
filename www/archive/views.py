from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Count

import logging
import datetime

from . import tasks
from .fb_query import get_feed_query
from .models import Group, Post
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

        _group = Group()
        _group.id = group_data.get('id')
        _group.name = group_data.get('name')
        _group.description = group_data.get('description')
        _group.updated_time = group_data.get('updated_time')
        _group.privacy = group_data.get('privacy')

        _group.save()
        logger.info('Saved group: %s', _group)

        store_group_feed(_group.id)

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
    _group = Group.objects.filter(id=group_id)[0]
    store_group_feed(_group.id)
    return HttpResponse("Send")


def group_update(request, group_id):
    updated_time = fb_request.group(group_id).get('updated_time')
    _group = Group.objects.filter(id=group_id)[0]

    if _group.is_updated(updated_time):
        _group.updated_time = updated_time
        _group.save()
        logger.info('Update group updated_time: %s', _group.id)

        update_group_feed(_group.id)
        return HttpResponseRedirect(reverse('archive:groups'))
    else:
        return redirect(reverse('archive:groups') + '?error=error3')


def group(request, group_id):
    if request.method == "GET":
        _group = Group.objects.filter(id=group_id)

        from_date = datetime.datetime.now() - datetime.timedelta(days=1)
        posts = Post.objects.filter(group=_group, created_time__range=[from_date, datetime.datetime.now()])\
            .extra(
            select={'field_sum': 'like_count + comment_count'},
            order_by=('-field_sum', )
        )

        print(_group)

        for post in posts:
            print(post.like_count + post.comment_count)
    elif request.method == "POST":
        pass

    return render(
        request,
        'archive/group/analysis.html',
        {
            'group': _group,
            'posts': posts,
        }
    )
