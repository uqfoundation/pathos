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
