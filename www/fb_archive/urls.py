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

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from mezzanine.conf import settings
from registration.backends.hmac.views import ActivationView, RegistrationView
from rest_framework import routers
from archive import views as archive_views
from analysis import views as analysis_views


admin.autodiscover()

urlpatterns = [
    url(r'^$', archive_views.groups, name="home"),
    url(r'^about/$', archive_views.about, name='about'),
    url(r'^alert/$', archive_views.alert, name='alert'),
    url(r"^admin/", include(admin.site.urls)),

    url(r'^', include('registration.auth_urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^archive/', include('archive.urls', namespace="archive")),
    url(r'^analysis/', include('analysis.urls', namespace="analysis")),
]


#######################
# DJANGO REGISTRATION #
#######################

urlpatterns += [
    url(r'^activate/complete/$',
        TemplateView.as_view(
            template_name='registration/activation_complete.html'
        ),
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>[-:\w]+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
    url(r'^register/$',
        RegistrationView.as_view(),
        name='registration_register'),
    url(r'^register/complete/$',
        TemplateView.as_view(
            template_name='registration/registration_complete.html'
        ),
        name='registration_complete'),
    url(r'^register/closed/$',
        TemplateView.as_view(
            template_name='registration/registration_closed.html'
        ),
        name='registration_disallowed'),
    url(r'^accounts/', include('registration.backends.hmac.urls', namespace="registration")),
    # url(r'^accounts/', include('registration.backends.simple.urls', namespace="registration")),
]

#########################
# DJANGO REST FRAMEWORK #
#########################

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', archive_views.UserViewSet)
router.register(r'groups', archive_views.GroupViewSet)
router.register(r'posts', archive_views.PostViewSet)
router.register(r'comments', archive_views.CommentViewSet)
router.register(r'medium', archive_views.MediaViewSet)
router.register(r'attachments', archive_views.AttachmentViewSet)
router.register(r'blacklists', archive_views.BlacklistViewSet)
router.register(r'reports', archive_views.ReportViewSet)
router.register(r'wards', archive_views.WardViewSet)
router.register(r'user_activities', archive_views.UserActivityViewSet)
router.register(r'spam_list', analysis_views.SpamListViewSet)
router.register(r'spam_word_list', analysis_views.SpamWordListViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


#############
# MEZZANINE #
#############

if settings.USE_MODELTRANSLATION:
    urlpatterns += patterns('',
        url('^i18n/$', 'django.views.i18n.set_language', name='set_language'),
    )

urlpatterns += patterns('',
    ("^", include("mezzanine.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
