
.PHONY: tools-docs remove-tools-docs

tools-docs: remove-tools-docs
	pdoc3 --html -o docs tools

remove-tools-docs:
	rm -rf docs/tools