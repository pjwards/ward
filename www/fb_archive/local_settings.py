# This file is exec'd from settings.py, so it has access to and can
# modify all the variables in settings.py.

# If this file is changed in development, the development server will
# have to be manually restarted because changes will not be noticed
# immediately.

DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = "0*pab#&%9##an(w9fk$b&uhn#yvv6b+(0nl(f^f6(-ec%5v)!k"
NEVERCACHE_KEY = "^)h*m1byrat2%jcaool9n@fc%=%%#97k0$qrh7yn2p^g-qw)ku"

DATABASES = {
    "default": {
        # Ends with "postgresql_psycopg2", "mysql", "sqlite3" or "oracle".
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        # DB name or path to database file if using sqlite3.
        "NAME": "ward",
        # Not used with sqlite3.
        "USER": "donghyun",
        # Not used with sqlite3.
        "PASSWORD": "",
        # Set to empty string for localhost. Not used with sqlite3.
        "HOST": "localhost",
        # Set to empty string for default. Not used with sqlite3.
        "PORT": "5432",
    }
}

###################
# DEPLOY SETTINGS #
###################

# Domains for public site
# ALLOWED_HOSTS = [""]

# These settings are used by the default fabfile.py provided.
# Check fabfile.py for defaults.

# FABRIC = {
#     "DEPLOY_TOOL": "rsync",  # Deploy with "git", "hg", or "rsync"
#     "SSH_USER": "",  # VPS SSH username
#     "HOSTS": [""],  # The IP address of your VPS
#     "DOMAINS": ALLOWED_HOSTS,  # Edit domains in ALLOWED_HOSTS
#     "REQUIREMENTS_PATH": "requirements.txt",  # Project's pip requirements
#     "LOCALE": "en_US.UTF-8",  # Should end with ".UTF-8"
#     "DB_PASS": "",  # Live database password
#     "ADMIN_PASS": "",  # Live admin user password
#     "SECRET_KEY": SECRET_KEY,
#     "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }


####################
# FACEBOOK SETTING #
####################

# Facebook Graph API
FB_APP_ID = '1621617961401149'
FB_APP_SECRET = 'bdc8380f61ba92b08e2d03bf9993303f'

SOCIAL_AUTH_FACEBOOK_KEY = FB_APP_ID
SOCIAL_AUTH_FACEBOOK_SECRET = FB_APP_SECRET


###################
# CELERY SETTINGS #
###################

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
# BROKER_URL = 'ec2-52-192-224-80.ap-northeast-1.compute.amazonaws.com'
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'db+sqlite:///results.db'
