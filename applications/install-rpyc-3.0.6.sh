# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Copyright (c) 1997-2016 California Institute of Technology.
# Copyright (c) 2016-2023 The Uncertainty Quantification Foundation.
# License: 3-clause BSD.  The full license text is available at:
#  - https://github.com/uqfoundation/pathos/blob/master/LICENSE
#
  NAME=rpyc
  VERSION=3.0
  REVISION=6
  IDENTIFIER=$NAME-$VERSION.$REVISION
  PREFIX=$HOME
  rm -fr $IDENTIFIER.tar.gz
  wget http://superb-east.dl.sourceforge.net/sourceforge/$NAME/$IDENTIFIER.tar.gz
  rm -fr $IDENTIFIER
  tar zxvf $IDENTIFIER.tar.gz
  cd $IDENTIFIER

  python setup.py build
  python setup.py install --prefix=$PREFIX

  cp -f $NAME/servers/classic_server.py $PREFIX/bin
  cp -f $NAME/servers/registry_server.py $PREFIX/bin
  cp -f $NAME/servers/vdbconf.py $PREFIX/bin

  cd ..
