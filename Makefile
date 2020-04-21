
.PHONY: tools-docs remove-docs docs

docs: remove-docs all-docs

tools-docs:
	pdoc3 --html -o docs tools

mechanics-docs:
	pdoc3 --html -o docs mechanics

all-docs:
	cd ..; pdoc3 --html -o settlersPy/docs settlersPy

remove-docs:
	rm -rf docs