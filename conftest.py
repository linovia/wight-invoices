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
        STATIC_URL='/static/',
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
            'allauth',
            'allauth.account',
        ),
        AUTHENTICATION_BACKENDS=(
            'django.contrib.auth.backends.ModelBackend', # this is default
            'guardian.backends.ObjectPermissionBackend',
        ),
        ANONYMOUS_USER_ID=None,
        CRISPY_TEMPLATE_PACK='bootstrap3',
        PASSWORD_HASHERS = (
            'tests.custom_password_hashers.ClearPasswordHasher',
        ),
        TEMPLATE_CONTEXT_PROCESSORS = (
            'django.contrib.auth.context_processors.auth',
            'django.core.context_processors.debug',
            'django.core.context_processors.i18n',
            'django.core.context_processors.media',
            'django.core.context_processors.static',
            'django.core.context_processors.tz',
            'django.core.context_processors.request',
            'django.contrib.messages.context_processors.messages'
        ),
    )

    import django
    django.setup()
