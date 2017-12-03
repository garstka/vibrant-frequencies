#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'sounddevice>=0.3.9',
    'pyaudio>=0.2.11',
    'pygame>=1.9.3',
    'numpy>=1.13.3'
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(garstka): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='vibrant_frequencies',
    version='0.1.0',
    description="Real-time sound visualization in Python.",
    long_description=readme + '\n\n' + history,
    author="Matt Garstka",
    author_email='matt.garstka@gmail.com',
    url='https://github.com/garstka/vibrant_frequencies',
    packages=find_packages(include=['vibrant_frequencies']),
    entry_points={
        'console_scripts': [
            'vf=vibrant_frequencies.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='vibrant_frequencies',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
