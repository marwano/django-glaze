
from setuptools import setup
import re

readme = open('README.rst').read()
changes = open('CHANGES.txt').read()
version_file = 'glaze/__init__.py'
version = re.findall("__version__ = '(.*)'", open(version_file).read())[0]
try:
    version = __import__('utile').git_version(version)
except ImportError:
    pass

setup(
    name='django-glaze',
    version=version,
    description="Adding extra functionality to Django",
    long_description=readme + '\n\n' + changes,
    author='Marwan Alsabbagh',
    author_email='marwan.alsabbagh@gmail.com',
    url='https://github.com/marwano/django-glaze',
    license='BSD',
    packages=['glaze', 'glaze.utils'],
    include_package_data=True,
    install_requires=[
        'utile>=0.3'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
