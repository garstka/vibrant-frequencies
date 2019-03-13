#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('requirements.txt') as requirements_file:
    REQUIREMENTS = [i for i in requirements_file.readlines() if i]

setup(
    author="Matt Garstka",
    author_email="matt@garstka.net",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Multimedia :: Sound/Audio',
        'Natural Language :: English',
    ],
    description="Real-time sound visualization in Python.",
    entry_points={
        'console_scripts': [
            'vibrant-frequencies=vibrant_frequencies.cli:main'
        ]
    },
    install_requires=REQUIREMENTS,
    long_description=README,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords="real-time sound visualization music",
    license="MIT license",
    name='vibrant_frequencies',
    packages=find_packages(include=['vibrant_frequencies']),
    url='https://github.com/garstka/vibrant_frequencies',
    version='0.1',
    zip_safe=False,
    test_suite='tests'
)
