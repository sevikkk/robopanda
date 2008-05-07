#!/bin/sh -x

CDIR=`pwd`
TDIR=`mktemp -d /var/tmp/zzXXXX`
cd $CDIR
svn export svn+ssh://rocky/data/ipnet/svn/sandbox/seva/robopanda robopanda_tools
rm -r robopanda_tools/virtex

tar cvzf $CDIR/robopanda_tools-`date +%Y%m%d%H%M`.tar.gz robopanda_tools
rm -r $TDIR

