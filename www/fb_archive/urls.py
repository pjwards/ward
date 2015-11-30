from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from mezzanine.conf import settings
from registration.backends.hmac.views import ActivationView, RegistrationView
from rest_framework import routers
from archive import views


admin.autodiscover()

urlpatterns = [
    url(r'^$', views.groups, name="home"),
    url(r'^about/$', views.about, name='about'),
    url(r"^admin/", include(admin.site.urls)),

    url(r'^', include('registration.auth_urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^archive/', include('archive.urls', namespace="archive")),
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
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'medium', views.MediaViewSet)
router.register(r'attachments', views.AttachmentViewSet)
router.register(r'blacklists', views.BlacklistViewSet)
router.register(r'reports', views.ReportViewSet)
router.register(r'wards', views.WardViewSet)

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
