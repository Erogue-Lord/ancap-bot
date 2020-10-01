#!/usr/bin/env python

import re

from setuptools import setup, find_packages

with open("ancap_bot/__init__.py") as f:
    version = re.search('__version__ = "(.*?)"', f.read()).group(1)

with open("README.rst") as f:
    long_description = f.read()

setup(
    name="ancap_bot",
    description="A Discord bot that simulates an ancap economy",
    author="Erogue Lord",
    author_email="debz1@protonmail.com",
    license="MIT",
    version=version,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Erogue-Lord/ancap-bot",
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": ["ancap-bot = ancap_bot.__main__:main_cli",]  # noqa: E231
    },
    package_data={
        "ancap_bot": ["locale/*/LC_MESSAGES/ancap_bot.mo", "py.typed"],
    },  # noqa: E231
    zip_safe=False,
    install_requires=["discord.py", "SQLAlchemy"],
    extras_require={
        "dev": ["flake8", "black"],
        "postgres": "psycopg2",
        "dotenv": "python-dotenv",
    },
)
