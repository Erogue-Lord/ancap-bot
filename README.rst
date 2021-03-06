Ancap Bot
=========

.. code-block::

       ___                      ___       __
      / _ | ___  _______ ____  / _ )___  / /_
     / __ |/ _ \/ __/ _ `/ _ \/ _  / _ \/ __/
    /_/ |_/_//_/\__/\_,_/ .__/____/\___/\__/
                       /_/

.. image:: https://img.shields.io/github/license/Erogue-Lord/ancap-bot
        :target: https://choosealicense.com/licenses/mit/
        :alt: License

A multi language discord bot that simulates an fictional Anarcho-capitalist economy, it's developed for an social experiment.

it is capable os simulating an fictional economy and leting users by and control their own channels

Installation
------------

Requirements
^^^^^^^^^^^^

* Runtime and Installation
    * Python >= 3.8
    * pip (Installation)
    * setuptools (Building)
    * discord.py and SQLAlchemy
    * database connector `suported dbs`_
    * Database (Tested with Postgresql and sqlite3, may work with any db supported by SQLAlchemy)
* Development
    * Black (style)
    * Flake8 (linter)
    * GNU Gettext (translation)
    * POSIX Make (optional)
    * wheel (optional)

Setting Up
^^^^^^^^^^

Create an ``.env`` file or set the enviroment table with the folowing variables

* TOKEN: the token of the discord bot (required)
* DATABASE_URL: The uri of the database ``dialect://username:password@host:port/database`` (default: sqlite://\:memory\:)
* WAGE: the default wage for the ``work`` command (default: 25.00)
* CHANNEL_PRICE: the price to buy a text channel (default: 100.00)
* COOLDOWN: the time in seconds to use the ``work`` command (default: 60)
* CHANNEL_CATEGORY: the category where the channels will be created (default: Text Channels)
* PREFIX: the command prefix (default: $)
* LOCALE: the language of the instance (default: en)
* LOGLEVEL: the level for the logging (default: INFO)
* LOGFILE: the file which the logs will be writen (default: stdout)
* ROLE: the role to give to the registered members (default: ancap)

create a virtual enviroment

.. code-block:: shell

    python -m venv env

Then install the bot

.. code-block:: shell

    pip install -e .

Options:

* [postgres] for Postgresql supported
* [mysql] for Mysql supported
* [dotenv] for .env file support

or install the connector manualy

create the Database tables with (isn't needed with in memory db)

.. code-block:: shell

    ancap-bot updatedb

then run

.. code-block:: shell

    ancap-bot run

if you see the message

.. code-block::

    We have logged in as <your bot name>

congrats, you have succefuly installed the bot.

Contribuing
-----------

Translation
^^^^^^^^^^^

If you want to contribuite to tanslating te bot you will need GNU Gettext and Make

Use

.. code-block:: shell

    make ancap_bot.pot

to create the empty message catalog

translate then put the po file in ``locale/<LENGUAGE>/LC_MESSAGES/ancap_bot.po``

to compile all translations use

.. code-block:: shell

    make i18n

to delete all compiled translations

.. code-block:: shell

    make clean-mo

License
-------

Released under the `MIT/Expat license <https://choosealicense.com/licenses/mit/>`_.

.. _suported dbs: https://tortoise-orm.readthedocs.io/en/latest/databases.html
