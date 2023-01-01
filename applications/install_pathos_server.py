#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
"""
remote bash-script installation of selected package

Usage: python install_pathos_server.py [package] [version] [hostname] 
    [package] - name of the package to install
    [version] - version of the package to install
    [hostname] - name of the host on which to install the package
"""

from pathos.core import copy,execute
from pathos.hosts import get_profile, register_profiles


if __name__ == '__main__':

##### CONFIGURATION & INPUT ########################
  # set the default remote host
  rhost = 'localhost'
 #rhost = 'foobar.danse.us'
 #rhost = 'computer.cacr.caltech.edu'

  # set any 'special' profiles (those which don't use default_profie)
  profiles = {'foobar.danse.us':'.profile',
              'computer.cacr.caltech.edu':'.cshrc'}

  from time import sleep
  delay = 0.0
  big_delay = 5.0

  # set the default package & version
  package = 'pp'    #XXX: package name MUST correspond to X in installer-X.sh
  version = '1.5.7' #XXX: also hardwired in installer-X.sh

  print("""Usage: python install_pathos_server.py [package] [version] [hostname] 
    [package] - name of the package to install
    [version] - version of the package to install
    [hostname] - name of the host on which to install the package
    defaults are: "%s" "%s" "%s".""" % (package, version, rhost))

  # get package to install from user
  import sys
  if '--help' in sys.argv:
    sys.exit(0)
  try:
    myinp = sys.argv[1],sys.argv[2]
  except: myinp = None
  if myinp:
    package,version = myinp #XXX: should test validity here... (filename)
  else: pass # use default
  del myinp

  # get remote hostname from user
  import sys
  try:
    myinp = sys.argv[3]
  except: myinp = None
  if myinp:
    rhost = myinp #XXX: should test rhost validity here... (how ?)
  else: pass # use default
  del myinp

  # get remote profile (this should go away soon)
  import sys
  try:
    myinp = sys.argv[4]
  except: myinp = None
  if myinp:
    rprof = myinp #XXX: should test validity here... (filename)
    profiles = {rhost:rprof}
  else: pass # use default
  del myinp

  # my remote environment (should be auto-detected)
  register_profiles(profiles)
  profile = get_profile(rhost)

##### CONFIGURATION & INPUT ########################

  file = 'install-%s-%s.sh' % (package,version)
  # XXX: should use easy_install, if is installed...

  import tempfile
# tempfile.tempdir = "~" #XXX: uncomment if cannot install to '/tmp'
  dest = tempfile.mktemp()+"_install" #XXX: checks local (not remote)

  # check for existing installation
  command = "source %s; python -c 'import %s'" % (profile,package)
  error = execute(command,rhost).response()
  if error in ['', None]:
    print('%s is already installed on %s' % (package,rhost))
# elif error[:39] == 'This system is available for legitimate use'[:39] \
#      and rhost[:3] == 'shc-b.cacr.caltech.edu'[:3]:
##     and error[-35:-1] == 'an authorized user of this system.'[-35:] \
#   print('%s is already installed on %s' % (package,rhost))
    #XXX: could parse 'error' for "ImportError" ==> not installed
    #XXX: could use command="python -c 'import X; X.__version__'"
    #XXX  ...returns version# or "AttributeError" ==> non-standard version tag
  else:
    print(error)
    sleep(delay)

    # create install directory
    command = 'mkdir -p %s' % dest #FIXME: *nix only
    report = execute(command,rhost).response()
    #XXX: could check for clean install by parsing for "Error" (?)
    sleep(delay)

    # copy over the installer to remote host
    copy(file,rhost,dest)
    sleep(delay)

    # run the installer
    command = 'cd %s; ./%s' % (dest,file) #FIXME: *nix only
    report = execute(command,rhost).response()
    #XXX: could check for clean install by parsing for "Error" (?)
    sleep(big_delay)

    # remove remote install file
#   killme = dest+'/'+file  #FIXME: *nix only
#   command = 'rm -f %s' % killme #FIXME: *nix only
#   execute(command,rhost).response()

    # remove remote package unpacking directory
#   killme = dest+'/'+package+'-'+version #FIXME: dies for NON-STANDARD naming
#   command = 'rm -rf %s' % killme #FIXME: *nix only
#   execute(command,rhost).response()

    # remove remote install directory
    killme = dest
    command = 'rm -rf %s' % killme #FIXME: *nix only
    execute(command,rhost).response()

    # check installation
    command = "source %s; python -c 'import %s'" % (profile,package)
    error = execute(command,rhost).response()
    if error in ['', None]:
      pass # is installed
    else:
      print(error)
#     raise ImportError("failure to install package")

