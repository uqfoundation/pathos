# -*- Makefile -*-
#

PROJECT = pathos
PACKAGE = examples

PROJ_TIDY +=
PROJ_CLEAN =

#--------------------------------------------------------------------------

#all: export
all: clean

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

#EXPORT_PYTHON_MODULES = \
EXPORT_BINS = \
#   dummy_example.py \


# export:: export-package-python-modules
export:: export-binaries release-binaries


# End of file
