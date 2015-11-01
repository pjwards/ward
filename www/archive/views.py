from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connections
from django.db.models import Count, Sum
from django.utils import timezone

import logging
import datetime

from . import tasks
from .utils import date_utils
from .fb_query import get_feed_query
from .models import Group, Post, Comment
from .fb_request import FBRequest

logger = logging.getLogger(__name__)
fb_request = FBRequest()


def groups(request):
    """
    Get a group list by HTTP GET Method and enter a group by HTTP POST METHOD

    :param request: request
    :return: render
    """
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


def group(request, group_id):
    """
    Display a group page by HTTP GET METHOD

    :param request: request
    :param group_id: group id
    :return: render
    """
    if request.method == "GET":
        _groups = Group.objects.all()
        _group = Group.objects.filter(id=group_id)[0]

        from_date, to_date = date_utils.week_delta()
        posts = Post.objects.filter(group=_group, created_time__range=[from_date, to_date]) \
                    .extra(
            select={'field_sum': 'like_count + comment_count'},
            order_by=('-field_sum',)
        )[:10]

    elif request.method == "POST":
        pass

    return render(
        request,
        'archive/group/analysis.html',
        {
            'groups': _groups,
            'group': _group,
            'posts': posts,
        }
    )


def group_store(request, group_id):
    """
    Store group method

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    if not Group.objects.filter(id=group_id).exists():
        return redirect(reverse('archive:groups') + '?error=error2')

    tasks.store_group_feed.delay(group_id, get_feed_query(10, 100))
    return HttpResponseRedirect(reverse('archive:groups'))


def group_update(request, group_id):
    """
    Update group method

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    if not Group.objects.filter(id=group_id).exists():
        return redirect(reverse('archive:groups') + '?error=error2')

    if tasks.update_group_feed.delay(group_id, get_feed_query(10, 100)):
        return HttpResponseRedirect(reverse('archive:groups'))


def group_issue(request, group_id):
    pass


def group_statistics(reqeust, group_id):
    _group = Group.objects.filter(id=group_id)[0]

    method = reqeust.GET.get('method', 'month')
    from_date = reqeust.GET.get('from', None)
    to_date = reqeust.GET.get('to', None)

    # if from_date:
    #     if to_date:
    #         all_posts = Post.objects.filter(group=_group, created_time__gt=from_date, created_time__lt=to_date)
    #         all_comments = Comment.objects.filter(group=_group, created_time__gt=from_date, created_time__lt=to_date)
    #     else:
    #         all_posts = Post.objects.filter(group=_group, created_time__gt=from_date)
    #         all_comments = Comment.objects.filter(group=_group, created_time__gt=from_date)
    # elif to_date:
    #     all_posts = Post.objects.filter(group=_group, created_time__lt=to_date)
    #     all_comments = Comment.objects.filter(group=_group, created_time__lt=to_date)
    # else:
    #     all_posts = Post.objects.filter(group=_group)
    #     all_comments = Comment.objects.filter(group=_group)

    all_posts = get_objects_by_time(_group, Post, from_date, to_date)
    all_comments = get_objects_by_time(_group, Comment, from_date, to_date)

    all_posts = all_posts.extra(
        select={'date': connections[Post.objects.db].ops.date_trunc_sql(method, 'created_time')}) \
        .values('date') \
        .annotate(p_count=Count('created_time'))

    all_comments = all_comments.extra(
        select={'date': connections[Comment.objects.db].ops.date_trunc_sql(method, 'created_time')}) \
        .values('date') \
        .annotate(c_count=Count('created_time'))

    if method == 'year':
        date_len = 4
    elif method == 'month':
        date_len = 7
    else:
        date_len = 10
    raw_data_source = list(zip(all_posts, all_comments))

    if raw_data_source:
        data_source = [{'date': x.get('date')[:date_len], 'posts': x.get('p_count'), 'comments': y.get('c_count')}
                       for x, y in raw_data_source]

    return JsonResponse({'statistics': data_source})


def get_objects_by_time(_group, model, from_date=None, to_date=None):
    if from_date:
        if to_date:
            return model.objects.filter(group=_group, created_time__gt=from_date, created_time__lt=to_date)
        else:
            return model.objects.filter(group=_group, created_time__gt=from_date)
    elif to_date:
        return model.objects.filter(group=_group, created_time__lt=to_date)
    else:
        return model.objects.filter(group=_group)
