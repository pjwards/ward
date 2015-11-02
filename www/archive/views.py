from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connections
from django.db.models import Count, Sum
from django.forms.models import model_to_dict
from django.utils import timezone

from rest_framework import viewsets
from .serializer import *

import logging
import datetime

from . import tasks
from .utils import date_utils
from .fb_query import get_feed_query
from .models import User, Group, Post, Comment
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
        'archive/group/base.html',
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


def get_issue(request, group_id):
    """
    Get hot issue posts from group.

    length : 20(default) | 50 | 100 from HTTP Request
    from_date : start day from HTTP Request
    to_date : to day from HTTP Request

    :param request: request
    :param group_id: group_id
    :return: (group, issue posts)
    """
    _group = Group.objects.filter(id=group_id)[0]

    length = int(request.GET.get('len', 20))
    from_date = request.GET.get('from', None)
    to_date = request.GET.get('to', None)

    # If from_date and to_date aren't exist, it has seven days range from seven days ago to today.
    if from_date is None and to_date is None:
        from_date, to_date = date_utils.week_delta()

    posts = get_objects_by_time(_group, Post, from_date, to_date)

    posts = posts.extra(
        select={'field_sum': 'like_count + comment_count'},
        order_by=('-field_sum',)
    )

    posts_len = len(posts)
    if posts_len < length:
        length = posts_len

    return _group, posts[:length]


def group_issue(request, group_id):
    """
    Get hot issue posts by using 'get_issue' method.
    It returns rendered template.

    :param request: request
    :param group_id: group_id
    :return: rendered template
    """
    _group, posts = get_issue(request, group_id)

    return render(
        request,
        'archive/group/issue.html',
        {
            'group': _group,
            'posts': posts,
        }
    )


def group_issue_json(request, group_id):
    """
    Get hot issue posts by using 'get_issue' method.
    It returns json.

    :param request: request
    :param group_id: group_id
    :return: json
    """
    _group, posts = get_issue(request, group_id)

    group_dict = model_to_dict(_group)
    posts_dict = [model_to_dict(post) for post in posts]

    return JsonResponse({
        'group': group_dict,
        'posts': posts_dict,
    })


def group_statistics(request, group_id):
    """
    Get statistics from group.

    method : year | month | day from HTTP Request
    from_date : start day from HTTP Request
    to_date : to day from HTTP Request

    :param request: request
    :param group_id: group_id
    :return: json
    """
    _group = Group.objects.filter(id=group_id)[0]

    method = request.GET.get('method', 'month')
    from_date = request.GET.get('from', None)
    to_date = request.GET.get('to', None)

    if method != 'year' and method != 'month' and method != 'day':
        raise ValueError("Method can be used 'year' or 'month' or 'day'. Input method:" + method)

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
    """
    Get objects between from_date and to_date.

    :param _group: _group
    :param model: model
    :param from_date: start_date
    :param to_date: end_date
    :return: objects
    """
    if from_date:
        if to_date:
            return model.objects.filter(group=_group, created_time__gt=from_date, created_time__lt=to_date)
        else:
            return model.objects.filter(group=_group, created_time__gt=from_date)
    elif to_date:
        return model.objects.filter(group=_group, created_time__lt=to_date)
    else:
        return model.objects.filter(group=_group)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
