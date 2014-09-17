from logan.runner import run_app, configure_app

import os
import base64


KEY_LENGTH = 40


CONFIG_TEMPLATE = """
# This file is just Python, with a touch of Django which means you
# you can inherit and tweak settings to your hearts content.
from wightinvoices.settings import *

import os.path

CONF_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        # You can swap out the engine for MySQL easily by changing this value
        # to ``django.db.backends.mysql`` or to PostgreSQL with
        # ``django.db.backends.postgresql_psycopg2``

        # If you change this, you'll also need to install the appropriate python
        # package: psycopg2 (Postgres) or mysql-python
        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': os.path.join(CONF_ROOT, 'wight_invoices.db'),
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',

        # If you're using Postgres, we recommend turning on autocommit
        # 'OPTIONS': {
        #     'autocommit': True,
        # }
    }
}


################
## Web Server ##
################

# You MUST configure the absolute URI root for Sentry:
INVOICE_URL_PREFIX = 'http://invoice.example.com'  # No trailing slash!

# If you're using a reverse proxy, you should enable the X-Forwarded-Proto
# and X-Forwarded-Host headers, and uncomment the following settings
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# USE_X_FORWARDED_HOST = True

INVOICE_WEB_HOST = '0.0.0.0'
INVOICE_WEB_PORT = 9000
INVOICE_WEB_OPTIONS = {
    'workers': 3,  # the number of gunicorn workers
    'limit_request_line': 0,  # required for raven-js
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}


###########
## etc. ##
###########

# If this file ever becomes compromised, it's important to regenerate your SECRET_KEY
# Changing this value will result in all current sessions being invalidated
SECRET_KEY = %(default_key)r
"""

def generate_settings():
    """
    This command is run when ``default_path`` doesn't exist, or ``init`` is
    run and returns a string representing the default data to put into their
    settings file.
    """
    output = CONFIG_TEMPLATE % dict(
        default_key=base64.b64encode(os.urandom(KEY_LENGTH)),
    )

    return output


def initialize_app(config):
    settings = config['settings']

    if settings.INVOICE_URL_PREFIX in ('', 'http://invoice.example.com'):
        # Maybe also point to a piece of documentation for more information?
        # This directly coincides with users getting the awkward
        # `ALLOWED_HOSTS` exception.
        print('')
        print('\033[91m!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        print('\033[91m!! INVOICE_URL_PREFIX is not configured !!\033[0m')
        print('\033[91m!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\033[0m')
        print('')
        # Set `ALLOWED_HOSTS` to the catch-all so it works
        settings.ALLOWED_HOSTS = ['*']

    # Set ALLOWED_HOSTS if it's not already available
    if not settings.ALLOWED_HOSTS:
        from urlparse import urlparse
        urlbits = urlparse(settings.INVOICE_URL_PREFIX)
        if urlbits.hostname:
            settings.ALLOWED_HOSTS = (urlbits.hostname,)


def configure(config_path=None):
    configure_app(
        project='wightinvoices',
        config_path=config_path,
        default_config_path='~/.wightinvoices/wightinvoices.conf.py',
        default_settings='wightinvoices.settings',
        settings_initializer=generate_settings,
        settings_envvar='INVOICE_CONF',
        initializer=initialize_app,
    )


def main():
    run_app(
        project='wightinvoices',
        default_config_path='~/.wightinvoices/wightinvoices.conf.py',
        default_settings='wightinvoices.settings',
        settings_initializer=generate_settings,
        settings_envvar='INVOICE_CONF',
        initializer=initialize_app,
    )

if __name__ == '__main__':
    main()