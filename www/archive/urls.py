from django.conf.urls import url

from . import views

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


urlpatterns = [
    url(r'^groups/$', views.groups, name='groups'),

    url(r'^group/(?P<group_id>[0-9]+)/$', views.group, name='group'),
    url(r'^group/(?P<group_id>[0-9]+)/store/$', views.group_store, name='group_store'),
    url(r'^group/(?P<group_id>[0-9]+)/update/$', views.group_update, name='group_update'),
    url(r'^group/(?P<group_id>[0-9]+)/issue/$', views.group_issue, name='group_issue'),
    url(r'^group/(?P<group_id>[0-9]+)/statistics/$', views.group_statistics, name='group_statistics'),
]
