#!/usr/bin/env python

from setuptools import setup
from setuptools.command.install import install


class CompileCatalog(install):
    def run(self):
        from babel.messages.frontend import compile_catalog
        compiler = compile_catalog(self.distribution)
        compiler.domain = ["ancap_bot"]
        compiler.directory = "ancap_bot/locale"
        compiler.run()
        super().run()


with open("requirements.txt") as f:
    requirements = f.readlines()

with open("requirements-dev.txt") as f:
    requirements_dev = f.readlines()

# metadata in setup.cfg

setup(
    name="ancap_bot",
    install_requires=requirements,
    extras_require={
        "dev": requirements_dev,
        "postgres": "psycopg2",
        "dotenv": "python-dotenv",
    },
    cmdclass={"install": CompileCatalog},
    setup_requires=["Babel", "pytz"],
)
