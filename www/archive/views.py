from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connections
from django.db.models import Count, Sum

import logging
import datetime

from . import tasks
from .fb_query import get_feed_query
from .models import Group, Post, Comment
from .fb_request import FBRequest

logger = logging.getLogger(__name__)
fb_request = FBRequest()


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

        tasks.store_group_feed.delay(_group.id, get_feed_query(10, 100))

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
    if not Group.objects.filter(id=group_id).exists():
        return redirect(reverse('archive:groups') + '?error=error2')

    tasks.store_group_feed.delay(group_id, get_feed_query(10, 100))
    return HttpResponse("Send")


def group_update(request, group_id):
    if not Group.objects.filter(id=group_id).exists():
        return redirect(reverse('archive:groups') + '?error=error2')

    if tasks.update_group_feed.delay(group_id, get_feed_query(10, 100)):
        return HttpResponseRedirect(reverse('archive:groups'))


def group(request, group_id):
    if request.method == "GET":
        _groups = Group.objects.all()
        _group = Group.objects.filter(id=group_id)[0]

        from_date = datetime.datetime.now() - datetime.timedelta(days=7)
        posts = Post.objects.filter(group=_group, created_time__range=[from_date, datetime.datetime.now()]) \
            .extra(
            select={'field_sum': 'like_count + comment_count'},
            order_by=('-field_sum',)
        )

        all_posts = Post.objects.filter(group=_group) \
            .extra(select={'date': connections[Post.objects.db].ops.date_trunc_sql('month', 'created_time')}) \
            .values('date') \
            .annotate(p_count=Count('created_time'))

        all_comments = Comment.objects.filter(group=_group) \
            .extra(select={'date': connections[Comment.objects.db].ops.date_trunc_sql('month', 'created_time')}) \
            .values('date') \
            .annotate(c_count=Count('created_time'))

        raw_data_source = list(zip(all_posts, all_comments))
        data_source = [{'date': x.get('date')[:7], 'profit1': x.get('p_count'), 'profit2': y.get('c_count')} for x, y in
                       raw_data_source]

        print(data_source)

    elif request.method == "POST":
        pass

    return render(
        request,
        'archive/group/analysis.html',
        {
            'groups': _groups,
            'group': _group,
            'posts': posts,
            'data_source': data_source,
        }
    )
