import logging
import collections
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db import connections
from django.db.models import Count, Max
from rest_framework import viewsets
from rest_framework.decorators import detail_route, renderer_classes
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

        tasks.store_group_feed.delay(_group.id, get_feed_query(100, 100))

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

    tasks.store_group_feed.delay(group_id, get_feed_query(100, 100))
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

    if tasks.update_group_feed.delay(group_id, get_feed_query(100, 100)):
        return HttpResponseRedirect(reverse('archive:groups'))


def group_search(request, group_id):
    """
    Search from group

    :param request: request
    :param group_id: group_id
    :return: searched data
    """
    _groups = Group.objects.all()
    _group = get_object_or_404(Group, pk=group_id)

    search = request.GET['q']
    if not search:
        search = None

    return render(
        request,
        'archive/group/search.html',
        {
            'groups': _groups,
            'group': _group,
            'search': search,
        }
    )


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
    @renderer_classes((JSONRenderer,))
    def statistics(self, request, pk=None):
        """
        Return Statistics for group

        method : year | month | day | hour from HTTP Request
        from_date : start day from HTTP Request
        to_date : to day from HTTP Request

        :param request: request
        :param pk: pk
        :return: json response
        """
        method = self.request.query_params.get('method', 'month')
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)

        if from_date:
            from_date = date_utils.get_date_from_str(from_date)
        if to_date:
            to_date = date_utils.get_date_from_str(to_date)

        if method != 'year' and method != 'month' and method != 'day' and method != 'hour' and method != 'hour_total':
            raise ValueError(
                "Method can be used 'year', 'month', 'day', 'hour' or 'hour_total'. Input method:" + method)

        all_posts = self.get_objects_by_time(Post, from_date, to_date)
        all_comments = self.get_objects_by_time(Comment, from_date, to_date)

        # Method Dictionary for group by time
        dic = {
            'year': 'strftime("%%Y", created_time)',
            'month': 'strftime("%%Y-%%m", created_time)',
            'day': 'strftime("%%Y-%%m-%%d", created_time)',
            'hour': 'strftime("%%Y-%%m-%%d-%%H", created_time)',
            'hour_total': 'strftime("%%H", created_time)',
        }

        all_posts = all_posts.extra({'date': dic[method]}).order_by().values('date') \
            .annotate(p_count=Count('created_time'))
        all_comments = all_comments.extra({'date': dic[method]}).order_by().values('date') \
            .annotate(c_count=Count('created_time'))

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

        return Response({
            'statistics': [data_source[key] for key in sorted(data_source.keys())],
            'post_max_cnt': post_max_cnt["p_count__max"],
            'comment_max_cnt': comment_max_cnt["c_count__max"]})

    @detail_route()
    def post_issue(self, request, pk=None):
        """
        Return Hot Comment Issue for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        posts = self.get_issue(Post)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def comment_issue(self, request, pk=None):
        """
        Return Hot Comment Issue for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        comments = self.get_issue(Comment)
        return self.response_models(comments, request, CommentSerializer)

    @detail_route()
    def post_archive(self, request, pk=None):
        """
        Return Post archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        posts = self.get_archive(Post)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def comment_archive(self, request, pk=None):
        """
        Return Comment archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        comments = self.get_archive(Comment)
        return self.response_models(comments, request, CommentSerializer)

    @detail_route()
    def activity(self, request, pk=None):
        """
        Return User for group activity

        :param request: request
        :param pk: pk
        :return: response model
        """
        users_post = self.get_activity()
        return self.response_models(users_post, request, ActivityUserSerializer)

    @detail_route()
    @renderer_classes((JSONRenderer,))
    def proportion(self, request, pk=None):
        """
        Return User Proportion for group

        :param request: request
        :param pk: pk
        :return: json respomse
        """
        _group = self.get_object()

        posts = {}
        p_counts = _group.user_set.annotate(p_count=Count('posts')).values('p_count')

        comments = {}
        c_counts = _group.user_set.annotate(c_count=Count('comments')).values('c_count')

        for p_count in p_counts:
            posts[p_count.get('p_count')] = posts.get(p_count.get('p_count'), 0) + 1

        for c_count in c_counts:
            comments[c_count.get('c_count')] = comments.get(c_count.get('c_count'), 0) + 1

        return Response({'posts': collections.OrderedDict(sorted(posts.items())),
                         'comments': collections.OrderedDict(sorted(comments.items()))})

    @detail_route()
    def user_archive(self, request, pk=None):
        """
        Return User Archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()
        search = self.request.query_params.get('q', '')

        if search:
            return self.response_models(_group.user_set.order_by('name').search(search), request, UserSerializer)
        else:
            return self.response_models(_group.user_set.order_by('name'), request, UserSerializer)

    @detail_route()
    def user_search(self, request, pk=None):
        """
        Return user search for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()

        search = self.request.query_params.get('q', '')
        return self.response_models(_group.user_set.search(search), request, UserSerializer)

    @detail_route()
    def post_search(self, request, pk=None):
        """
        Return post search for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()

        search = self.request.query_params.get('q', '')
        return self.response_models(_group.post_set.search(search), request, PostSerializer)

    @detail_route()
    def comment_search(self, request, pk=None):
        """
        Return comment search for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()

        search = self.request.query_params.get('q', '')
        return self.response_models(_group.comment_set.search(search), request, CommentSerializer)

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

    def get_objects_by_time(self, model, from_date=None, to_date=None):
        """
        Get objects between from_date and to_date.

        :param model: model
        :param from_date: start_date
        :param to_date: end_date
        :return: objects
        """
        _group = self.get_object()

        if from_date:
            from_date = date_utils.combine_min_time(from_date)
        if to_date:
            to_date = date_utils.combine_max_time(to_date)

        if from_date:
            if to_date:
                if from_date == to_date:
                    return model.objects.filter(group=_group, created_time__range=[from_date, to_date])
                return model.objects.filter(group=_group, created_time__range=[from_date, to_date])
            else:
                return model.objects.filter(group=_group, created_time__gte=from_date)
        elif to_date:
            return model.objects.filter(group=_group, created_time__lte=to_date)
        else:
            return model.objects.filter(group=_group)

    def get_issue(self, model):
        """
        Get hot issue models from group.

        from_date : start day from HTTP Request
        to_date : to day from HTTP Request

        :param model: model to get issue
        :return: result models
        """
        from_date = self.request.query_params.get('from', None)
        to_date = self.request.query_params.get('to', None)

        # If from_date and to_date aren't exist, it has seven days range from seven days ago to today.
        if not from_date and not to_date:
            from_date, to_date = date_utils.week_delta()

        if from_date:
            from_date = date_utils.get_date_from_str(from_date)
        if to_date:
            to_date = date_utils.get_date_from_str(to_date)

        models = self.get_objects_by_time(model, from_date, to_date)

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
        from_date = self.request.query_params.get('from', None)

        if from_date:
            from_date, to_date = date_utils.date_range(date_utils.get_date_from_str(from_date), 1)
        else:
            from_date, to_date = date_utils.date_range(date_utils.get_today(), 1)

        models = self.get_objects_by_time(model, from_date, to_date).order_by('-created_time')
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
            return _group.user_set.filter(posts__created_time__gt=from_date, posts__created_time__lt=to_date) \
                .annotate(count=Count('posts')).order_by('-count')
        else:
            return _group.user_set.filter(comments__created_time__gt=from_date, comments__created_time__lt=to_date) \
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
