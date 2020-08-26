#!/usr/bin/env python

from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.readlines()

with open("requirements-dev.txt") as f:
    requirements_dev = f.readlines()

# metadata is in setup.cfg

setup(
    name="ancap_bot",
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
        "postgres": "psycopg2",
        "dotenv": "python-dotenv",
    },
)
