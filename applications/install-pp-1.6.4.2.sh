# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/pathos/browser/pathos/LICENSE
#
  NAME=pp
  VERSION=1.6.4
  REVISION=2
  IDENTIFIER=$NAME-$VERSION.$REVISION
  PREFIX=$HOME
  rm -fr $IDENTIFIER.zip
  wget http://dev.danse.us/packages/$IDENTIFIER.zip
 #wget http://www.parallelpython.com/downloads/$NAME/$IDENTIFIER.tar.gz
  rm -fr $IDENTIFIER
  tar zxvf $IDENTIFIER.zip
  cd $IDENTIFIER

  python setup.py build
  python setup.py install --prefix=$PREFIX
  cd ..
