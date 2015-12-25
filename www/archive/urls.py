from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"

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
