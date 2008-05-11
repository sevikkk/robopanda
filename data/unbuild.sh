#!/bin/sh -x

if [ -z "$1" ]; then
	exit 1
fi

../scripts/unbuild.py $1.bin>$1.src

