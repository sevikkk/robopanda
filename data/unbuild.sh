#!/bin/sh -x

if [ -z "$1" ]; then
	exit 1
fi

rm -rf dump
../scripts/unbuild.py $1.bin>$1.src
rm -rf dump_$1
mv dump dump_$1

