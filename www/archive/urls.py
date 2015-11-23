from django.conf.urls import url

from . import views

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


urlpatterns = [
    url(r'^groups/$', views.groups, name='groups'),

    url(r'^group/(?P<group_id>[0-9]+)/$', views.group_analysis, name='group'),
    url(r'^group/(?P<group_id>[0-9]+)/analysis/$', views.group_analysis, name='group_analysis'),
    url(r'^group/(?P<group_id>[0-9]+)/user/$', views.group_user, name='group_user'),
    url(r'^group/(?P<group_id>[0-9]+)/search/$', views.group_search, name='group_search'),
    url(r'^group/(?P<group_id>[0-9]+)/management/$', views.group_management, name='group_management'),
    url(r'^group/(?P<group_id>[0-9]+)/store/$', views.group_store, name='group_store'),
    url(r'^group/(?P<group_id>[0-9]+)/update/$', views.group_update, name='group_update'),

    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
]
