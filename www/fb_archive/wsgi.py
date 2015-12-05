"""
WSGI config for fb_archive project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
import site

import os
import sys


site.addsitedir('/home/ubuntu/.virtualenvs/fb_archive/lib/python3.4/site-packages')

from mezzanine.utils.conf import real_project_name
os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                      "%s.settings" % real_project_name("fb_archive"))

sys.path.insert(0, '/home/ubuntu/workspace/ward')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
