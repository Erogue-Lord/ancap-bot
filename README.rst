=========
Ancap Bot
=========

An discord bot that simulates an fictional Anarcho-capitalist economy, it's developed for an social experiment.

Installation
------------

Requirements
^^^^^^^^^^^^

* Runtime and Installation
    * Python >= 3.6
    * pip
    * setuptools
    * all modules in ``requirements.txt``
    * database connector, psycopg2 is recomended for Postgres, `suported db's <https://docs.sqlalchemy.org/en/13/dialects/>`_
    * Database (Tested with Postgresql and sqlite3, may work with any db supported by SQLAlchemy)
    * Python venv (optional)
    * Make (optional)
* Development
    * black (style)
    * flake8 (linter)
    * GNU Gettext (translation)

setting up
^^^^^^^^^^

create an ``.env`` file or set the enviroment table with the folowing variables

* TOKEN: the token of the discord bot (required)
* DB: The uri of the database ``dialect+driver://username:password@host:port/database``, `more info`_ (if not defined a ``db.sqlite`` will be created at the root of the project)
* WAGE: the default wage for the ``work`` command (default: 25.00)
* CHANNEL_PRICE: the price to buy a text channel (default: 100.00)
* COOLDOWN: the time in seconds to use the ``work`` command (default: 60)
* CHANNEL_CATEGORY: the category where the channels will be created (default: Text Channels)
* PREFIX: the command prefix (default: $)
* LOCALE: the lenguage of the instance (default: en)

Then install with ::

    pip install -e .

Or to install with psycopg2 ::

    pip install -e .[postgres]

orinstall the connector manualy

create the Database tables with ::

    ancap-bot updatedb

Then run ::

    ancap-bot run

if you see the message ::

    We have logged in as <your bot name>

congrats, you have succefuly installed the bot.

License
-------

Released under the `MIT <https://choosealicense.com/licenses/mit/>`_ license.

.. _more info:  https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls
