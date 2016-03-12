# The MIT License (MIT)
#
# Copyright (c) 2015 pjwards.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==================================================================================
""" Views for default pages and for django rest framework """
import csv
import json
import urllib.parse
import urllib.request
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import connection
import logging
from django.core.urlresolvers import reverse
from django.db.models import Count, Q, F
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseForbidden, HttpResponse, StreamingHttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User as DjangoUser
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from rest_framework import viewsets
from rest_framework.decorators import detail_route, renderer_classes, list_route
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from archive.fb.fb_query import get_feed_query, get_comment_query, get_feed_with_comment_query
from archive.fb.fb_request import FBRequest
from archive.fb.fb_lookup import lookup_id
from archive.fb import fb_tasks
from allauth.socialaccount.models import SocialAccount
from . import tasks
from .rest.serializer import *
from .utils import date_utils
from archive.models import *
from analysis.models import *

logger = logging.getLogger(__name__)


def about(request):
    """
    About page

    :param request:
    :return:
    """
    return render(request, 'about.html', {})


def request_to_archive_server(request):
    if request.method == "GET":
        parameter = request.GET
    elif request.method == "POST":
        parameter = request.POST

    if not settings.ARCHIVE_SERVER:
        try:
            details = urllib.parse.urlencode(parameter)
            details = details.encode('UTF-8')
            url = urllib.request.Request(settings.ARCHIVE_SERVER_URL + request.path, details)
            url.add_header("User-Agent",
                           "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")
            response_data = urllib.request.urlopen(url).read().decode("utf-8")
        except Exception:
            error = 'Server that enroll facebook group does currently not work.'
            return {'error': error}

        try:
            return json.loads(response_data)
        except Exception:
            pass


@csrf_exempt
def groups(request):
    """
    Get a group list by HTTP GET Method and enter a group by HTTP POST METHOD

    :param request: request
    :return: render
    """
    if request.method == "GET":
        return render(request, 'archive/group/list.html', {})
    elif request.method == "POST":
        # Check this server is archive server
        if not settings.ARCHIVE_SERVER:
            return JsonResponse(request_to_archive_server(request))

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
        fb_request = FBRequest()
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
            tasks.store_group_feed_task.delay(_group.id, get_feed_query(), get_comment_query())

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


def is_interest_group(request, group_id):
    """
    Is interest group?

    :param request: request
    :param group_id: group id
    :return:
    """

    if not request.user.is_authenticated():
        return False

    _user = request.user
    _group = get_object_or_404(Group, id=group_id)

    if InterestGroupList.objects.filter(user=_user, group=_group).exists():
        return True
    return False


def group_analysis(request, group_id):
    """
    Display a group analysis page

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
                'interest_group': is_interest_group(request, group_id),
            }
    )


def group_user(request, group_id):
    """
    Display a group user page

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
                'interest_group': is_interest_group(request, group_id),
            }
    )


def group_archive(request, group_id):
    """
    Display a group archive page

    :param request: request
    :param group_id: group id
    :return: render
    """
    _groups = Group.objects.all().order_by('name')
    _group = get_object_or_404(Group, pk=group_id)
    posts = Post.objects.filter(group=_group, created_time__range=date_utils.week_delta())

    return render(
            request,
            'archive/group/archive.html',
            {
                'groups': _groups,
                'group': _group,
                'posts': posts,
                'interest_group': is_interest_group(request, group_id),
            }
    )


def group_search(request, group_id):
    """
    Display a search page about group

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
                'interest_group': is_interest_group(request, group_id),
            }
    )


@login_required
def group_management(request, group_id):
    """
    Display manage page for group owner

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
        posts = Post.objects.filter(group=_group, created_time__range=date_utils.week_delta())
        return render(
                request,
                'archive/group/management.html',
                {
                    'groups': _groups,
                    'group': _group,
                    'posts': posts,
                    'interest_group': is_interest_group(request, group_id),
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
            res, e = fb_tasks.delete_group_content_by_fb(object_id, model, fb_request_del)
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


'''
@login_required
def group_spam(request, group_id):
    """
    Display spam page for group owner

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
        spams = SpamList.objects.filter(group=_group, last_updated_time__range=date_utils.week_delta())
        return render(
            request,
            'archive/group/spam.html',
            {
                'groups': _groups,
                'group': _group,
                'posts': spams,
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
        if model == 'spam':
            check_box = request.POST.getlist('del_spam')
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
'''


@user_passes_test(lambda u: u.is_superuser)
def group_store(request, group_id):
    """
    Store group method for super user

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    p_limit = int(request.GET.get("post_limit", '100'))
    c_limit = int(request.GET.get("comment_limit", '100'))
    c_c_limit = int(request.GET.get("child_comment_limit", '100'))

    # Check this server is archive server
    if not settings.ARCHIVE_SERVER:
        latest_group_list = Group.objects.order_by('name')
        error = 'This is wrong connection.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    if not Group.objects.filter(id=group_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist group.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    tasks.store_group_feed_task.delay(group_id, get_feed_query(p_limit), get_comment_query(c_limit, c_c_limit))
    return HttpResponseRedirect(reverse('archive:groups_admin'))


@csrf_exempt
def group_update(request, group_id):
    """
    Update group method

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    p_limit = int(request.GET.get("post_limit", '100'))
    c_limit = int(request.GET.get("comment_limit", '100'))

    # Check this server is archive server
    if not settings.ARCHIVE_SERVER:
        latest_group_list = Group.objects.order_by('name')
        request_to_archive_server(request)
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list})

    if not Group.objects.filter(id=group_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist group.'
        return render(request, 'archive/group/list.html', {'latest_group_list': latest_group_list, 'error': error})

    if tasks.update_group_feed_task.delay(group_id, get_feed_with_comment_query(p_limit, c_limit)):
        return HttpResponseRedirect(reverse('archive:groups'))


@user_passes_test(lambda u: u.is_superuser)
def group_check(request, group_id):
    """
    Check group method for super user

    :param request: request
    :param group_id: group id
    :return: if you succeed, redirect groups page
    """
    c_limit = int(request.GET.get("comment_limit", '100'))
    c_c_limit = int(request.GET.get("child_comment_limit", '100'))

    # Check this server is archive server
    if not settings.ARCHIVE_SERVER:
        latest_group_list = Group.objects.order_by('name')
        error = 'This is wrong connection.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    if not Group.objects.filter(id=group_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist group.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    tasks.check_group_task.delay(group_id, get_comment_query(c_limit, c_c_limit))
    return HttpResponseRedirect(reverse('archive:groups_admin'))


@user_passes_test(lambda u: u.is_superuser)
def group_post_check(request, post_id):
    """
    Check post comments for super user

    :param request: request
    :param post_id: post id
    :return: if you succeed, redirect groups page
    """
    c_limit = int(request.GET.get("comment_limit", '100'))
    c_c_limit = int(request.GET.get("child_comment_limit", '100'))

    # Check this server is archive server
    if not settings.ARCHIVE_SERVER:
        latest_group_list = Group.objects.order_by('name')
        error = 'This is wrong connection.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    if not Post.objects.filter(id=post_id).exists():
        latest_group_list = Group.objects.order_by('name')
        error = 'Does not exist post.'
        return render(request, 'archive/group/list_admin.html',
                      {'latest_group_list': latest_group_list, 'error': error})

    tasks.check_group_post_task.delay(post_id, get_comment_query(c_limit, c_c_limit))
    return HttpResponseRedirect(reverse('archive:groups_admin'))


def group_download(request, group_id):
    """
    Download page

    :param request: request
    :param group_id: group id
    :return: render or csv
    """
    _groups = Group.objects.all().order_by('name')
    _group = get_object_or_404(Group, pk=group_id)
    posts = Post.objects.filter(group=_group, created_time__range=date_utils.week_delta())

    if request.method == "GET":
        return render(
                request,
                'archive/group/download.html',
                {
                    'groups': _groups,
                    'group': _group,
                    'posts': posts,
                    'interest_group': is_interest_group(request, group_id),
                }
        )
    elif request.method == "POST":
        model = request.POST.get("model", None)
        from_date = request.POST.get('from', None)
        to_date = request.POST.get('to', None)
        filename = model

        # check model
        if model == 'post':
            model = Post
        elif model == 'comment':
            model = Comment
        else:
            return render(
                    request,
                    'archive/group/download.html',
                    {
                        'groups': _groups,
                        'group': _group,
                        'posts': posts,
                        'interest_group': is_interest_group(request, group_id),
                    }
            )

        # check date
        if from_date:
            filename = filename + '_from_' + from_date
            from_date = date_utils.get_date_from_str(from_date)
            from_date = date_utils.combine_min_time(from_date)
        if to_date:
            filename = filename + '_to_' + to_date
            to_date = date_utils.get_date_from_str(to_date)
            to_date = date_utils.combine_max_time(to_date)

        # get data
        if from_date:
            if to_date:
                if from_date == to_date:
                    data = model.objects.filter(group=_group, created_time__range=[from_date, to_date])
                else:
                    data = model.objects.filter(group=_group, created_time__range=[from_date, to_date])
            else:
                data = model.objects.filter(group=_group, created_time__gte=from_date)
        elif to_date:
            data = model.objects.filter(group=_group, created_time__lte=to_date)
        else:
            data = model.objects.filter(group=_group)

        # get db_column name
        model_field = []
        for field in model._meta.fields:
            if field.get_attname_column()[0] != 'is_show':
                model_field.append(field.get_attname_column()[0])

        # get data for cvs
        data = list(data.order_by('-created_time').values_list(*model_field))
        data.insert(0, model_field)

        # make response for cvs
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in data), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)

        return response


class Echo(object):
    """
    An object that implements just the write method of the file-like interface.
    """
    def write(self, value):
        """
        Write the value by returning it, instead of storing in a buffer.

        :param value: value
        """
        return value


def user(request, user_id):
    """
    Display a user page

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
                'fb_user': _user,
                'groups': _groups.exclude(privacy='CLOSED'),
            }
    )


def report(request, object_id):
    """
    Enroll a report about a spam

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
    Report action like hide, show, checked and delete for super user

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
                res, e = fb_tasks.delete_group_content(_report.post.id, 'post')
            elif _report.comment:
                res, e = fb_tasks.delete_group_content(_report.comment.id, 'comment')

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
    Display report page

    :param request: request
    :return: render
    """

    return render(request, 'archive/reports.html', {})


@login_required()
def ward(request, object_id):
    """
    Enroll ward which is a post or comment saved by user for wathching

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
    Update ward status

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
    Display ward page

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


@login_required()
def alert(request):
    """
    Display alert page

    :param request: request
    :return: render
    """
    return render(
            request,
            'archive/alert.html',
            {
            }
    )


@login_required()
def interest_group(request, group_id):
    """
    Add interest group

    :param request: request
    :param group_id: group id
    :return: render
    """
    if request.method == "GET":
        _user = request.user
        _group = get_object_or_404(Group, id=group_id)

        if InterestGroupList.objects.filter(user=_user, group=_group).exists():
            return JsonResponse({'exist': True})
        return JsonResponse({'exist': False})
    elif request.method == "POST":
        _user = request.user
        _group = get_object_or_404(Group, id=group_id)

        if InterestGroupList.objects.filter(user=_user, group=_group).exists():
            error = 'This group is already added.'
            return JsonResponse({'error': error})

        _interest_group = InterestGroupList(user=_user, group=_group)
        _interest_group.save()
        return JsonResponse({'success': 'Add this group in interest group.'})
    elif request.method == "DELETE":
        _user = request.user
        _group = get_object_or_404(Group, id=group_id)

        _interest_group = InterestGroupList.objects.filter(user=_user, group=_group)
        if not _interest_group.exists():
            error = 'Did not exist this group in interest group list.'
            return JsonResponse({'error': error})

        _interest_group = _interest_group[0]
        if _interest_group.user != _user:
            error = 'Did not match the owner.'
            return JsonResponse({'error': error})

        _interest_group.delete()
        return JsonResponse({'success': 'Delete this group in interest group.'})


# ViewSets define the view behavior for restful api.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    User View Set for django restful framework
    """
    queryset = FBUser.objects.all()
    serializer_class = FBUserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Group View Set for django restful framework
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

        if method != 'year' and method != 'month' and method != 'day' and method != 'hour_total':
            raise ValueError(
                    "Method can be used 'year', 'month', 'day' or 'hour_total'. Input method:" + method)

        statistics_model = self.get_statistics_model(method)
        posts, comments = self.process_memoization(statistics_model, method, from_date, to_date)

        # Return json data after rearranging data
        return Response({
            'posts': posts,
            'comments': comments
        })

    def get_statistics_model(self, method):
        """
        Get statistics model from model

        :param method: method
        :return: statistics model
        """
        if method == 'year':
            return YearGroupStatistics
        elif method == 'month':
            return MonthGroupStatistics
        elif method == 'day':
            return DayGroupStatistics
        elif method == 'hour_total':
            return TimeOverviewGroupStatistics
        else:
            return None

    def process_memoization(self, statistics_model, method, from_date, to_date):
        """
        Process memoization

        :param statistics_model: statistics_model
        :param method: method
        :param from_date: from_date
        :param to_date: to_date
        :return: posts and comments
        """
        # Is memoization?
        if not statistics_model.objects.filter(group=self.get_object()).exists():
            posts, comments = self.get_statistics(method, from_date, to_date)

            for post in posts:
                self.save_statistics_model(statistics_model, post, 'post')
            for comment in comments:
                self.save_statistics_model(statistics_model, comment, 'comment')

            GroupStatisticsUpdateList.update(group=self.get_object(), method=method)

            posts, comments = self.process_statistics(method, posts, comments)
        else:
            # Is ready to update?
            update_list = GroupStatisticsUpdateList.objects.filter(group=self.get_object(), method=method)
            if update_list:
                is_update = update_list[0].is_update()
            else:
                GroupStatisticsUpdateList.update(group=self.get_object(), method=method)
                is_update = False

            # Get statistics from memoization
            posts = statistics_model.objects.filter(group=self.get_object(), model='post').order_by('time')
            comments = statistics_model.objects.filter(group=self.get_object(), model='comment').order_by('time')

            if is_update:
                if method == 'hour_total':
                    update_posts, update_comments = self.get_statistics(method, from_date, to_date)

                    for post in update_posts:
                        self.update_statistics_model(statistics_model, post, 'post')
                    for comment in update_comments:
                        self.update_statistics_model(statistics_model, comment, 'comment')
                else:
                    update_posts = self.get_statistics_by_model(Post, method, posts[len(posts) - 1].time, to_date)
                    update_comments = self.get_statistics_by_model(Comment, method, comments[len(comments) - 1].time,
                                                                   to_date)

                    for post in update_posts:
                        self.update_statistics_model(statistics_model, post, 'post')
                    for comment in update_comments:
                        self.update_statistics_model(statistics_model, comment, 'comment')

                GroupStatisticsUpdateList.update(group=self.get_object(), method=method)

            posts, comments = self.process_statistics_model(method, posts, comments)

        return posts, comments

    def get_statistics(self, method, from_date, to_date):
        """
        Get statistics

        :param method: method
        :param from_date: from_date
        :param to_date: to_date
        :return: posts and comments
        """
        posts = self.get_statistics_by_model(Post, method, from_date, to_date)
        comments = self.get_statistics_by_model(Comment, method, from_date, to_date)
        return posts, comments

    def get_statistics_by_model(self, model, method, from_date, to_date):
        """
        Get statistics by model

        :param model: model
        :param method: method
        :param from_date: from_date
        :param to_date: to_date
        :return: models
        """
        _models = self.get_objects_by_time(model, from_date, to_date)

        # Method Dictionary for group by time
        dic = {
            'year': "date_trunc('year', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'month': "date_trunc('month', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'day': "date_trunc('day', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'hour': "date_trunc('hour', created_time at time zone 'UTC' AT TIME ZONE '+9')",
            'hour_total': "date_part('hour', created_time at time zone 'UTC' AT TIME ZONE '+9')",
        }

        # Get models count in some date
        return _models.extra(select={'date': dic[method]}).order_by().values('date') \
            .annotate(count=Count('created_time'))

    def process_statistics(self, method, posts, comments):
        """
        Process statistics for chart

        :param method: method
        :param posts: post
        :param comments: comment
        :return: sorted processed posts and comments
        """
        processed_posts = []
        processed_comments = []

        for post in posts:
            if method == "hour_total":
                date = '{0:0.0f}'.format(post.get('date')).zfill(2)
            else:
                date = post.get("date").strftime("%Y-%m-%d %I:%M%p")
            count = post.get("count")
            processed_posts.append([date, count])

        for comment in comments:
            if method == "hour_total":
                date = '{0:0.0f}'.format(comment.get('date')).zfill(2)
            else:
                date = comment.get("date").strftime("%Y-%m-%d %I:%M%p")
            count = comment.get("count")
            processed_comments.append([date, count])

        return sorted(processed_posts, key=lambda k: k[0]), sorted(processed_comments, key=lambda k: k[0])

    def process_statistics_model(self, method, posts, comments):
        """
        Process statistics by model for chart

        :param method: method
        :param posts: post
        :param comments: comment
        :return: sorted processed posts and comments
        """
        processed_posts = []
        processed_comments = []

        for post in posts:
            if method == "hour_total":
                date = '{0:0.0f}'.format(post.time).zfill(2)
            else:
                date = post.time.strftime("%Y-%m-%d %I:%M%p")
            count = post.count
            processed_posts.append([date, count])

        for comment in comments:
            if method == "hour_total":
                date = '{0:0.0f}'.format(comment.time).zfill(2)
            else:
                date = comment.time.strftime("%Y-%m-%d %I:%M%p")
            count = comment.count
            processed_comments.append([date, count])

        return sorted(processed_posts, key=lambda k: k[0]), sorted(processed_comments, key=lambda k: k[0])

    def save_statistics_model(self, statistics_model, model, model_string):
        """
        Save statistics model

        :param statistics_model: statistics_model
        :param model: model
        :param model_string: model_string
        """
        statistics_model(group=self.get_object(), time=model.get("date"), model=model_string,
                         count=model.get("count")).save()

    def update_statistics_model(self, statistics_model, model, model_string):
        """
        Update statistics model

        :param statistics_model: statistics_model
        :param model: model
        :param model_string: model_string
        """
        old_model = statistics_model.objects.filter(group=self.get_object(), model=model_string, time=model.get("date"))

        if old_model:
            old_model[0].count = model.get("count")
            old_model[0].save()
        else:
            self.save_statistics_model(statistics_model, model, model_string)

    @detail_route()
    def post_issue(self, request, pk=None):
        """
        Return Hot Comment Issue for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        posts = self.get_issue(Post)
        return self.response_models(posts, request, PostIssueSerializer)

    @detail_route()
    def comment_issue(self, request, pk=None):
        """
        Return Hot Comment Issue for group

        :param request: request
        :param pk: pk
        :return: response model
        """
        comments = self.get_issue(Comment)
        return self.response_models(comments, request, CommentIssueSerializer)

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
        ratio = self.request.query_params.get('ratio', None)

        select_query = 'like_count + comment_count'
        if ratio:
            select_query = 'like_count * {} + comment_count * {}'.format(float(ratio), 1.0 - float(ratio))

        # If from_date and to_date aren't exist, it has seven days range from seven days ago to today.
        if from_date:
            from_date = date_utils.get_date_from_str(from_date)
        if to_date:
            to_date = date_utils.get_date_from_str(to_date)

        if not from_date and not to_date:
            from_date, to_date = date_utils.week_delta()

        if from_date and from_date > (timezone.now() - timezone.timedelta(30)).date():
            if model == Post:
                model = MonthPost
            else:
                model = MonthComment

        _models = self.get_objects_by_time(model, from_date, to_date)

        if model == MonthPost:
            _models = _models.exclude(post__is_show=False)
            return Post.objects.filter(pk__in=_models.values_list('post', flat=True)) \
                .extra(select={'score': select_query}, order_by=('-score',))
        elif model == MonthComment:
            _models = _models.exclude(comment__is_show=False)
            return Comment.objects.filter(pk__in=_models.values_list('comment', flat=True)) \
                .extra(select={'score': select_query}, order_by=('-score',))
        else:
            _models = _models.extra(select={'score': select_query}, order_by=('-score',))
            return _models.exclude(is_show=False)

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

    def get_archive(self, model):
        """
        Get archive models from group.

        from_date : day to find archives from HTTP Request

        :param model: model to get archive
        :return: result models
        """
        from_date = self.request.query_params.get('from', None)
        to_date = None
        user_id = self.request.query_params.get('user_id', None)

        if from_date:
            from_date = date_utils.get_date_from_str(from_date)
            to_date = from_date
        else:
            from_date = date_utils.get_today().date()
            to_date = from_date

        if from_date and from_date > (timezone.now() - timezone.timedelta(30)).date():
            if model == Post:
                model = MonthPost
            else:
                model = MonthComment

        _models = self.get_objects_by_time(model, from_date, to_date)

        if model == MonthPost:
            _models = Post.objects.filter(pk__in=_models.values_list('post', flat=True))
        elif model == MonthComment:
            _models = Comment.objects.filter(pk__in=_models.values_list('comment', flat=True))

        if user_id:
            _user = get_object_or_404(FBUser, id=user_id)
            return _models.filter(user=_user).order_by('-created_time')
        else:
            return _models.order_by('-created_time')

    @detail_route()
    def activity(self, request, pk=None):
        """
        Return User for group activity
        :param request: request
        :param pk: pk
        :return: response model
        """
        _group = self.get_object()
        model = self.request.query_params.get('model', None)

        if model != 'post' and model != 'comment':
            raise ValueError("Model can be used 'post' or 'comment'. Input model:" + model)

        if model == 'post':
            user_activities = UserActivity.objects.filter(group=_group).order_by('-post_count')
        else:
            user_activities = UserActivity.objects.filter(group=_group).order_by('-comment_count')

        return self.response_models(user_activities, request, UserActivitySerializer)

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
        cursor.execute("SELECT count(*) FROM archive_fbuser_groups WHERE group_id = %s", [_group.id])
        user_count = cursor.fetchall()[0][0]

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

        return Response({'posts': [[key, posts[key]] for key in posts.keys()],
                         'comments': [[key, comments[key]] for key in comments.keys()]})

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
        user_id = self.request.query_params.get('user_id', '')

        if search:
            _users = FBUser.objects.search(search)
            user_activities = UserActivity.objects.filter(group=_group, user__in=_users).order_by('user__name')
        elif user_id:
            _user = FBUser.objects.get(id=user_id)
            user_activities = UserActivity.objects.filter(group=_group, user=_user).order_by('user__name')
        else:
            user_activities = UserActivity.objects.filter(group=_group).order_by('user__name')

        return self.response_models(user_activities, request, UserActivitySerializer)

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

    @list_route()
    def group_search(self, request):
        """
        Return group search

        :param request: request
        :return: response model
        """
        order = self.get_order()
        _groups = self.get_queryset().exclude(privacy='CLOSED').order_by(order)
        search = self.request.query_params.get('q', '')
        if search:
            return self.response_models(_groups.search(search), request, GroupSerializer)
        else:
            return self.response_models(_groups, request, GroupSerializer)

    @list_route()
    def interest_group(self, request):
        """
        Return interest group

        :param request: request
        :return: response model
        """
        order = self.get_order()
        user_id = self.request.query_params.get('user_id', None)
        _user = get_object_or_404(User, id=user_id)

        _groups = InterestGroupList.objects.filter(user=_user).values_list('group')
        _groups = self.get_queryset().filter(id__in=_groups).exclude(privacy='CLOSED').order_by(order)
        search = self.request.query_params.get('q', '')
        if search:
            return self.response_models(_groups.search(search), request, GroupSerializer)
        else:
            return self.response_models(_groups, request, GroupSerializer)

    def get_order(self):
        """
        Return order

        :return: order
        """
        order_column = self.request.query_params.get('order_column', 'updated_time')
        order_keyword = self.request.query_params.get('order_keyword', 'desc')

        if order_column != 'name' and order_column != 'updated_time' \
                and order_column != 'post_count' and order_column != 'comment_count':
            raise ValueError(
                    "order_column can be used 'name', 'updated_time', 'post_count'or 'comment_count'. Input order_column:"
                    + order_column)

        if order_keyword != 'desc' and order_keyword != 'asc':
            raise ValueError(
                    "order_keyword can be used 'desc', 'asc'. Input order_keyword:" + order_keyword)

        if order_keyword == 'desc':
            order_keyword = '-'
        else:
            order_keyword = ''

        return order_keyword + order_column

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


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Post View Set for django restful framework
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Comment View Set for django restful framework
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class MediaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Media View Set for django restful framework
    """
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


class AttachmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Attachment View Set for django restful framework
    """
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class BlacklistViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Blacklist View Set for django restful framework
    """
    queryset = Blacklist.objects.all()
    serializer_class = BlacklistSerializer


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Report View Set for django restful framework
    """
    queryset = Report.objects.all().exclude(status='checked').order_by('-updated_time')
    serializer_class = ReportSerializer


class WardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Ward View Set for django restful framework
    """
    queryset = Ward.objects.all().order_by('-created_time')
    serializer_class = WardSerializer

    @list_route()
    def ward_alert(self, request):
        user_id = self.request.query_params.get('user_id', None)
        _user = get_object_or_404(User, pk=user_id)

        _wards = Ward.objects.all().filter(user=_user).filter(Q(updated_time__lte=F('post__updated_time'))) \
            .order_by('-post__updated_time')
        page = self.paginate_queryset(_wards)
        if page is not None:
            serializers = WardSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializers.data)

        serializers = WardSerializer(_wards, many=True, context={'request': request})
        return Response(serializers.data)


class UserActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Ward View Set for django restful framework
    """
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer


# Error page
def handler404(request):
    """
    Return 404 error response

    :param request: request
    :return:
    """
    response = render_to_response('errors/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    """
    Return 500 error response

    :param request: request
    :return:
    """
    response = render_to_response('errors/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
