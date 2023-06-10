MARKDOWN=$(wildcard *.md)
MARKDOWN_HTML=$(patsubst %.md,%.html,$(MARKDOWN))

.PHONY: markdown

markdown: $(MARKDOWN_HTML)

$(MARKDOWN_HTML): %.html: %.md style.css
	pandoc --standalone --css=style.css --mathjax="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.3/MathJax.js?config=TeX-MML-AM_CHTML" -f markdown+gfm_auto_identifiers+emoji+autolink_bare_uris --highlight-style haddock --toc -t html5  $< -o $@

zip: markdown
	make -C acotsp/src clean
	rm -f ../irace-exercises.zip
	zip -r ../irace-exercises.zip . -x 'Makefile' '*.md' '*.git*' '*~' '*.DS_Store*' '*__py*' 'acotsp/*' '*.Rdata' '*report.html' '*/report_files/*'
