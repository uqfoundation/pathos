  NAME=pp
  VERSION=1.5.7
 #REVISION=1
  IDENTIFIER=$NAME-$VERSION
  PREFIX=$HOME
  rm -fr $IDENTIFIER.tar.gz
  wget http://www.parallelpython.com/downloads/$NAME/$IDENTIFIER.tar.gz
  rm -fr $IDENTIFIER
  tar zxvf $IDENTIFIER.tar.gz
  cd $IDENTIFIER

  python setup.py build
  python setup.py install --prefix=$PREFIX
  cd ..
