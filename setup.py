#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='dockbot',
    version="0.0.1",
    author="Sebastian Vetter",
    author_email="sebastian@roadside-developer.com",
    description="Docker-based CI server",
    long_description='\n\n'.join([
        open('README.rst').read(),
    ]),
    keywords="buildbot, docker, CI",
    license='MIT',
    platforms=['linux'],
    packages=find_packages(
        exclude=["salt*"]
    ),
    include_package_data=True,
    install_requires=[
        'docker-py>=0.2.1',
        'buildbot>=0.8.8',
    ],
    # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    entry_points={
        'console_scripts': ['dockbot = dockbot.cli:main']
    },
)
