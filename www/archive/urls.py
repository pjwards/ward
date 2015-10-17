from django.conf.urls import url

from . import views

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


urlpatterns = [
    url(r'^groups/$', views.groups, name='groups'),
    url(r'^groups/(?P<group_id>[0-9]+)/store/$', views.group_store, name='group_store'),
    url(r'^groups/(?P<group_id>[0-9]+)/update/$', views.group_update, name='group_update'),
]
