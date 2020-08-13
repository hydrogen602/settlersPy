
.PHONY: docs remove-docs help all-docs check

help:
	@echo docs check

docs: remove-docs all-docs

#all-docs:
#	cd ..; pdoc3 --html -o settlersPy/docs settlersPy

all-docs:
	pdoc3 --html -o docs/ gameServer

remove-docs:
	rm -rf docs

check:
	mypy gameServer --warn-unused-ignores