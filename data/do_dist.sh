#!/bin/sh -x

CDIR=`pwd`
TDIR=`mktemp -d /var/tmp/zzXXXX`
cd $CDIR
svn export svn+ssh://rocky/data/ipnet/svn/sandbox/seva/robopanda robopanda_tools
mv robopanda_tools/virtex robopanda_hwemu

VER=`date +%Y%m%d%H%M`
tar cvzf $CDIR/robopanda_tools-${VER}.tar.gz robopanda_tools
tar cvzf $CDIR/robopanda_hwemu-${VER}.tar.gz robopanda_hwemu
rm -r $TDIR

