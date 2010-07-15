

POSTCRIPTS:=$(patsubst %.dot, %.ps, $(wildcard *.dot))
PDFS:=$(patsubst %.dot, %.pdf, $(wildcard *.dot))
SOURCE_ROOT=../../..

all:   generate $(POSTCRIPTS) $(PDFS)


generate:
	for workflow in `find $(SOURCE_ROOT) -name definition.xml`;\
	do 							\
	    ./workflowGraph --workflow=$$workflow;		\
	done

	

%.ps:	%.dot
	dot -Tps -Grankdir=BT $< >$@

%.pdf:  %.ps
	ps2pdf $< $@