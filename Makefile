.PHONY: clean-pyc clean-build clean-mo clean i18n install

help:
	@echo clean:
	@echo 	delete all compiled or chached files
	@echo clean-build:
	@echo 	delete folders and files resulting from the build
	@echo clean-pyc:
	@echo 	delete all .pyc files and __pycache__ folders
	@echo clean-mo:
	@echo 	delete all .mo files
	@echo i18n:
	@echo 	compile all .po files to .mo
	@echo messages.pot:
	@echo 	generate an empty message catalog for translation

clean: clean-build clean-pyc clean-mo

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr src/*.egg-info

clean-pyc:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean-mo:
	find . -type f -name '*.mo' -delete

i18n: $(PO_FILES:po=mo)

%.mo: %.po
	msgfmt $< -o $@

messages.pot:
	find . -iname "*.py" | xargs xgettext --from-code utf-8 -o messages.pot