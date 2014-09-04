import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


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
    install_requires=['logan'],
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
