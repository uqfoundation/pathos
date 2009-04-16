# -*- Makefile -*-
#

PROJECT = pathos
PACKAGE = tests

PROJ_CLEAN += $(PROJ_CPPTESTS)

PROJ_PYTESTS = 
PROJ_CPPTESTS = 
PROJ_TESTS = $(PROJ_PYTESTS) # $(PROJ_CPPTESTS)
PROJ_LIBRARIES = -L$(BLD_LIBDIR) # -lpathos

#--------------------------------------------------------------------------
#

all: $(PROJ_TESTS)

test:
	for test in $(PROJ_TESTS) ; do $${test}; done

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#


# End of file

