PYTHON ?= python
XGETTEXT ?= xgettext
MSGFMT ?= msgfmt

.PHONY: clean-pyc clean-build clean-mo clean i18n install dist help

.DEFAULT: help

help:
	@echo "clean"
	@echo "	delete all compiled or chached files"
	@echo "clean-build"
	@echo "	delete folders and files resulting from the build"
	@echo "clean-pyc"
	@echo "	delete all .pyc files and __pycache__ folders"
	@echo "clean-mo"
	@echo "	delete all .mo files"
	@echo "i18n"
	@echo "	compile all .po files to .mo"
	@echo "ancap_bot.pot"
	@echo "	generate an empty message catalog for translation"
	@echo "install"
	@ehco "	install the module"
	@echo "dist"
	@echo "	prepare the module for distribution"

install:
	pip install -U .

clean: clean-build clean-pyc clean-mo

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean-mo:
	find . -type f -name '*.mo' -delete

i18n: $(PO_FILES:po=mo)

%.mo: %.po
	$(MSGFMT) $< -o $@

ancap_bot.pot:
	find . -iname "*.py" | xargs $(XGETTEXT) -o messages.pot

dist: i18n
	$(PYTHON) setup.py bdist_wheel sdist