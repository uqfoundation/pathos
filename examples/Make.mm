# -*- Makefile -*-
#

PROJECT = pathos
PACKAGE = examples

PROJ_TIDY += *txt
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
    sum_primesX.py \
    pp_map.py \
    secure_copy.py \
    secure_hello.py \
    simple_tunnel.py \
    spawn.py \


# export:: export-package-python-modules
export:: export-binaries release-binaries


# End of file
