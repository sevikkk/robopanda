#!/bin/sh -x

if [ -z "$1" ]; then
	exit 1
fi

CARTRIDGE=${2:-cartridge_black.bin}

../scripts/spi_decode.py trace_$1.bin > $1.txt
../scripts/fill_data.py $1.txt $CARTRIDGE > $1_data.txt

