
.PHONY: tools-docs remove-docs docs

docs: remove-docs tools-docs mechanics-docs

tools-docs:
	pdoc3 --html -o docs tools

mechanics-docs:
	pdoc3 --html -o docs mechanics


remove-docs:
	rm -rf docs