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
        ROOT_URLCONF='wightinvoices.urls',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'wightinvoices.invoice',

            'crispy_forms',
            'guardian',
        ),
        AUTHENTICATION_BACKENDS=(
            'django.contrib.auth.backends.ModelBackend', # this is default
            'guardian.backends.ObjectPermissionBackend',
        ),
        ANONYMOUS_USER_ID=None,
    )

    import django
    django.setup()
