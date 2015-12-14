from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
import logging
from django.core.urlresolvers import reverse
from django.db.models import Count, Max
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from rest_framework import viewsets
from rest_framework.decorators import detail_route, renderer_classes, list_route
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from archive.fb.fb_query import get_feed_query, get_comment_query
from archive.fb.fb_request import FBRequest
from archive.fb.fb_lookup import lookup_id
from allauth.socialaccount.models import SocialAccount
from . import tasks
from .rest.serializer import *
from .utils import date_utils

logger = logging.getLogger(__name__)
fb_request = FBRequest()


def groups(request):
    """
    Get a group list by HTTP GET Method and enter a group by HTTP POST METHOD

    :param request: request
    :return: render
    """
    if request.method == "GET":
        return render(request, 'archive/group/list.html', {})
    elif request.method == "POST":
        # Get a url and validate the url
        fb_url = request.POST.get("fb_url", None)
        if fb_url is None:
            error = 'Did not exist a url.'
            return JsonResponse({'error': error})

        # Get a group id from the url and validate the group id
        group_id = lookup_id(fb_url)
        if group_id is None:
            error = 'Did not exist the group or enroll the wrong url.'
            return JsonResponse({'error': error})

        # Get group data from graph api and validate the group data
        group_data = fb_request.group(group_id)
        if group_data is None:
            error = 'Did not exist group or privacy group.'
            return JsonResponse({'error': error})

        # Check the group exist
        if Group.objects.filter(id=group_data.get('id')).exists():
            error = 'This group is already exist.'
            return JsonResponse({'error': error})

        # Store the group
        _group = tasks.store_group(group_data)

        if settings.ARCHIVE_GROUP_AUTO_SAVE:
            tasks.store_group_feed.delay(_group.id, get_feed_query(), settings.ARCHIVE_USE_CELERY, True)

        return JsonResponse({'success': 'Success to enroll ' + _group.id})


@user_passes_test(lambda u: u.is_superuser)
def groups_admin(request):
    """
    Get a group list by HTTP GET Method and enter a group by HTTP POST METHOD For Admin

    :param request: request
    :return: render
    """
    if request.method == "GET":
        return render(request, 'archive/group/list_admin.html', {})


def group_analysis(request, group_id):
    """
    Display a group analysis page by HTTP GET METHOD

    :param request: request
    :param group_id: group id
    :return: render
    """
    _groups = Group.objects.all().order_by('name')
    _group = get_object_or_404(Group, pk=group_id)
    posts = Post.objects.filter(group=_group, created_time__range=date_utils.week_delta())

    return render(
        request,
        'archive/group/analysis.html',
        {
            'groups': _groups,
            'group': _group,
            'posts': posts,
        }
    )


def group_user(request, group_id):
    """
    Display a group user page by HTTP GET METHOD

    :param request: request
    :param group_id: group id
    :return: render
    """
    _groups = Group.objects.all().order_by('name')
    _group = get_object_or_404(Group, pk=group_id)
    posts = Post.objects.filter(group=_group, created_time__range=date_utils.week_delta())

    return render(
        request,
        'archive/group/user.html',
        {
            'groups': _groups,
            'group': _group,
            'posts': posts,
        }
    )


def group_search(request, group_id):
    """
    Search from group

    :param request: request
    :param group_id: group_id
    :return: searched data
    """
    _groups = Group.objects.all().order_by('name')
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


@login_required
def group_management(request, group_id):
    """
    Manage group

    :param request: request
    :param group_id: group_id
    :return: searched data
    """
    _group = get_object_or_404(Group, pk=group_id)
    if not request.user.is_superuser:
        social_account = SocialAccount.objects.filter(user=request.user)
        if not social_account or _group.owner.id != SocialAccount.objects.filter(user=request.user)[0].uid:
            return HttpResponseForbidden()

    if request.method == "GET":
        _groups = Group.objects.all()
        return render(
            request,
            'archive/group/management.html',
            {
                'groups': _groups,
                'group': _group,
            }
        )
    elif request.method == "POST":
        # Get a model and validate a model
        model = request.POST.get("model", None)
        if model is None:
            error = 'Did not exist this model.'
            return JsonResponse({'error': error})

        # Get a access token and validate the access token
        access_token = request.POST.get("access_token", None)
        if not access_token:
            error = 'Did not exist this access token.'
            return JsonResponse({'error': error})

        # Get a check box by using model
        if model == 'post':
            check_box = request.POST.getlist('del_post')
        elif model == 'comment':
            check_box = request.POST.getlist('del_comment')
        else:
            error = 'This model did not validate.'
            return JsonResponse({'success': error})

        # Validate the check box
        if not check_box:
            error = 'Did not check any check box.'
            return JsonResponse({'error': error})

        # Generate fb request by using the access token
        fb_request_del = FBRequest(access_token=access_token)

        # Validate access token
        res, e = fb_request_del.validate_token()
        if not res:
            return JsonResponse({'error': e})

        # Delete object in check box
        total = len(check_box)
        error = set()
        success = 0
        fail = 0
        for object_id in check_box:
            # res, e = tasks.delete_group_content(object_id, model)
            res, e = tasks.delete_group_content_by_fb(object_id, model, fb_request_del)
            if res:
                success += 1
            else:
                fail += 1
                error.add(e)

        # Post and comment count in group size change
        tasks.check_cp_cnt_group(_group)

        # Return result json
        return JsonResponse(
            {
                'model': model,
                'result': {'total': total, 'success': success, 'fail': fail},
                'error': list(error)
            })


@user_passes_test(lambda u: u.is_superuser)
def group_store(request, group_id):
    """
    Store group method

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    if not Group.objects.filter(id=group_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist group.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    tasks.store_group_feed.delay(group_id, get_feed_query(), settings.ARCHIVE_USE_CELERY, True)
    return HttpResponseRedirect(reverse('archive:groups_admin'))


def group_update(request, group_id):
    """
    Update group method

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    if not Group.objects.filter(id=group_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist group.'
        return render(request, 'archive/group/list.html', {'latest_group_list': latest_group_list, 'error': error})

    if tasks.update_group_feed.delay(group_id, get_feed_query(), True, True):
        return HttpResponseRedirect(reverse('archive:groups'))


@user_passes_test(lambda u: u.is_superuser)
def group_check(request, group_id):
    """
    Check group method

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    p_limit = int(request.POST.get("post_limit", '100'))
    c_limit = int(request.POST.get("comment_limit", '100'))

    if not Group.objects.filter(id=group_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist group.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    tasks.check_group_feed.delay(group_id, get_feed_query(p_limit, c_limit), settings.ARCHIVE_USE_CELERY, True)
    return HttpResponseRedirect(reverse('archive:groups_admin'))


@user_passes_test(lambda u: u.is_superuser)
def group_comments_check(request, group_id):
    """
    Check group comments

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    if not Group.objects.filter(id=group_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist group.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    tasks.check_group_comments.delay(group_id, get_feed_query(), settings.ARCHIVE_USE_CELERY, True)
    return HttpResponseRedirect(reverse('archive:groups_admin'))


def user(request, user_id):
    """
    Display a user

    :param request: request
    :param user_id: user id
    :return: render
    """
    _user = get_object_or_404(FBUser, id=user_id)
    _groups = _user.groups

    return render(
        request,
        'archive/user/user.html',
        {
            'user': _user,
            'groups': _groups.all(),
        }
    )


def report(request, object_id):
    """
    Report object

    :param request: request
    :param object_id: object id
    :return: render
    """

    if request.method == "POST":
        _report = Report()
        is_exist = False  # report is already exist
        try:
            # Post id is bigger than 20
            if len(object_id) > 20:
                _object = Post.objects.get(pk=object_id)
                if not Report.objects.filter(post=_object).exists():
                    _report.post = _object
                else:
                    _report = Report.objects.filter(post=_object)[0]
                    is_exist = True
            else:
                _object = Comment.objects.get(pk=object_id)
                if not Report.objects.filter(comment=_object).exists():
                    _report.comment = _object
                else:
                    _report = Report.objects.filter(comment=_object)[0]
                    is_exist = True
        except (Post.DoesNotExist, Comment.DoesNotExist):
            error = 'Did not exist this object.'
            return JsonResponse({'error': error})

        # If report is already exist, renew the report.
        if is_exist:
            _report.status = 'new'
            _report.updated_time = date_utils.timezone.now()
            _report.save()
        else:
            _report.group = _object.group
            _report.user = _object.user
            _report.save()
        return JsonResponse({'success': 'Report success'})


@user_passes_test(lambda u: u.is_superuser)
def report_action(request, report_id, action):
    """
    Report action

    :param request: request
    :param report_id: report id
    :param action: action
    :return: render
    """
    if request.method == "POST":
        _report = get_object_or_404(Report, id=report_id)

        # report is already deleted.
        if _report.status == 'deleted':
            error = 'You could not this action when status is deleted.'
            return JsonResponse({'error': error})

        # Do actions
        if action == 'hide':
            _report.status = 'hide'
            _report.save()
            if _report.post:
                _report.post.is_show = False
                _report.post.save()
            elif _report.comment:
                _report.comment.is_show = False
                _report.comment.save()
        elif action == 'show':
            _report.status = 'show'
            _report.save()
            if _report.post:
                _report.post.is_show = True
                _report.post.save()
            elif _report.comment:
                _report.comment.is_show = True
                _report.comment.save()
        elif action == 'checked':
            if _report.status == 'hide':
                error = 'You could not this action when status is hide.'
                return JsonResponse({'error': error})
            _report.status = 'checked'
            _report.save()
        elif action == 'delete':
            if _report.post:
                res, e = tasks.delete_group_content(_report.post.id, 'post')
            elif _report.comment:
                res, e = tasks.delete_group_content(_report.comment.id, 'comment')

            if res:
                _report.status = 'deleted'
                _report.save()
            else:
                return JsonResponse({'error': e})
        else:
            error = 'Did not exist this action.'
            return JsonResponse({'error': error})
        return JsonResponse({'success': 'Report action success'})


@user_passes_test(lambda u: u.is_superuser)
def reports(request):
    """
    Display reports

    :param request: request
    :return: render
    """

    return render(request, 'archive/reports.html', {})


@login_required()
def ward(request, object_id):
    """
    Report object

    :param request: request
    :param object_id: object id
    :return: render
    """

    if request.method == "POST":
        _user = request.user
        _ward = Ward()
        is_exist = False  # report is already exist
        try:
            # Post id is bigger than 20
            if len(object_id) > 20:
                _object = Post.objects.get(pk=object_id)
                if not Ward.objects.filter(user=_user, post=_object).exists():
                    _ward.post = _object
                else:
                    _ward = Ward.objects.filter(user=_user, post=_object)[0]
                    is_exist = True
            else:
                _object = Comment.objects.get(pk=object_id)
                if not Ward.objects.filter(user=_user, comment=_object).exists():
                    _ward.comment = _object
                else:
                    _ward = Ward.objects.filter(user=_user, comment=_object)[0]
                    is_exist = True
        except (Post.DoesNotExist, Comment.DoesNotExist):
            error = 'Did not exist this object.'
            return JsonResponse({'error': error})

        # If report is already exist, renew the report.
        if is_exist:
            _ward.created_time = date_utils.timezone.now()
            _ward.updated_time = date_utils.timezone.now()
            _ward.save()
        else:
            _ward.group = _object.group
            _ward.user = _user
            _ward.save()
        return JsonResponse({'success': 'Ward success'})
    elif request.method == "DELETE":
        try:
            _ward = Ward.objects.get(id=object_id)
        except Ward.DoesNotExist:
            error = 'Did not exist this ward.'
            return JsonResponse({'error': error})

        _user = request.user
        if _ward.user != _user:
            error = 'Did not match the owner.'
            return JsonResponse({'error': error})

        _ward.delete()
        return JsonResponse({'success': 'Delete ward success'})


@login_required()
def ward_update(request, ward_id):
    """
    Update Ward

    :param request: request
    :param ward_id: ward id
    :return: render
    """
    if request.method == "POST":
        _ward = get_object_or_404(Ward, id=ward_id)
        _ward.updated_time = date_utils.timezone.now()
        _ward.save()
        return JsonResponse({'success': 'Ward open success'})


@login_required()
def wards(request):
    """
    Display wards

    :param request: request
    :return: render
    """
    _user = request.user
    _groups = list(set(Group.objects.filter(wards__user=_user).all()))

    return render(
        request,
        'archive/wards.html',
        {
            'groups': _groups,
        }
    )


# ViewSets define the view behavior.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User View Set
    """
    queryset = FBUser.objects.all()
    serializer_class = FBUserSerializer


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
            'year': "date_trunc('year', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'month': "date_trunc('month', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'day': "date_trunc('day', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'hour': "date_trunc('hour', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'hour_total': "date_part('hour', created_time at time zone 'UTC' AT TIME ZONE '+9')",
        }

        # Get posts and comment count in some date
        all_posts = all_posts.extra(select={'date': dic[method]}).order_by().values('date') \
            .annotate(p_count=Count('created_time'))
        all_comments = all_comments.extra(select={'date': dic[method]}).order_by().values('date') \
            .annotate(c_count=Count('created_time'))

        # Max count in above data
        post_max_cnt = all_posts.aggregate(Max('p_count'))
        comment_max_cnt = all_comments.aggregate(Max('c_count'))

        # Value for slice
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

        # Merge post and comment data
        data_source = {}

        for comment in all_comments:
            if method == "hour_total":
                date = '{0:0.0f}'.format(comment.get('date')).zfill(2)
            else:
                date = comment.get("date").isoformat()[:13].replace('T', '-')
            dic = dict()
            dic["date"] = date[date_start_len:date_end_len]
            dic["posts"] = 0
            dic["comments"] = comment.get("c_count")
            data_source[date] = dic

        for post in all_posts:
            if method == "hour_total":
                date = '{0:0.0f}'.format(post.get('date')).zfill(2)
            else:
                date = post.get("date").isoformat()[:13].replace('T', '-')
            if date in data_source:
                data_source[date]["posts"] = post.get("p_count")
            else:
                dic = dict()
                dic["date"] = date[date_start_len:date_end_len]
                dic["posts"] = post.get("p_count")
                dic["comments"] = 0
                data_source[date] = dic

        # Return json data after rearranging data
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
        posts = self.get_issue(Post).exclude(is_show=False)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def comment_issue(self, request, pk=None):
        """
        Return Hot Comment Issue for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        comments = self.get_issue(Comment).exclude(is_show=False)
        return self.response_models(comments, request, CommentSerializer)

    @detail_route()
    def post_archive(self, request, pk=None):
        """
        Return Post archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        posts = self.get_archive(Post).exclude(is_show=False)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def comment_archive(self, request, pk=None):
        """
        Return Comment archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        comments = self.get_archive(Comment).exclude(is_show=False)
        return self.response_models(comments, request, CommentSerializer)

    @detail_route()
    def activity(self, request, pk=None):
        """
        Return User for group activity
        :param request: request
        :param pk: pk
        :return: response model
        """
        users_activity = self.get_activity()
        return self.response_models(users_activity, request, ActivityFBUserSerializer)

    @detail_route()
    @renderer_classes((JSONRenderer,))
    def proportion(self, request, pk=None):
        """
        Return User Proportion for group

        :param request: request
        :param pk: pk
        :return: json respomse
        """
        cursor = connection.cursor()
        _group = self.get_object()

        # Count posts and comments about user in group
        user_count = _group.fbuser_set.count()

        # Get post proportion
        posts = {}
        cursor.execute("""
                SELECT T.count, count(*) FROM
                (SELECT
                  count(user_id) as count
                FROM
                  archive_post
                WHERE
                  group_id = %s
                GROUP BY user_id) AS T
                GROUP BY T.count
                ORDER BY count(*) DESC
                LIMIT 9;
        """, [_group.id])
        p_counts = cursor.fetchall()
        s = 0
        for p_count in p_counts:
            posts[p_count[0]] = p_count[1]
            s += p_count[1]
        posts["others"] = user_count - s

        # Get comment proportion
        comments = {}
        cursor.execute("""
                SELECT T.count, count(*) FROM
                (SELECT
                  count(user_id) as count
                FROM
                  archive_comment
                WHERE
                  group_id = %s
                GROUP BY user_id) AS T
                GROUP BY T.count
                ORDER BY count(*) DESC
                LIMIT 9;
        """, [_group.id])
        c_counts = cursor.fetchall()
        s = 0
        for c_count in c_counts:
            comments[c_count[0]] = c_count[1]
            s += c_count[1]
        comments["others"] = user_count - s

        return Response({'posts': posts,
                         'comments': comments})

    @detail_route()
    def user_archive(self, request, pk=None):
        """
        Return User Archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        cursor = connection.cursor()
        _group = self.get_object()

        search = self.request.query_params.get('q', '')

        if search:
            cursor.execute(
                """
                SELECT
                    UG.fbuser_id as id,
                    U.name as name,
                    U.picture as picture,
                    (SELECT count(*) FROM archive_post WHERE group_id = %s AND user_id = UG.fbuser_id) as p_count,
                    (SELECT count(*) FROM archive_comment WHERE group_id = %s AND user_id = UG.fbuser_id) as c_count
                FROM
                    archive_fbuser_groups as UG
                INNER JOIN archive_fbuser as U
                ON UG.fbuser_id = U.id
                WHERE UG.group_id = %s AND U.name @@ %s
                ORDER BY U.name;
                """, [_group.id, _group.id, _group.id, search])
        else:
            cursor.execute(
                """
                SELECT
                    UG.fbuser_id as id,
                    U.name as name,
                    U.picture as picture,
                    (SELECT count(*) FROM archive_post WHERE group_id = %s AND user_id = UG.fbuser_id) as p_count,
                    (SELECT count(*) FROM archive_comment WHERE group_id = %s AND user_id = UG.fbuser_id) as c_count
                FROM
                    archive_fbuser_groups as UG
                INNER JOIN archive_fbuser as U
                ON UG.fbuser_id = U.id
                WHERE UG.group_id = %s
                ORDER BY U.name;
                """, [_group.id, _group.id, _group.id])
        row = self.dictfetchall(cursor)

        return self.response_models(row, request, ActivityForArchiveFBUserSerializer)

    @staticmethod
    def dictfetchall(cursor):
        """
        Return all rows from a cursor as a dict

        :param cursor: cursor
        """
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
            ]

    @detail_route()
    def post_search(self, request, pk=None):
        """
        Return post search for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        posts = self.group_search_by_check(Post).exclude(is_show=False)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def comment_search(self, request, pk=None):
        """
        Return comment search for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        comments = self.group_search_by_check(Comment).exclude(is_show=False)
        return self.response_models(comments, request, CommentSerializer)

    @detail_route()
    def user_post_archive(self, request, pk=None):
        """
        Return user post archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        posts = self.get_archive_by_user(Post)
        return self.response_models(posts, request, PostSerializer)

    @detail_route()
    def user_comment_archive(self, request, pk=None):
        """
        Return user comment archive for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        comments = self.get_archive_by_user(Comment)
        return self.response_models(comments, request, CommentSerializer)

    @list_route()
    def group_search(self, request):
        """
        Return group search

        :param request: request
        :return: response model
        """
        _groups = self.get_queryset().order_by('-updated_time')
        search = self.request.query_params.get('q', '')
        if search:
            return self.response_models(_groups.search(search), request, GroupSerializer)
        else:
            return self.response_models(_groups, request, GroupSerializer)

    @detail_route()
    @renderer_classes((JSONRenderer,))
    def user_autocomplete(self, request, pk=None):
        """
        User list for auto complete

        :param request: request
        :param pk: pk
        :return: json
        """
        _group = self.get_object()
        users = _group.fbuser_set.values('id', 'name')

        return Response({'users': users})

    @detail_route()
    def blacklist(self, request, pk=None):
        """
        Return blacklist

        :param request: request
        :param pk: pk
        :return: response model
        """
        blacklist = self.get_object().blacklist.all().order_by('-updated_time')
        return self.response_models(blacklist, request, BlacklistSerializer)

    @detail_route()
    def blacklist_user(self, request, pk=None):
        """
        Return blacklist for user

        :param request: request
        :param pk: pk
        :return: response model
        """
        user_id = self.request.query_params.get('user_id', None)
        _user = get_object_or_404(FBUser, id=user_id)

        blacklist = Blacklist.objects.get(group=self.get_object(), user=_user)
        return Response(BlacklistSerializer(blacklist, context={'request': request}).data)

    @detail_route()
    def blacklist_search(self, request, pk=None):
        """
        Return blacklist search for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()

        search = self.request.query_params.get('q', '')

        if search:
            blacklist = _group.fbuser_set.filter(blacklist__group=_group).exclude(blacklist=None).order_by(
                '-blacklist__updated_time').search(search)
        else:
            blacklist = _group.fbuser_set.filter(blacklist__group=_group).exclude(blacklist=None).order_by(
                '-blacklist__updated_time')

        return self.response_models(blacklist, request, BlacklistFBUserSerializer)

    @detail_route()
    def post_ward(self, request, pk=None):
        """
        Return post wards

        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()
        user_id = self.request.query_params.get('user_id', None)
        _user = get_object_or_404(DjangoUser, id=user_id)
        _wards = Ward.objects.filter(group=_group, user=_user).exclude(post=None).order_by('-created_time')
        return self.response_models(_wards, request, WardSerializer)

    @detail_route()
    def comment_ward(self, request, pk=None):
        """
        Return comment wards

        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()
        user_id = self.request.query_params.get('user_id', None)
        _user = get_object_or_404(DjangoUser, id=user_id)
        _wards = Ward.objects.filter(group=_group, user=_user).exclude(comment=None).order_by('-created_time')
        return self.response_models(_wards, request, WardSerializer)

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
        if from_date:
            from_date = date_utils.get_date_from_str(from_date)
        if to_date:
            to_date = date_utils.get_date_from_str(to_date)

        if not from_date and not to_date:
            from_date, to_date = date_utils.week_delta()

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
            from_date = date_utils.get_date_from_str(from_date)
            to_date = from_date
        else:
            from_date = date_utils.get_today()
            to_date = from_date

        models = self.get_objects_by_time(model, from_date, to_date).order_by('-created_time')
        return models

    def get_archive_by_user(self, model):
        """
        Get archive models by user.

        from_date : day to find archives from HTTP Request

        :param model: model to get archive
        :return: result models
        """
        from_date = self.request.query_params.get('from', None)
        to_date = None
        user_id = self.request.query_params.get('user_id', None)
        _user = get_object_or_404(FBUser, id=user_id)

        if from_date:
            from_date = date_utils.get_date_from_str(from_date)
            to_date = from_date

        models = self.get_objects_by_time(model, from_date, to_date).filter(user=_user).order_by('-created_time')
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
            if model == 'post':
                return _group.fbuser_set.filter(posts__group=_group).annotate(count=Count('posts')).order_by('-count')
            else:
                return _group.fbuser_set.filter(comments__group=_group).annotate(count=Count('comments')).order_by(
                    '-count')

        elif method == 'month':
            to_date, from_date = date_utils.date_range(date_utils.get_today(), -30)
        else:
            to_date, from_date = date_utils.date_range(date_utils.get_today(), -7)

        if model == 'post':
            return _group.fbuser_set.filter(posts__group=_group, posts__created_time__gt=from_date,
                                            posts__created_time__lt=to_date) \
                .annotate(count=Count('posts')).order_by('-count')
        else:
            return _group.fbuser_set.filter(comments__group=_group, comments__created_time__gt=from_date,
                                            comments__created_time__lt=to_date) \
                .annotate(count=Count('comments')).order_by('-count')

    def group_search_by_check(self, model):
        """
        Get models by search

        :param model: model
        :return: models
        """
        _group = self.get_object()

        search = self.request.query_params.get('q', '')
        search_check = self.request.query_params.get('c', None)

        if search_check == 'user':
            _user = FBUser.objects.filter(id=search)
            return model.objects.filter(group=_group, user=_user).order_by('-created_time')

        if search:
            return model.objects.filter(group=_group).order_by('-created_time').search(search)
        else:
            return model.objects.filter(group=_group).order_by('-created_time')


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


class BlacklistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Blacklist View Set
    """
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Report View Set
    """
    queryset = Report.objects.all().order_by('-updated_time')
    serializer_class = ReportSerializer


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Ward View Set
    """
    queryset = Ward.objects.all().order_by('-created_time')
    serializer_class = WardSerializer


def about(request):
    return render(request, 'about.html', {})
