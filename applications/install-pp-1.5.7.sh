  NAME=pp
  VERSION=1.5.7
  REVISION=pathos
  IDENTIFIER=$NAME-$VERSION-$REVISION
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
