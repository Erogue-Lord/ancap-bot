#!/usr/bin/env python

import re

from setuptools import setup, find_packages
from setuptools.command import build_py, install

# This is a hack for getting setuptools to compile .po files with Babel on build


class CompileCatalog:
    def run(self):
        from babel.messages.frontend import compile_catalog

        compiler = compile_catalog(self.distribution)
        compiler.domain = ["ancap_bot"]
        compiler.directory = "ancap_bot/locale"
        compiler.run()
        super().run()


class CompileCatalogBuild(CompileCatalog, build_py.build_py):
    pass


class CompileCatalogInstall(CompileCatalog, install.install):
    pass


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
    cmdclass={
        "build_py": CompileCatalogBuild,
        "install": CompileCatalogInstall,
    },  # noqa: E231
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
    setup_requires=["Babel"],
    classifiers=[
        "Environment :: Web Environment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
    ],
)
