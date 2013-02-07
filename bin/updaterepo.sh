#!/bin/sh
cd RPMS/x86_64
rm -f *.noarch.rpm
ln -s ../noarch/*.rpm .
createrepo .
