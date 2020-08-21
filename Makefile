.PHONY: clean-pyc clean-build clean i18n install

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr src/*.egg-info

clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
