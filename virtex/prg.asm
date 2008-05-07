        writeuart "Load ..."

	read #1  // first sector number
	write r2

	read #128  // start addr
	write idx2

boot_loop:
	read r2
	shift left8
	shift left1

	writewb @7   // sector number
	shift right8
	writewb @8
	shift right8
	writewb @9
	shift right8
	writewb @10

        read #2
        writewb @2
        read #1
        writewb @3

boot_sd_read:
        readwb @4 // TRANS_STS_REG
        skip !1   // != TRANS_BUSY
        jump $boot_sd_read

        readwb @5 // TRANS_ERROR_REG
        skip !0
        jump $boot_read_ok

        writeuart "error, code: "
        writeuart acc, hex1
	writeuart " sector: "
	read r2
	writeuart acc, hex4
	writeuart "\r\n"

boot_error:
	jump $boot_error

boot_read_ok:
        read #127
        write cnt

boot_read_loop:
	read #0
        readwb @16
        shift left8
        readwb @16
        shift left8
        readwb @16
        shift left8
        readwb @16

	write @idx2+
	loop $boot_read_loop

        read r2
        addl #1
        write r2
        skip =8
        jump $boot_loop
        writeuart " done\r\n"

main_loop:
        writeuart "\r\nOk> "
    1:
        jump $1,!tx_empty
    2:
        jump $2,!rx_rdy
        read uart
        write uart
        writeuart "\r\n"

	skip !'w'
	jump $do_w

	skip !'i'
	jump $do_i

	skip !'c'
	jump $do_c

	skip !'r'
	jump $do_r

        writeuart "Error!"
	jump $main_loop

do_w:
	writeuart "SD write...\r\n"

	read #0xC000 // sectors to write
	write r0

	read #10  // first sector number
	write r2

	read #0  // start addr
	write idx

sector_loop:
	read r2
	shift left8
	shift left1

	writewb @7   // sector number
	shift right8
	writewb @8
	shift right8
	writewb @9
	shift right8
	writewb @10

	read #127 // loops for fifo write
	write cnt

fifo_loop:
	readdram @idx+
	writewb @32
	shift right8
	writewb @32
	shift right8
	writewb @32
	shift right8
	writewb @32

	loop $fifo_loop

        writeuart "F"

	read #3
	writewb @2 // transaction type: write

	read #1
	writewb @3 // transaction start

sd_write:
	readwb @4 // TRANS_STS_REG
	skip !1   // != TRANS_BUSY
	jump $sd_write

	readwb @5 // TRANS_ERROR_REG
	skip !0
	jump $write_ok

        writeuart "write error, code: "
	writeuart acc, hex1

	writeuart " sector: "
	read r2
	writeuart acc, hex4

        writeuart "\r\n"

        jump $main_loop

write_ok:
	jump $write_ok,!tx_empty
	writeuart "W"
	read r2
	addl #1
	write r2
	read r0
	subl #1
	write r0
	writeuart acc, hex4
	writeuart "\r"
	skip =0
	jump $sector_loop

        writeuart "\r\ndone          \r\n"

        jump $main_loop

do_i:
        writeuart "Init SDCard..."
	read #1
	writewb @2 // SPI_TRANS_TYPE_REG = SPI_INIT_SD
	writewb @3 // SPI_TRANS_CTRL_REG = SPI_TRANS_START

sd_init:
	readwb @4 // TRANS_STS_REG
	skip !1   // != TRANS_BUSY
	jump $sd_init

        writeuart "done, code: "
	readwb @5 // TRANS_ERROR_REG
	writeuart acc, hex1
        writeuart "\r\n"

        jump $main_loop

do_c:
        writeuart "Clear sniffer memory..."
	read #0x600000
	write cnt
	read #0
	write idx2
	read #0xceba1234

cm_loop:
	writedram @idx2+
	loop $cm_loop
        writeuart "done"

        jump $main_loop

do_r:
	writeuart "Read cartridge data...\r\n"
	read #0x600000 // start addr
	write idx2
	read #0x4000 // number of sectors
	write r1
	read #0x10000 // start sector
	write r2

cr_loop:
	read r2
	shift left8
	shift left1

	writewb @7   // sector number
	shift right8
	writewb @8
	shift right8
	writewb @9
	shift right8
	writewb @10

        read #2
        writewb @2
        read #1
        writewb @3

cr_sd_read:
        readwb @4 // TRANS_STS_REG
        skip !1   // != TRANS_BUSY
        jump $cr_sd_read

        readwb @5 // TRANS_ERROR_REG
        skip !0
        jump $cr_read_ok

        writeuart "error, code: "
        writeuart acc, hex1
	writeuart " sector: "
	read r2
	writeuart acc, hex4
	writeuart "\r\n"

	jump $main_loop

cr_read_ok:
        read #127
        write cnt

cr_read_loop:
	read #0
        readwb @16
        shift left8
        readwb @16
        shift left8
        readwb @16
        shift left8
        readwb @16

	writedram @idx2+
	loop $cr_read_loop

        read r2
        addl #1
        write r2
        read r1
        subl #1
        write r1
	writeuart acc, hex4
	writeuart "\r"
        skip =0
        jump $cr_loop
        writeuart " done        \r\n"
	jump $main_loop
