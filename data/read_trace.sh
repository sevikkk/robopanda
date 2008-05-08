#!/bin/sh -x

if [ -z "$1" ]; then
	exit 1
fi

sudo dd if=/dev/da0 of=trace_$1.bin bs=1m count=32

