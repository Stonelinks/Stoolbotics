.PHONY: docs

FILES = $(shell ls *.md | cut -d '.' -f1)

docs:
	rm -rf README.html
	cat static/header.html > README.html
	markdown -x toc README.md >> README.html 
	cat static/footer.html >> README.html
