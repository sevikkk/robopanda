#!/bin/sh -x

if [ -z "$1" ]; then
	exit 1
fi

../scripts/byteswap.py $1.bin $1.sbin
sudo dd if=$1.sbin of=/dev/da0 bs=1m oseek=32

