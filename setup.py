import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


install_requires = [
    'Django==1.7',
    'django-debug-toolbar==1.2',
    'sqlparse==0.1.11',
    'django-crispy-forms==1.4.0',
    'django-guardian==1.2.0',
    'six==1.6.1',
    'django-allauth==0.16.1',
    'oauthlib==0.6.1',
    'python3-openid==3.0.4',
    'requests==2.3.0',
    'requests-oauthlib==0.4.0',
    'django-filter==0.7',
    'djangorestframework==2.3.14',
    'logan',
]

tests_require = [
    'pytest',
    'pytest-django',
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='wight-invoice',
    version='0.2.0',
    packages=find_packages('.'),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
    },
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'wightinvoices = wightinvoices.runner:main',
        ],
    },
)
