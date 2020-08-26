#!/usr/bin/env python

import re

from setuptools import setup, find_packages

with open("ancap_bot/__init__.py") as f:
    version = re.search('__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="ancap_bot",
    description="An discord bot that simulates an ancap economy",
    author="Erogue Lord",
    author_email="debz1@protonmail.com",
    license="MIT",
    version=version,
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    license_file="LICENSE",
    url="https://github.com/Erogue-Lord/ancap-bot",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["ancap-bot = ancap_bot.__main__:main_cli",]  # noqa: E231
    },
    package_data={"ancap_bot": ["locale/*/LC_MESSAGES/ancap_bot.mo"],},  # noqa: E231
    zip_safe=False,
    install_requires=open("requirements.txt").readlines(),
    extras_require={
        "dev": open("requirements-dev.txt").readlines(),
        "postgres": "psycopg2",
        "dotenv": "python-dotenv",
    },
)
