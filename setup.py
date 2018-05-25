#!/usr/bin/env python

from setuptools import setup

setup(
    name="statusbot",
    version="0.1.0",
    description="Status Bot",
    author="Mike Fiedler",
    author_email="miketheman@gmail.com",
    license="MIT",
    url="https://www.miketheman.net/",
    packages=["statusbot"],
    install_requires=["python-dateutil", "requests", "tldextract"],
)
