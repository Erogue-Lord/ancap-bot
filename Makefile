.POSIX:
PYTHON = /usr/bin/env python
PIP = $(PYTHON) -m pip
XGETTEXT = xgettext
MSGFMT = msgfmt
RM = rm -f
PO = ancap_bot/locale/pt_BR/LC_MESSAGES/ancap_bot.po

MO = $(PO:.po=.mo)

TRANSLATED_FILES =\
	ancap_bot/bot.py\
	ancap_bot/__main__.py\
	ancap_bot/cogs/adm.py\
	ancap_bot/cogs/basics.py\
	ancap_bot/cogs/economy.py\
	ancap_bot/cogs/gambling.py\
	ancap_bot/db/db.py

.PHONY: clean-pyc clean-build clean-mo clean i18n install dist test

all: install

install:
	$(PIP) install -U .

clean: clean-build clean-pyc clean-mo

clean-build:
	$(RM) -r build/
	$(RM) -r dist/
	$(RM) -r *.egg-info/
	$(RM) -r .eggs/

clean-pyc:
	find ancap_bot tests \( -type f -name '*.py[co]' -o -type d -name __pycache__ \) -prune -exec $(RM) -r {} \;

clean-mo:
	$(RM) $(MO)
	$(RM) ancap_bot.pot

test:
	$(PYTHON) -m pytest

lint:
	$(PYTHON) -m flake8

i18n: $(MO)

.SUFFIXES: .po .mo
.po.mo:
	$(MSGFMT) $< -o $@

ancap_bot.pot: $(TRANSLATED_FILES)
	$(XGETTEXT) -o ancap_bot.pot $(TRANSLATED_FILES)

dist:
	$(PYTHON) setup.py bdist_wheel sdist
