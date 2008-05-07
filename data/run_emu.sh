#!/bin/sh -x

if [ -z "$1" ]; then
	exit 1
fi

CARTRIDGE=${2:-cartridge_black.bin}

../scripts/emu.py $CARTRIDGE $1.txt> $1.log

