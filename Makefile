


# DEPENDENCIES:
# Install collective.dist (within the python used)
# journalcommons is defined in $HOME/.pypirc
REPOSITORY=journalcommons
PYTHON=../../zinstance/Python-2.4/bin/python2.4 

EGGS=journalcommons.Journal journalcommons.Conference

all:
	$(MAKE) COMMAND=upload forall

alldist:
	$(MAKE) COMMAND=dodist forall

forall:
	@for egg in $(EGGS);		\
	do				\
	    echo Processing $$egg;	\
	    cd $$egg;			\
	    make -f ../Makefile $(COMMAND);	\
	done
	
dodist:
	$(PYTHON) setup.py bdist_egg
	scp dist/* root@www.historicalmaterialism.org:/opt/plone/dev-eggs

upload:
	$(PYTHON) setup.py sdist mupload -r $(REPOSITORY)

register:	
	$(PYTHON) setup.py sdist mregister -r $(REPOSITORY)

setup:
	$(EASY_INSTALL) collective.dist

