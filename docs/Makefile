.PHONY: docs compile.github compile.web compile.body

compile.github:
	cat header.md >> README.md
	$(MAKE) compile.body

compile.web:
	cat header.md >> README.md
	echo "[TOC]" >> README.md
	$(MAKE) compile.body

compile.body:
	cat intro.md >> README.md
	cat usage.md >> README.md
	cat implementation.md >> README.md
	cat closing.md >> README.md

docs:
	rm README.html &
	rm README.md &
	
	$(MAKE) compile.web
	cat static/header.html > README.html
	markdown -x toc README.md >> README.html 
	cat static/footer.html >> README.html
	
	rm README.md &
	$(MAKE) compile.github
