import logging
import operator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connections
from django.db.models import Count, Max
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .rest.serializer import *
from .rest.pagination import *
from . import tasks
from .utils import date_utils
from .fb_query import get_feed_query
from .models import User, Group, Post, Comment
from .fb_request import FBRequest

logger = logging.getLogger(__name__)
fb_request = FBRequest()


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


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


def group_analysis(request, group_id):
    """
    Display a group analysis page by HTTP GET METHOD

    :param request: request
    :param group_id: group id
    :return: render
    """
    _groups = Group.objects.all()
    _group = get_object_or_404(Group, pk=group_id)

    return render(
        request,
        'archive/group/analysis.html',
        {
            'groups': _groups,
            'group': _group,
        }
    )


def group_user(request, group_id):
    """
    Display a group user page by HTTP GET METHOD

    :param request: request
    :param group_id: group id
    :return: render
    """
    _groups = Group.objects.all()
    _group = get_object_or_404(Group, pk=group_id)

    return render(
        request,
        'archive/group/user.html',
        {
            'groups': _groups,
            'group': _group,
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


def group_statistics(request, group_id):
    """
    Get statistics from group.

    method : year | month | day | hour from HTTP Request
    from_date : start day from HTTP Request
    to_date : to day from HTTP Request

    :param request: request
    :param group_id: group_id
    :return: json
    """
    _group = get_object_or_404(Group, pk=group_id)

    method = request.GET.get('method', 'month')
    from_date = request.GET.get('from', None)
    to_date = request.GET.get('to', None)

    if method != 'year' and method != 'month' and method != 'day' and method != 'hour' and method != 'hour_total':
        raise ValueError(
            "Method can be used 'year', 'month', 'day', 'hour' or 'hour_total'. Input method:" + method)

    all_posts = get_objects_by_time(_group, Post, from_date, to_date)
    all_comments = get_objects_by_time(_group, Comment, from_date, to_date)

    # Method Dictionary for group by time
    dic = {
        'year': 'strftime("%%Y", created_time)',
        'month': 'strftime("%%Y-%%m", created_time)',
        'day': 'strftime("%%Y-%%m-%%d", created_time)',
        'hour': 'strftime("%%Y-%%m-%%d-%%H", created_time)',
        'hour_total': 'strftime("%%H", created_time)',
    }

    all_posts = all_posts.extra({'date': dic[method]}).order_by().values('date').annotate(p_count=Count('created_time'))
    all_comments = all_comments.extra({'date': dic[method]}).order_by().values('date').annotate(
        c_count=Count('created_time'))

    post_max_cnt = all_posts.aggregate(Max('p_count'))
    comment_max_cnt = all_comments.aggregate(Max('c_count'))

    if method == 'year':
        date_start_len = 0
        date_end_len = 4
    elif method == 'month':
        date_start_len = 2
        date_end_len = 7
    elif method == 'day':
        date_start_len = 5
        date_end_len = 10
    elif method == 'hour':
        date_start_len = 8
        date_end_len = 13
    else:
        date_start_len = 0
        date_end_len = 2

    data_source = {}

    for comment in all_comments:
        dic = dict()
        dic["date"] = comment.get("date")[date_start_len:date_end_len]
        dic["posts"] = 0
        dic["comments"] = comment.get("c_count")
        data_source[comment.get("date")] = dic

    for post in all_posts:
        if post.get("date") in data_source:
            data_source[post.get("date")]["posts"] = post.get("p_count")
        else:
            dic = dict()
            dic["date"] = post.get("date")[date_start_len:date_end_len]
            dic["posts"] = post.get("p_count")
            dic["comments"] = 0
            data_source[post.get("date")] = dic

    return JsonResponse({
        'statistics': [data_source[key] for key in sorted(data_source.keys())],
        'post_max_cnt': post_max_cnt["p_count__max"],
        'comment_max_cnt': comment_max_cnt["c_count__max"]})


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
            if from_date == to_date:
                from_date, to_date = date_utils.date_range(date_utils.get_date_from_str(from_date), 1)
                return model.objects.filter(group=_group, created_time__gt=from_date, created_time__lt=to_date)
            return model.objects.filter(group=_group, created_time__gt=from_date, created_time__lt=to_date)
        else:
            return model.objects.filter(group=_group, created_time__gt=from_date)
    elif to_date:
        return model.objects.filter(group=_group, created_time__lt=to_date)
    else:
        return model.objects.filter(group=_group)


# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User View Set
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Group View Set
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @detail_route()
    def post_issue(self, request, pk=None):
        """
        Return Hot Comment Issue for group
        """
        posts = self.get_issue(Post)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def comment_issue(self, request, pk=None):
        """
        Return Hot Comment Issue for group
        """
        comments = self.get_issue(Comment)
        return self.response_models(comments, request, CommentSerializer)

    @detail_route()
    def post_archive(self, request, pk=None):
        """
        Return Post archive for group
        """
        posts = self.get_archive(Post)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def comment_archive(self, request, pk=None):
        """
        Return Comment archive for group
        """
        comments = self.get_archive(Comment)
        return self.response_models(comments, request, CommentSerializer)

    @detail_route()
    def activity(self, request, pk=None):
        """
        Return User for group activity
        """
        users_post = self.get_activity()
        return self.response_models(users_post, request, ActivityUserSerializer)

    def response_models(self, models, request, model_serializer):
        """
        Return response for models with pagination

        :param models: models
        :param request: request
        :param model_serializer: model_serializer
        :return: response
        """
        page = self.paginate_queryset(models)
        if page is not None:
            serializers = model_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializers.data)

        serializers = model_serializer(models, many=True, context={'request': request})
        return Response(serializers.data)

    def get_issue(self, model):
        """
        Get hot issue models from group.

        from_date : start day from HTTP Request
        to_date : to day from HTTP Request

        :param model: model to get issue
        :return: result models
        """
        _group = self.get_object()

        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)

        # If from_date and to_date aren't exist, it has seven days range from seven days ago to today.
        if not from_date and not to_date:
            from_date, to_date = date_utils.week_delta()

        models = get_objects_by_time(_group, model, from_date, to_date)

        models = models.extra(
            select={'field_sum': 'like_count + comment_count'},
            order_by=('-field_sum',)
        )

        return models

    def get_archive(self, model):
        """
        Get archive models from group.

        from_date : day to find archives from HTTP Request

        :param model: model to get archive
        :return: result models
        """
        _group = self.get_object()

        from_date = self.request.query_params.get('from', None)

        if from_date:
            from_date, to_date = date_utils.date_range(date_utils.get_date_from_str(from_date), 1)
        else:
            from_date, to_date = date_utils.date_range(date_utils.get_today(), 1)

        models = get_objects_by_time(_group, model, from_date, to_date).order_by('-created_time')
        return models

    def get_activity(self):
        """
        Get user activity

        :return: result models
        """
        _group = self.get_object()

        method = self.request.query_params.get('method', 'total')
        model = self.request.query_params.get('model', None)

        if method != 'total' and method != 'week' and method != 'month':
            raise ValueError("Method can be used 'total', 'week', or 'month'. Input method:" + method)
        if model != 'post' and model != 'comment':
            raise ValueError("Model can be used 'post' or 'comment'. Input model:" + model)

        if method == 'total':
            return _group.user_set.annotate(count=Count(model + 's')).order_by('-count')
        elif method == 'month':
            to_date, from_date = date_utils.date_range(date_utils.get_today(), -30)
        else:
            to_date, from_date = date_utils.date_range(date_utils.get_today(), -7)

        if model == 'post':
            return _group.user_set.filter(posts__created_time__gt=from_date, posts__created_time__lt=to_date)\
                .annotate(count=Count('posts')).order_by('-count')
        else:
            return _group.user_set.filter(comments__created_time__gt=from_date, comments__created_time__lt=to_date)\
                .annotate(count=Count('comments')).order_by('-count')


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Post View Set
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Comment View Set
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MediaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Media View Set
    """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class AttachmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Attachment View Set
    """
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
