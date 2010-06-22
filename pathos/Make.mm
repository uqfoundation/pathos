# -*- Makefile -*-
 
PROJECT = pathos
PACKAGE = pathos

BUILD_DIRS = 
RECURSE_DIRS = $(BUILD_DIRS)

PROJ_TIDY += *.txt
PROJ_CLEAN = 

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

release: tidy
	cvs release .

update: clean
	cvs update .

#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
    __init__.py      \
    _ppserver_config.py    \
    Launcher.py      \
    LauncherSSH.py   \
    LauncherSCP.py   \
    Tunnel.py        \
    core.py          \
    hosts.py         \
    pp_map.py        \
    util.py          \
    Server.py        \
    XMLRPCServer.py  \
    XMLRPCRequestHandler.py \

export:: export-python-modules

# End of file
