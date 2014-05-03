def pytest_configure():
    from django.conf import settings

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        SECRET_KEY='not very secret in tests',
        # USE_I18N=True,
        # USE_L10N=True,
        # STATIC_URL='/static/',
        # ROOT_URLCONF='tests.urls',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'wightinvoices',
            'wightinvoices.invoice',
        ),
    )