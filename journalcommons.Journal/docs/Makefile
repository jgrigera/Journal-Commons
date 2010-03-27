
POSTCRIPTS=$(patsubst %.dot, %.ps, $(wildcard *.dot))
PDFS=$(patsubst %.dot, %.pdf, $(wildcard *.dot))


all:    $(POSTCRIPTS) $(PDFS)

	

%.ps:	%.dot
	dot -Tps -Grankdir=LR $< >$@

%.pdf:  %.ps
	ps2pdf $< $@