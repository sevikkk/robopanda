	jump $start

        .org 128
start:
	writeuart "URA!!!\r\n"

        writeuart "Clear DRAM..."
	read #32768
	write cnt
	read #0
	write idx2
	read #0x12345678
clear_ram:
	writedram @idx2+
	loop $clear_ram
        writeuart "done\r\n"

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
	
main_loop:
        writeuart "\r\nOk> "
    1:
        jump $1,!tx_empty
    2:
        jump $2,!rx_rdy
        read uart
        write uart
        writeuart "\r\n"

	skip !'r'
	jump $do_r

	skip !'i'
	jump $do_i

	skip !'g'
	jump #0

        writeuart "Error!"
	jump $main_loop

do_r:
	writeuart "SD Read..."
	read #0
	writewb @7
	writewb @8
	writewb @9
	writewb @10
	read #2
	writewb @2
	read #1
	writewb @3

sd_read:
	readwb @4 // TRANS_STS_REG
	skip !1   // != TRANS_BUSY
	jump $sd_read

        writeuart "done, code: "
	readwb @5 // TRANS_ERROR_REG
	writeuart acc, hex1
        writeuart "\r\nCount: "

	readwb @18
	writeuart acc, hex1
	readwb @19
	writeuart acc, hex1
        writeuart "\r\n"

	read #127
	write cnt
	read #0
	write idx2

sd_read_loop:
	read #0
	readwb @16
	shift left8
	readwb @16
	shift left8
	readwb @16
	shift left8
	readwb @16

	writeuart acc, hex4
        writeuart " "
	write @idx2+
    w:
        jump $w,!tx_empty
	loop $sd_read_loop
        writeuart "\r\n"

        jump $main_loop

