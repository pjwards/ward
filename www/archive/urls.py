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
""" Sets urls """

from django.conf.urls import url
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^groups/admin/$', views.groups_admin, name='groups_admin'),

    url(r'^group/(?P<group_id>[0-9]+)/$', RedirectView.as_view(pattern_name='archive:group_analysis', permanent=False),
        name='group'),
    url(r'^group/(?P<group_id>[0-9]+)/analysis/$', views.group_analysis, name='group_analysis'),
    url(r'^group/(?P<group_id>[0-9]+)/user/$', views.group_user, name='group_user'),
    url(r'^group/(?P<group_id>[0-9]+)/search/$', views.group_search, name='group_search'),
    url(r'^group/(?P<group_id>[0-9]+)/management/$', views.group_management, name='group_management'),
    url(r'^group/(?P<group_id>[0-9]+)/store/$', views.group_store, name='group_store'),
    url(r'^group/(?P<group_id>[0-9]+)/update/$', views.group_update, name='group_update'),
    url(r'^group/(?P<group_id>[0-9]+)/check/$', views.group_check, name='group_check'),
    url(r'^group/(?P<group_id>[0-9]+)/comments_check/$', views.group_comments_check, name='group_comments_check'),

    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),

    url(r'^report/(?P<object_id>[0-9_]+)/$', views.report, name='report'),
    url(r'^report/(?P<report_id>[0-9_]+)/(?P<action>[a-z]+)/$', views.report_action, name='report_action'),
    url(r'^reports/$', views.reports, name='reports'),

    url(r'^ward/(?P<object_id>[0-9_]+)/$', views.ward, name='ward'),
    url(r'^ward/(?P<ward_id>[0-9_]+)/update/$', views.ward_update, name='ward_update'),
    url(r'^wards/$', views.wards, name='wards'),
]
