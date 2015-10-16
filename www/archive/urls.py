from django.conf.urls import url

from . import views

__author__ = "Donghyun Seo"
__copyright__ = "Copyright ⓒ 2015, All rights reserved."
__email__ = "egaoneko@naver.com"


urlpatterns = [
    url(r'^(?P<group_id>[0-9]+)/store/$', views.store, name='store'),
    url(r'^groups/$', views.groups, name='groups'),
]
