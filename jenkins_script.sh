#!/bin/bash

rm -rf tabular-predDB
git clone --depth=1 https://probcomp-reserve:metropolis1953@github.com/mit-probabilistic-computing-project/tabular-predDB.git
cd tabular-predDB
if [ ! -e /var/lib/jenkins/.virtualenvs ]
then
  bash -i virtualenv_setup.sh jenkins /var/lib/jenkins >virtualenv.out 2>virtualenv.err
fi
. /var/lib/jenkins/.virtualenvs/tabular_predDB/bin/activate
cd /var/lib/jenkins/workspace/C++\ unit\ tests/tabular-predDB
make tests
cd tests
nosetests --with-xunit cpp_unit_tests.py cpp_long_tests.py
