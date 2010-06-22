# -*- Makefile -*-

PROJECT = pathos
PACKAGE = applications

PROJ_TIDY += *.log *.out
PROJ_CLEAN =

#--------------------------------------------------------------------------
#

#all: export
all: clean

#--------------------------------------------------------------------------
#

EXPORT_BINS = \
    install_pathos_server.py \


export:: export-binaries release-binaries


# End of file
