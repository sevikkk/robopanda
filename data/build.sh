#!/bin/sh -x

if [ -z "$1" ]; then
	exit 1
fi

../scripts/build.py $1.cfg $1.bin

