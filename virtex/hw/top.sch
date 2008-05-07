VERSION 6
BEGIN SCHEMATIC
    BEGIN ATTR DeviceFamilyName "virtexe"
        DELETE all:0
        EDITNAME all:0
        EDITTRAIT all:0
    END ATTR
    BEGIN NETLIST
        BEGIN SIGNAL reset
        END SIGNAL
        SIGNAL clk_80
        SIGNAL XLXN_1004
        SIGNAL CLK60
        SIGNAL XLXN_780
        SIGNAL XLXN_781
        SIGNAL XLXN_786
        SIGNAL XLXN_851
        SIGNAL XLXN_790
        SIGNAL spi_cs
        SIGNAL XLXN_854
        SIGNAL XLXN_1063
        SIGNAL vga_data(31:0)
        SIGNAL vga_addr(23:0)
        SIGNAL dram_dq(31:0)
        SIGNAL dram_a(11:0)
        SIGNAL dram_di(31:0)
        SIGNAL dram_cas
        SIGNAL dram_ras
        SIGNAL dram_we
        SIGNAL dram_t
        SIGNAL wr_we
        SIGNAL XLXN_869
        SIGNAL wr_addr(23:0)
        SIGNAL wr_data(31:0)
        SIGNAL refr
        SIGNAL wr_ack
        SIGNAL XLXN_855
        SIGNAL XLXN_1529
        SIGNAL XLXN_868
        SIGNAL vga_b
        SIGNAL vga_hsync
        SIGNAL x(10:0)
        SIGNAL y(10:0)
        SIGNAL vga_vsync
        SIGNAL XLXN_1062
        SIGNAL vga_r
        SIGNAL vga_g
        SIGNAL int2_dat(15)
        SIGNAL int_dat(15:0)
        SIGNAL int_dat(15)
        SIGNAL int2_dat(15:0)
        SIGNAL vga_data(15:0)
        SIGNAL vga_data(31:16)
        SIGNAL vcc_n
        SIGNAL XLXN_1986
        SIGNAL XLXN_839
        SIGNAL clk_30
        SIGNAL spi_clk
        SIGNAL spi_si
        SIGNAL spi_so
        SIGNAL XLXN_2164
        BEGIN SIGNAL reset_30
        END SIGNAL
        SIGNAL XLXN_866
        SIGNAL XLXN_862
        SIGNAL XLXN_1987
        SIGNAL uart_rxd
        SIGNAL XLXN_2156(7:0)
        SIGNAL XLXN_2157(7:0)
        SIGNAL XLXN_2158(7:0)
        SIGNAL XLXN_2159
        SIGNAL XLXN_2160
        SIGNAL XLXN_2161
        SIGNAL XLXN_2162(7:0)
        SIGNAL XLXN_2163
        SIGNAL tx_fifo_empty
        SIGNAL XLXN_2173
        SIGNAL XLXN_2174(7:0)
        SIGNAL sd_clk
        SIGNAL sd_do
        SIGNAL sd_di
        SIGNAL sd_cs
        SIGNAL tx_enable
        SIGNAL uart_txd
        SIGNAL XLXN_2165(7:0)
        SIGNAL XLXN_2169
        SIGNAL XLXN_2181
        SIGNAL XLXN_2168
        SIGNAL dram_wb_ack
        SIGNAL dram_wb_idata(31:0)
        SIGNAL dram_wb_stb
        SIGNAL dram_wb_we
        SIGNAL dram_wb_addr(22:0)
        SIGNAL dram_wb_odata(31:0)
        SIGNAL mem_wr
        SIGNAL capture_active
        SIGNAL XLXN_2233
        SIGNAL rd_data(31:0)
        SIGNAL spi_so_emu
        PORT Input CLK60
        PORT Input spi_cs
        PORT Input dram_dq(31:0)
        PORT Output dram_a(11:0)
        PORT Output dram_di(31:0)
        PORT Output dram_cas
        PORT Output dram_ras
        PORT Output dram_we
        PORT Output dram_t
        PORT Output vga_b
        PORT Output vga_hsync
        PORT Output vga_vsync
        PORT Output vga_r
        PORT Output vga_g
        PORT Input spi_clk
        PORT Input spi_si
        PORT Input spi_so
        PORT Input uart_rxd
        PORT Output sd_clk
        PORT Output sd_do
        PORT Input sd_di
        PORT Output sd_cs
        PORT Output uart_txd
        PORT Input mem_wr
        PORT Output capture_active
        PORT Output spi_so_emu
        BEGIN BLOCKDEF and2
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 0 -64 64 -64 
            LINE N 0 -128 64 -128 
            LINE N 256 -96 192 -96 
            ARC N 96 -144 192 -48 144 -48 144 -144 
            LINE N 144 -48 64 -48 
            LINE N 64 -144 144 -144 
            LINE N 64 -48 64 -144 
        END BLOCKDEF
        BEGIN BLOCKDEF gen_reset
            TIMESTAMP 2008 4 13 17 2 32
            LINE N 64 32 0 32 
            LINE N 64 -32 0 -32 
            LINE N 320 -32 384 -32 
            RECTANGLE N 64 -64 320 128 
        END BLOCKDEF
        BEGIN BLOCKDEF gnd
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 64 -64 64 -96 
            LINE N 76 -48 52 -48 
            LINE N 68 -32 60 -32 
            LINE N 88 -64 40 -64 
            LINE N 64 -64 64 -80 
            LINE N 64 -128 64 -96 
        END BLOCKDEF
        BEGIN BLOCKDEF inv
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 0 -32 64 -32 
            LINE N 224 -32 160 -32 
            LINE N 64 -64 128 -32 
            LINE N 128 -32 64 0 
            LINE N 64 0 64 -64 
            CIRCLE N 128 -48 160 -16 
        END BLOCKDEF
        BEGIN BLOCKDEF buf
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 0 -32 64 -32 
            LINE N 224 -32 128 -32 
            LINE N 64 0 128 -32 
            LINE N 128 -32 64 -64 
            LINE N 64 -64 64 0 
        END BLOCKDEF
        BEGIN BLOCKDEF vcc
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 64 -32 64 -64 
            LINE N 64 0 64 -32 
            LINE N 96 -64 32 -64 
        END BLOCKDEF
        BEGIN BLOCKDEF vga_sync_gen
            TIMESTAMP 2008 4 13 16 4 46
            RECTANGLE N 320 276 384 300 
            LINE N 320 288 384 288 
            LINE N 320 96 384 96 
            LINE N 320 160 384 160 
            LINE N 320 224 384 224 
            LINE N 64 32 0 32 
            LINE N 64 -288 0 -288 
            LINE N 320 -288 384 -288 
            LINE N 320 -224 384 -224 
            LINE N 320 -160 384 -160 
            RECTANGLE N 320 -108 384 -84 
            LINE N 320 -96 384 -96 
            RECTANGLE N 64 -320 320 320 
        END BLOCKDEF
        BEGIN BLOCKDEF clkdlle
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 384 -576 320 -576 
            LINE N 384 -512 320 -512 
            LINE N 384 -448 320 -448 
            LINE N 0 -448 64 -448 
            LINE N 0 -512 64 -512 
            LINE N 0 -128 64 -128 
            LINE N 384 -128 320 -128 
            LINE N 384 -192 320 -192 
            LINE N 384 -384 320 -384 
            LINE N 384 -256 320 -256 
            LINE N 384 -320 320 -320 
            LINE N 64 -432 80 -448 
            LINE N 80 -448 64 -464 
            LINE N 64 -496 80 -512 
            LINE N 80 -512 64 -528 
            RECTANGLE N 64 -636 320 -64 
        END BLOCKDEF
        BEGIN BLOCKDEF vga_addr_ctrl
            TIMESTAMP 2008 4 17 20 51 21
            LINE N 64 96 0 96 
            LINE N 64 160 0 160 
            LINE N 64 32 0 32 
            LINE N 64 -224 0 -224 
            LINE N 64 -32 0 -32 
            LINE N 320 -224 384 -224 
            RECTANGLE N 320 -44 384 -20 
            LINE N 320 -32 384 -32 
            RECTANGLE N 64 -256 320 192 
        END BLOCKDEF
        BEGIN BLOCKDEF sr16cle
            TIMESTAMP 2000 1 1 10 10 10
            RECTANGLE N 64 -640 320 -64 
            LINE N 0 -128 64 -128 
            LINE N 0 -192 64 -192 
            LINE N 0 -32 64 -32 
            LINE N 0 -512 64 -512 
            LINE N 0 -320 64 -320 
            LINE N 384 -384 320 -384 
            LINE N 0 -576 64 -576 
            LINE N 80 -128 64 -144 
            LINE N 64 -112 80 -128 
            LINE N 192 -32 64 -32 
            LINE N 192 -64 192 -32 
            RECTANGLE N 0 -524 64 -500 
            RECTANGLE N 320 -396 384 -372 
        END BLOCKDEF
        BEGIN BLOCKDEF dram_ctrl
            TIMESTAMP 2008 4 23 22 9 27
            LINE N 64 96 0 96 
            LINE N 64 160 0 160 
            RECTANGLE N 0 212 64 236 
            LINE N 64 224 0 224 
            RECTANGLE N 0 276 64 300 
            LINE N 64 288 0 288 
            LINE N 400 96 464 96 
            RECTANGLE N 400 148 464 172 
            LINE N 400 160 464 160 
            LINE N 64 32 0 32 
            LINE N 400 32 464 32 
            LINE N 64 -608 0 -608 
            LINE N 64 -544 0 -544 
            LINE N 64 -480 0 -480 
            LINE N 64 -416 0 -416 
            LINE N 64 -352 0 -352 
            RECTANGLE N 0 -300 64 -276 
            LINE N 64 -288 0 -288 
            RECTANGLE N 0 -236 64 -212 
            LINE N 64 -224 0 -224 
            RECTANGLE N 0 -172 64 -148 
            LINE N 64 -160 0 -160 
            RECTANGLE N 0 -108 64 -84 
            LINE N 64 -96 0 -96 
            LINE N 400 -608 464 -608 
            LINE N 400 -544 464 -544 
            LINE N 400 -480 464 -480 
            LINE N 400 -416 464 -416 
            LINE N 400 -352 464 -352 
            LINE N 400 -288 464 -288 
            RECTANGLE N 400 -236 464 -212 
            LINE N 400 -224 464 -224 
            RECTANGLE N 400 -172 464 -148 
            LINE N 400 -160 464 -160 
            RECTANGLE N 400 -108 464 -84 
            LINE N 400 -96 464 -96 
            RECTANGLE N 400 -44 464 -20 
            LINE N 400 -32 464 -32 
            RECTANGLE N 64 -640 400 320 
        END BLOCKDEF
        BEGIN BLOCKDEF cb8ce
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 384 -128 320 -128 
            RECTANGLE N 320 -268 384 -244 
            LINE N 384 -256 320 -256 
            LINE N 0 -192 64 -192 
            LINE N 192 -32 64 -32 
            LINE N 192 -64 192 -32 
            LINE N 80 -128 64 -144 
            LINE N 64 -112 80 -128 
            LINE N 0 -128 64 -128 
            LINE N 0 -32 64 -32 
            LINE N 384 -192 320 -192 
            RECTANGLE N 64 -320 320 -64 
        END BLOCKDEF
        BEGIN BLOCKDEF fdce
            TIMESTAMP 2000 1 1 10 10 10
            LINE N 0 -128 64 -128 
            LINE N 0 -192 64 -192 
            LINE N 0 -32 64 -32 
            LINE N 0 -256 64 -256 
            LINE N 384 -256 320 -256 
            LINE N 64 -112 80 -128 
            LINE N 80 -128 64 -144 
            LINE N 192 -64 192 -32 
            LINE N 192 -32 64 -32 
            RECTANGLE N 64 -320 320 -64 
        END BLOCKDEF
        BEGIN BLOCKDEF wrdata_fifo
            TIMESTAMP 2008 4 16 20 13 27
            RECTANGLE N 32 32 544 672 
            BEGIN LINE W 0 80 32 80 
            END LINE
            LINE N 0 144 32 144 
            LINE N 0 240 32 240 
            LINE N 0 368 32 368 
            LINE N 144 704 144 672 
            BEGIN LINE W 576 80 544 80 
            END LINE
            LINE N 576 208 544 208 
            LINE N 576 432 544 432 
        END BLOCKDEF
        BEGIN BLOCKDEF RxUnit
            TIMESTAMP 2008 4 17 20 55 48
            RECTANGLE N 64 -320 320 0 
            LINE N 64 -288 0 -288 
            LINE N 64 -224 0 -224 
            LINE N 64 -160 0 -160 
            LINE N 64 -96 0 -96 
            LINE N 64 -32 0 -32 
            LINE N 320 -288 384 -288 
            LINE N 320 -208 384 -208 
            LINE N 320 -128 384 -128 
            RECTANGLE N 320 -60 384 -36 
            LINE N 320 -48 384 -48 
        END BLOCKDEF
        BEGIN BLOCKDEF ClkUnit
            TIMESTAMP 2008 4 17 20 55 38
            RECTANGLE N 64 -128 320 0 
            LINE N 64 -96 0 -96 
            LINE N 64 -32 0 -32 
            LINE N 320 -96 384 -96 
            LINE N 320 -32 384 -32 
        END BLOCKDEF
        BEGIN BLOCKDEF TxUnit
            TIMESTAMP 2008 4 17 20 55 56
            RECTANGLE N 64 -320 320 0 
            LINE N 64 -288 0 -288 
            LINE N 64 -224 0 -224 
            LINE N 64 -160 0 -160 
            LINE N 64 -96 0 -96 
            RECTANGLE N 0 -44 64 -20 
            LINE N 64 -32 0 -32 
            LINE N 320 -288 384 -288 
            LINE N 320 -160 384 -160 
            LINE N 320 -32 384 -32 
        END BLOCKDEF
        BEGIN BLOCKDEF spiMaster
            TIMESTAMP 2008 4 20 18 8 28
            RECTANGLE N 64 -512 384 0 
            LINE N 64 -480 0 -480 
            LINE N 64 -416 0 -416 
            LINE N 64 -352 0 -352 
            LINE N 64 -288 0 -288 
            LINE N 64 -224 0 -224 
            LINE N 64 -160 0 -160 
            RECTANGLE N 0 -108 64 -84 
            LINE N 64 -96 0 -96 
            RECTANGLE N 0 -44 64 -20 
            LINE N 64 -32 0 -32 
            LINE N 384 -480 448 -480 
            LINE N 384 -368 448 -368 
            LINE N 384 -256 448 -256 
            LINE N 384 -144 448 -144 
            RECTANGLE N 384 -44 448 -20 
            LINE N 384 -32 448 -32 
        END BLOCKDEF
        BEGIN BLOCKDEF sys_ctrl
            TIMESTAMP 2008 4 24 19 5 1
            LINE N 64 32 0 32 
            RECTANGLE N 0 84 64 108 
            LINE N 64 96 0 96 
            LINE N 432 32 496 32 
            LINE N 432 96 496 96 
            RECTANGLE N 432 148 496 172 
            LINE N 432 160 496 160 
            RECTANGLE N 432 212 496 236 
            LINE N 432 224 496 224 
            LINE N 64 -416 0 -416 
            LINE N 64 -352 0 -352 
            LINE N 64 -288 0 -288 
            LINE N 64 -224 0 -224 
            LINE N 64 -160 0 -160 
            RECTANGLE N 0 -108 64 -84 
            LINE N 64 -96 0 -96 
            RECTANGLE N 0 -44 64 -20 
            LINE N 64 -32 0 -32 
            LINE N 432 -416 496 -416 
            LINE N 432 -352 496 -352 
            LINE N 432 -288 496 -288 
            LINE N 432 -224 496 -224 
            RECTANGLE N 432 -172 496 -148 
            LINE N 432 -160 496 -160 
            RECTANGLE N 432 -108 496 -84 
            LINE N 432 -96 496 -96 
            RECTANGLE N 432 -44 496 -20 
            LINE N 432 -32 496 -32 
            RECTANGLE N 64 -448 432 256 
        END BLOCKDEF
        BEGIN BLOCKDEF tx_fifo_ctrl
            TIMESTAMP 2008 4 21 21 44 40
            RECTANGLE N 64 -256 320 0 
            LINE N 64 -224 0 -224 
            LINE N 64 -160 0 -160 
            LINE N 64 -96 0 -96 
            LINE N 64 -32 0 -32 
            LINE N 320 -224 384 -224 
            LINE N 320 -32 384 -32 
        END BLOCKDEF
        BEGIN BLOCKDEF spi_emu
            TIMESTAMP 2008 5 6 9 42 32
            LINE N 464 32 528 32 
            LINE N 64 -544 0 -544 
            LINE N 64 -480 0 -480 
            LINE N 64 -416 0 -416 
            LINE N 64 -352 0 -352 
            LINE N 64 -288 0 -288 
            LINE N 64 -224 0 -224 
            LINE N 64 -160 0 -160 
            LINE N 64 -96 0 -96 
            RECTANGLE N 0 -44 64 -20 
            LINE N 64 -32 0 -32 
            LINE N 464 -544 528 -544 
            LINE N 464 -416 528 -416 
            LINE N 464 -288 528 -288 
            RECTANGLE N 464 -172 528 -148 
            LINE N 464 -160 528 -160 
            RECTANGLE N 464 -44 528 -20 
            LINE N 464 -32 528 -32 
            RECTANGLE N 64 -576 464 64 
        END BLOCKDEF
        BEGIN BLOCK XLXI_304 clkdlle
            PIN CLKFB XLXN_786
            PIN CLKIN CLK60
            PIN RST XLXN_851
            PIN CLK0
            PIN CLK180
            PIN CLK270
            PIN CLK2X XLXN_786
            PIN CLK2X180
            PIN CLK90
            PIN CLKDV clk_30
            PIN LOCKED XLXN_780
        END BLOCK
        BEGIN BLOCK XLXI_320 gnd
            PIN G XLXN_851
        END BLOCK
        BEGIN BLOCK XLXI_306 inv
            PIN I XLXN_780
            PIN O XLXN_781
        END BLOCK
        BEGIN BLOCK XLXI_305 clkdlle
            BEGIN ATTR CLKDV_DIVIDE 1.5
                VERILOG all:0 dp:1nosynth wsynop:1 wsynth:1
                VHDL all:0 gm:1nosynth wa:1 wd:1
                VALUETYPE Float
            END ATTR
            PIN CLKFB XLXN_790
            PIN CLKIN XLXN_786
            PIN RST XLXN_781
            PIN CLK0 XLXN_790
            PIN CLK180
            PIN CLK270
            PIN CLK2X
            PIN CLK2X180
            PIN CLK90
            PIN CLKDV clk_80
            PIN LOCKED XLXN_1004
        END BLOCK
        BEGIN BLOCK XLXI_67 gen_reset
            PIN locked XLXN_1004
            PIN clk clk_80
            PIN reset reset
        END BLOCK
        BEGIN BLOCK XLXI_321 dram_ctrl
            PIN req1 XLXN_855
            PIN we1 wr_we
            PIN req2 XLXN_1529
            PIN clk clk_80
            PIN reset reset
            PIN req_r XLXN_869
            PIN addr1(23:0) wr_addr(23:0)
            PIN idata1(31:0) wr_data(31:0)
            PIN addr2(23:0) vga_addr(23:0)
            PIN dram_dq(31:0) dram_dq(31:0)
            PIN ack1 wr_ack
            PIN ack2 XLXN_854
            PIN dram_t dram_t
            PIN dram_we dram_we
            PIN dram_ras dram_ras
            PIN dram_cas dram_cas
            PIN ack_r XLXN_868
            PIN odata1(31:0) rd_data(31:0)
            PIN odata2(31:0) vga_data(31:0)
            PIN dram_di(31:0) dram_di(31:0)
            PIN dram_a(11:0) dram_a(11:0)
            PIN wb_stb dram_wb_stb
            PIN wb_we dram_wb_we
            PIN wb_addr(22:0) dram_wb_addr(22:0)
            PIN wb_idata(31:0) dram_wb_idata(31:0)
            PIN wb_ack dram_wb_ack
            PIN wb_odata(31:0) dram_wb_odata(31:0)
        END BLOCK
        BEGIN BLOCK XLXI_285 vga_sync_gen
            PIN clk clk_80
            PIN reset reset
            PIN hsync vga_hsync
            PIN vsync vga_vsync
            PIN active XLXN_1986
            PIN load XLXN_839
            PIN next_addr XLXN_1062
            PIN reset_addr XLXN_1063
            PIN x(10:0) x(10:0)
            PIN y(10:0) y(10:0)
        END BLOCK
        BEGIN BLOCK XLXI_315 and2
            PIN I0 int2_dat(15)
            PIN I1 XLXN_1986
            PIN O vga_r
        END BLOCK
        BEGIN BLOCK XLXI_316 and2
            PIN I0 int2_dat(15)
            PIN I1 XLXN_1986
            PIN O vga_g
        END BLOCK
        BEGIN BLOCK XLXI_317 and2
            PIN I0 int2_dat(15)
            PIN I1 XLXN_1986
            PIN O vga_b
        END BLOCK
        BEGIN BLOCK XLXI_311 vga_addr_ctrl
            PIN clk clk_80
            PIN reset reset
            PIN next_addr XLXN_1062
            PIN reset_addr XLXN_1063
            PIN ack XLXN_854
            PIN req XLXN_1529
            PIN addr(23:0) vga_addr(23:0)
        END BLOCK
        BEGIN BLOCK XLXI_312 sr16cle
            PIN C clk_80
            PIN CE XLXN_1986
            PIN CLR vcc_n
            PIN D(15:0) vga_data(15:0)
            PIN L XLXN_839
            PIN SLI vcc_n
            PIN Q(15:0) int_dat(15:0)
        END BLOCK
        BEGIN BLOCK XLXI_314 sr16cle
            PIN C clk_80
            PIN CE XLXN_1986
            PIN CLR vcc_n
            PIN D(15:0) vga_data(31:16)
            PIN L XLXN_839
            PIN SLI int_dat(15)
            PIN Q(15:0) int2_dat(15:0)
        END BLOCK
        BEGIN BLOCK XLXI_318 gnd
            PIN G vcc_n
        END BLOCK
        BEGIN BLOCK XLXI_580 gen_reset
            PIN locked XLXN_780
            PIN clk clk_30
            PIN reset reset_30
        END BLOCK
        BEGIN BLOCK XLXI_336 vcc
            PIN P XLXN_866
        END BLOCK
        BEGIN BLOCK XLXI_334 fdce
            PIN C clk_80
            PIN CE refr
            PIN CLR XLXN_868
            PIN D XLXN_866
            PIN Q XLXN_869
        END BLOCK
        BEGIN BLOCK XLXI_331 cb8ce
            PIN C clk_80
            PIN CE XLXN_862
            PIN CLR reset
            PIN CEO refr
            PIN Q(7:0)
            PIN TC
        END BLOCK
        BEGIN BLOCK XLXI_332 vcc
            PIN P XLXN_862
        END BLOCK
        BEGIN BLOCK XLXI_574 sys_ctrl
            PIN rx_rdy XLXN_2163
            PIN tx_empty tx_fifo_empty
            PIN spim_ack XLXN_2161
            PIN clk clk_30
            PIN reset reset_30
            PIN rx_data(7:0) XLXN_2162(7:0)
            PIN spim_idata(7:0) XLXN_2156(7:0)
            PIN rx_rd XLXN_2164
            PIN tx_stb XLXN_2173
            PIN spim_stb XLXN_2160
            PIN spim_we XLXN_2159
            PIN tx_data(7:0) XLXN_2174(7:0)
            PIN spim_addr(7:0) XLXN_2158(7:0)
            PIN spim_odata(7:0) XLXN_2157(7:0)
            PIN dram_ack dram_wb_ack
            PIN dram_idata(31:0) dram_wb_odata(31:0)
            PIN dram_stb dram_wb_stb
            PIN dram_we dram_wb_we
            PIN dram_addr(22:0) dram_wb_addr(22:0)
            PIN dram_odata(31:0) dram_wb_idata(31:0)
        END BLOCK
        BEGIN BLOCK XLXI_550 RxUnit
            PIN Clk clk_30
            PIN Reset reset_30
            PIN Enable XLXN_1987
            PIN RxD uart_rxd
            PIN RD XLXN_2164
            PIN FErr
            PIN OErr
            PIN DRdy XLXN_2163
            PIN DataIn(7:0) XLXN_2162(7:0)
        END BLOCK
        BEGIN BLOCK XLXI_551 ClkUnit
            PIN SysClk clk_30
            PIN Reset reset_30
            PIN EnableRx XLXN_1987
            PIN EnableTx tx_enable
        END BLOCK
        BEGIN BLOCK XLXI_553 spiMaster
            PIN clk_i clk_30
            PIN rst_i reset_30
            PIN strobe_i XLXN_2160
            PIN we_i XLXN_2159
            PIN spiSysClk clk_30
            PIN spiDataIn sd_di
            PIN address_i(7:0) XLXN_2158(7:0)
            PIN data_i(7:0) XLXN_2157(7:0)
            PIN ack_o XLXN_2161
            PIN spiClkOut sd_clk
            PIN spiDataOut sd_do
            PIN spiCS_n sd_cs
            PIN data_o(7:0) XLXN_2156(7:0)
        END BLOCK
        BEGIN BLOCK XLXI_552 TxUnit
            PIN Clk clk_30
            PIN Reset reset_30
            PIN Enable tx_enable
            PIN Load XLXN_2169
            PIN DataO(7:0) XLXN_2165(7:0)
            PIN TxD uart_txd
            PIN TRegE
            PIN TBufE XLXN_2181
        END BLOCK
        BEGIN BLOCK XLXI_582 tx_fifo_ctrl
            PIN clk clk_30
            PIN reset reset_30
            PIN fifo_empty tx_fifo_empty
            PIN tx_buf_empty XLXN_2181
            PIN fifo_rd XLXN_2168
            PIN tx_load XLXN_2169
        END BLOCK
        BEGIN BLOCK XLXI_577 wrdata_fifo
            PIN din(7:0) XLXN_2174(7:0)
            PIN wr_en XLXN_2173
            PIN rd_en XLXN_2168
            PIN clk clk_30
            PIN rst reset_30
            PIN dout(7:0) XLXN_2165(7:0)
            PIN full
            PIN empty tx_fifo_empty
        END BLOCK
        BEGIN BLOCK XLXI_583 spi_emu
            PIN clk clk_80
            PIN reset reset
            PIN trigger mem_wr
            PIN spi_cs spi_cs
            PIN spi_clk spi_clk
            PIN spi_si spi_si
            PIN spi_so_sniffer spi_so
            PIN dram_ack wr_ack
            PIN dram_idata(31:0) rd_data(31:0)
            PIN spi_so spi_so_emu
            PIN dram_req XLXN_855
            PIN dram_we wr_we
            PIN enable XLXN_2233
            PIN dram_addr(23:0) wr_addr(23:0)
            PIN dram_odata(31:0) wr_data(31:0)
        END BLOCK
        BEGIN BLOCK XLXI_260 buf
            PIN I XLXN_2233
            PIN O capture_active
        END BLOCK
    END NETLIST
    BEGIN SHEET 1 7040 5440
        BEGIN BRANCH CLK60
            WIRE 208 304 256 304
        END BRANCH
        INSTANCE XLXI_304 256 816 R0
        BEGIN BRANCH XLXN_780
            WIRE 176 768 672 768
            WIRE 176 768 176 1312
            WIRE 176 1312 368 1312
            WIRE 640 688 672 688
            WIRE 672 688 720 688
            WIRE 672 688 672 768
        END BRANCH
        BEGIN BRANCH XLXN_781
            WIRE 944 688 960 688
        END BRANCH
        BEGIN BRANCH XLXN_786
            WIRE 240 64 240 368
            WIRE 240 368 256 368
            WIRE 240 64 672 64
            WIRE 672 64 672 304
            WIRE 672 304 672 496
            WIRE 672 304 960 304
            WIRE 640 496 672 496
        END BRANCH
        BEGIN BRANCH XLXN_851
            WIRE 128 688 256 688
            WIRE 128 688 128 704
        END BRANCH
        INSTANCE XLXI_320 64 832 R0
        BEGIN BRANCH clk_80
            WIRE 1344 624 1664 624
            WIRE 1664 624 1696 624
            BEGIN DISPLAY 1664 624 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN INSTANCE XLXI_305 960 816 R0
            BEGIN DISPLAY 80 -44 ATTR CLKDV_DIVIDE
                FONT 28 "Arial"
                DISPLAYFORMAT NAMEEQUALSVALUE
            END DISPLAY
        END INSTANCE
        BEGIN INSTANCE XLXI_67 368 944 R0
        END INSTANCE
        BEGIN BRANCH clk_80
            WIRE 352 912 368 912
            BEGIN DISPLAY 352 912 ATTR Name
                ALIGNMENT SOFT-RIGHT
            END DISPLAY
        END BRANCH
        BEGIN BRANCH XLXN_1004
            WIRE 192 800 1360 800
            WIRE 192 800 192 976
            WIRE 192 976 368 976
            WIRE 1344 688 1360 688
            WIRE 1360 688 1360 800
        END BRANCH
        IOMARKER 208 304 CLK60 R180 28
        BEGIN INSTANCE XLXI_321 3120 1856 R0
        END INSTANCE
        BEGIN BRANCH reset
            WIRE 2976 1504 2992 1504
            WIRE 2992 1504 3120 1504
            BEGIN DISPLAY 2992 1504 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH vga_data(31:0)
            WIRE 3584 1696 3680 1696
            WIRE 3680 1696 3744 1696
            BEGIN DISPLAY 3680 1696 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH vga_addr(23:0)
            WIRE 2944 1696 2960 1696
            WIRE 2960 1696 3120 1696
            BEGIN DISPLAY 2960 1696 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_dq(31:0)
            WIRE 3040 1760 3120 1760
        END BRANCH
        BEGIN BRANCH dram_a(11:0)
            WIRE 3584 1824 3680 1824
        END BRANCH
        BEGIN BRANCH dram_di(31:0)
            WIRE 3584 1760 3680 1760
        END BRANCH
        BEGIN BRANCH dram_cas
            WIRE 3584 1568 3680 1568
        END BRANCH
        BEGIN BRANCH dram_ras
            WIRE 3584 1504 3680 1504
        END BRANCH
        BEGIN BRANCH dram_we
            WIRE 3584 1440 3680 1440
        END BRANCH
        BEGIN BRANCH dram_t
            WIRE 3584 1376 3680 1376
        END BRANCH
        BEGIN BRANCH XLXN_869
            WIRE 2864 1888 3120 1888
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 2976 1440 2992 1440
            WIRE 2992 1440 3120 1440
            BEGIN DISPLAY 2992 1440 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH wr_addr(23:0)
            WIRE 2992 1568 3008 1568
            WIRE 3008 1568 3120 1568
            BEGIN DISPLAY 3008 1568 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH wr_data(31:0)
            WIRE 2704 1632 2736 1632
            WIRE 2736 1632 3120 1632
            BEGIN DISPLAY 2736 1632 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH refr
            WIRE 2464 1568 2800 1568
            WIRE 2464 1568 2464 1952
            WIRE 2464 1952 2480 1952
            WIRE 2720 1344 2800 1344
            WIRE 2800 1344 2800 1568
        END BRANCH
        BEGIN BRANCH XLXN_855
            WIRE 2848 2624 3952 2624
            WIRE 3088 1104 3088 1248
            WIRE 3088 1248 3120 1248
            WIRE 3088 1104 3952 1104
            WIRE 3952 1104 3952 2624
        END BRANCH
        BEGIN BRANCH XLXN_1529
            WIRE 3104 1136 3104 1376
            WIRE 3104 1376 3120 1376
            WIRE 3104 1136 4144 1136
            WIRE 4064 656 4144 656
            WIRE 4144 656 4144 1136
        END BRANCH
        BEGIN BRANCH XLXN_854
            WIRE 3584 1312 3632 1312
            WIRE 3632 848 3632 1312
            WIRE 3632 848 3680 848
        END BRANCH
        BEGIN BRANCH vga_b
            WIRE 4112 432 4160 432
        END BRANCH
        BEGIN BRANCH vga_hsync
            WIRE 3200 144 3568 144
        END BRANCH
        BEGIN BRANCH x(10:0)
            WIRE 3200 336 3312 336
            WIRE 3312 336 3328 336
            BEGIN DISPLAY 3312 336 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH y(10:0)
            WIRE 3200 720 3296 720
            WIRE 3296 720 3312 720
            BEGIN DISPLAY 3296 720 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset
            WIRE 2752 464 2768 464
            WIRE 2768 464 2816 464
            BEGIN DISPLAY 2768 464 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 2720 144 2768 144
            WIRE 2768 144 2816 144
            BEGIN DISPLAY 2768 144 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN INSTANCE XLXI_285 2816 432 R0
        END INSTANCE
        BEGIN BRANCH vga_vsync
            WIRE 3200 208 3568 208
        END BRANCH
        BEGIN BRANCH XLXN_1062
            WIRE 3200 592 3488 592
            WIRE 3488 592 3488 976
            WIRE 3488 976 3680 976
        END BRANCH
        INSTANCE XLXI_315 3856 272 R0
        BEGIN BRANCH vga_r
            WIRE 4112 176 4160 176
        END BRANCH
        BEGIN BRANCH vga_g
            WIRE 4112 304 4160 304
        END BRANCH
        BEGIN BRANCH int2_dat(15)
            WIRE 3552 464 3584 464
            WIRE 3584 464 3840 464
            WIRE 3840 464 3856 464
            WIRE 3840 208 3856 208
            WIRE 3840 208 3840 336
            WIRE 3840 336 3840 464
            WIRE 3840 336 3856 336
            BEGIN DISPLAY 3584 464 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        INSTANCE XLXI_316 3856 400 R0
        INSTANCE XLXI_317 3856 528 R0
        BEGIN BRANCH vga_addr(23:0)
            WIRE 4064 848 4160 848
            WIRE 4160 848 4224 848
            BEGIN DISPLAY 4160 848 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset
            WIRE 3568 912 3600 912
            WIRE 3600 912 3680 912
            BEGIN DISPLAY 3600 912 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 3552 656 3584 656
            WIRE 3584 656 3680 656
            BEGIN DISPLAY 3584 656 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN INSTANCE XLXI_311 3680 880 R0
        END INSTANCE
        BEGIN BRANCH XLXN_1063
            WIRE 3200 656 3424 656
            WIRE 3424 656 3424 1040
            WIRE 3424 1040 3680 1040
        END BRANCH
        INSTANCE XLXI_314 4304 2528 R0
        BEGIN BRANCH int_dat(15:0)
            WIRE 4704 1440 4752 1440
            WIRE 4752 1440 4784 1440
            BEGIN DISPLAY 4752 1440 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH int_dat(15)
            WIRE 4256 1952 4272 1952
            WIRE 4272 1952 4304 1952
            BEGIN DISPLAY 4272 1952 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH int2_dat(15:0)
            WIRE 4688 2144 4720 2144
            WIRE 4720 2144 4768 2144
            BEGIN DISPLAY 4720 2144 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH vga_data(15:0)
            WIRE 3984 1312 4016 1312
            WIRE 4016 1312 4320 1312
            BEGIN DISPLAY 4016 1312 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH vga_data(31:16)
            WIRE 4032 2016 4064 2016
            WIRE 4064 2016 4304 2016
            BEGIN DISPLAY 4064 2016 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        INSTANCE XLXI_318 4016 1632 R0
        BEGIN BRANCH vcc_n
            WIRE 4080 1440 4080 1504
            WIRE 4080 1440 4176 1440
            WIRE 4176 1440 4176 1792
            WIRE 4176 1792 4176 2496
            WIRE 4176 2496 4304 2496
            WIRE 4176 1792 4320 1792
            WIRE 4176 1248 4320 1248
            WIRE 4176 1248 4176 1440
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 4112 2400 4128 2400
            WIRE 4128 2400 4304 2400
            BEGIN DISPLAY 4128 2400 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 4096 1696 4112 1696
            WIRE 4112 1696 4320 1696
            BEGIN DISPLAY 4112 1696 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH XLXN_1986
            WIRE 3200 272 3808 272
            WIRE 3808 272 3856 272
            WIRE 3808 272 3808 400
            WIRE 3808 400 3856 400
            WIRE 3808 400 3808 512
            WIRE 3808 512 4320 512
            WIRE 4320 512 4320 1040
            WIRE 3808 144 3856 144
            WIRE 3808 144 3808 272
            WIRE 4208 1040 4208 1632
            WIRE 4208 1632 4208 2336
            WIRE 4208 2336 4304 2336
            WIRE 4208 1632 4320 1632
            WIRE 4208 1040 4320 1040
        END BRANCH
        BEGIN BRANCH XLXN_839
            WIRE 3200 528 4384 528
            WIRE 4384 528 4384 1088
            WIRE 4240 1088 4240 1504
            WIRE 4240 1504 4240 2208
            WIRE 4240 2208 4304 2208
            WIRE 4240 1504 4320 1504
            WIRE 4240 1088 4384 1088
        END BRANCH
        IOMARKER 3680 1376 dram_t R0 28
        IOMARKER 3680 1440 dram_we R0 28
        IOMARKER 3680 1504 dram_ras R0 28
        IOMARKER 3680 1568 dram_cas R0 28
        IOMARKER 3680 1760 dram_di(31:0) R0 28
        IOMARKER 3680 1824 dram_a(11:0) R0 28
        IOMARKER 3040 1760 dram_dq(31:0) R180 28
        IOMARKER 3568 144 vga_hsync R0 28
        IOMARKER 3568 208 vga_vsync R0 28
        IOMARKER 4160 176 vga_r R0 28
        IOMARKER 4160 304 vga_g R0 28
        IOMARKER 4160 432 vga_b R0 28
        BEGIN BRANCH clk_30
            WIRE 640 624 768 624
            WIRE 768 624 816 624
            BEGIN DISPLAY 768 624 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH XLXN_790
            WIRE 944 64 944 368
            WIRE 944 368 960 368
            WIRE 944 64 1392 64
            WIRE 1392 64 1392 240
            WIRE 1344 240 1392 240
        END BRANCH
        BEGIN INSTANCE XLXI_580 368 1280 R0
        END INSTANCE
        BEGIN BRANCH clk_30
            WIRE 352 1248 368 1248
            BEGIN DISPLAY 352 1248 ATTR Name
                ALIGNMENT SOFT-RIGHT
            END DISPLAY
        END BRANCH
        INSTANCE XLXI_306 720 720 R0
        BEGIN BRANCH reset_30
            WIRE 752 1248 1328 1248
            WIRE 1328 1248 1344 1248
            BEGIN DISPLAY 1328 1248 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        INSTANCE XLXI_312 4320 1824 R0
        BEGIN BRANCH XLXN_866
            WIRE 2384 1840 2384 1888
            WIRE 2384 1888 2480 1888
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 2336 2016 2400 2016
            WIRE 2400 2016 2480 2016
            BEGIN DISPLAY 2400 2016 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        INSTANCE XLXI_336 2320 1840 R0
        INSTANCE XLXI_334 2480 2144 R0
        BEGIN BRANCH XLXN_868
            WIRE 2480 2112 2480 2208
            WIRE 2480 2208 3888 2208
            WIRE 3584 1888 3888 1888
            WIRE 3888 1888 3888 2208
        END BRANCH
        INSTANCE XLXI_331 2336 1536 R0
        BEGIN BRANCH XLXN_862
            WIRE 2224 1312 2224 1344
            WIRE 2224 1344 2336 1344
        END BRANCH
        INSTANCE XLXI_332 2160 1312 R0
        BEGIN BRANCH reset
            WIRE 2256 1504 2272 1504
            WIRE 2272 1504 2336 1504
            BEGIN DISPLAY 2272 1504 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 2304 1408 2320 1408
            WIRE 2320 1408 2336 1408
            BEGIN DISPLAY 2320 1408 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_ack
            WIRE 3584 1952 3632 1952
            WIRE 3632 1952 3728 1952
            BEGIN DISPLAY 3632 1952 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_odata(31:0)
            WIRE 3584 2016 3648 2016
            WIRE 3648 2016 3728 2016
            BEGIN DISPLAY 3648 2016 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_stb
            WIRE 2992 1952 3024 1952
            WIRE 3024 1952 3120 1952
            BEGIN DISPLAY 3024 1952 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_we
            WIRE 2992 2016 3008 2016
            WIRE 3008 2016 3120 2016
            BEGIN DISPLAY 3008 2016 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_addr(22:0)
            WIRE 2992 2080 3024 2080
            WIRE 3024 2080 3120 2080
            BEGIN DISPLAY 3024 2080 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_idata(31:0)
            WIRE 2992 2144 3024 2144
            WIRE 3024 2144 3120 2144
            BEGIN DISPLAY 3024 2144 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH XLXN_1987
            WIRE 2720 3664 3168 3664
        END BRANCH
        BEGIN BRANCH uart_rxd
            WIRE 3024 3728 3168 3728
        END BRANCH
        BEGIN INSTANCE XLXI_574 3856 3872 R0
        END INSTANCE
        BEGIN BRANCH clk_30
            WIRE 3744 3648 3760 3648
            WIRE 3760 3648 3856 3648
            BEGIN DISPLAY 3760 3648 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset_30
            WIRE 3744 3712 3760 3712
            WIRE 3760 3712 3856 3712
            BEGIN DISPLAY 3760 3712 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH XLXN_2156(7:0)
            WIRE 3616 3248 3616 3840
            WIRE 3616 3840 3856 3840
            WIRE 3616 3248 5376 3248
            WIRE 5376 3248 5376 3840
            WIRE 5312 3840 5376 3840
        END BRANCH
        BEGIN BRANCH XLXN_2157(7:0)
            WIRE 4352 3840 4864 3840
        END BRANCH
        BEGIN BRANCH XLXN_2158(7:0)
            WIRE 4352 3776 4864 3776
        END BRANCH
        BEGIN BRANCH XLXN_2159
            WIRE 4352 3648 4624 3648
            WIRE 4624 3584 4624 3648
            WIRE 4624 3584 4864 3584
        END BRANCH
        BEGIN BRANCH XLXN_2160
            WIRE 4352 3584 4544 3584
            WIRE 4544 3520 4544 3584
            WIRE 4544 3520 4864 3520
        END BRANCH
        BEGIN BRANCH XLXN_2161
            WIRE 3664 3296 3664 3584
            WIRE 3664 3584 3856 3584
            WIRE 3664 3296 5344 3296
            WIRE 5344 3296 5344 3392
            WIRE 5312 3392 5344 3392
        END BRANCH
        BEGIN BRANCH XLXN_2162(7:0)
            WIRE 3552 3776 3856 3776
        END BRANCH
        BEGIN BRANCH XLXN_2163
            WIRE 3552 3696 3584 3696
            WIRE 3584 3456 3584 3696
            WIRE 3584 3456 3856 3456
        END BRANCH
        BEGIN BRANCH XLXN_2173
            WIRE 4352 3520 4528 3520
            WIRE 4528 3520 4528 4112
            WIRE 4528 4112 4752 4112
        END BRANCH
        BEGIN BRANCH XLXN_2174(7:0)
            WIRE 4352 3712 4480 3712
            WIRE 4480 3712 4480 4048
            WIRE 4480 4048 4752 4048
        END BRANCH
        BEGIN BRANCH clk_30
            WIRE 3056 3536 3120 3536
            WIRE 3120 3536 3168 3536
            BEGIN DISPLAY 3120 3536 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset_30
            WIRE 3056 3600 3120 3600
            WIRE 3120 3600 3168 3600
            BEGIN DISPLAY 3120 3600 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN INSTANCE XLXI_550 3168 3824 R0
        END INSTANCE
        BEGIN BRANCH XLXN_2164
            WIRE 3088 3344 3088 3792
            WIRE 3088 3792 3168 3792
            WIRE 3088 3344 4368 3344
            WIRE 4368 3344 4368 3456
            WIRE 4352 3456 4368 3456
        END BRANCH
        BEGIN INSTANCE XLXI_551 2336 3760 R0
        END INSTANCE
        BEGIN BRANCH clk_30
            WIRE 2272 3664 2288 3664
            WIRE 2288 3664 2336 3664
            BEGIN DISPLAY 2288 3664 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset_30
            WIRE 2272 3728 2288 3728
            WIRE 2288 3728 2336 3728
            BEGIN DISPLAY 2288 3728 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN INSTANCE XLXI_553 4864 3872 R0
        END INSTANCE
        BEGIN BRANCH sd_clk
            WIRE 5312 3504 5440 3504
        END BRANCH
        BEGIN BRANCH sd_do
            WIRE 5312 3616 5440 3616
        END BRANCH
        BEGIN BRANCH sd_di
            WIRE 4784 3712 4864 3712
        END BRANCH
        BEGIN BRANCH sd_cs
            WIRE 5312 3728 5440 3728
        END BRANCH
        BEGIN BRANCH clk_30
            WIRE 4672 3392 4704 3392
            WIRE 4704 3392 4864 3392
            BEGIN DISPLAY 4704 3392 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset_30
            WIRE 4672 3456 4704 3456
            WIRE 4704 3456 4864 3456
            BEGIN DISPLAY 4704 3456 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH clk_30
            WIRE 4672 3648 4704 3648
            WIRE 4704 3648 4864 3648
            BEGIN DISPLAY 4704 3648 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        IOMARKER 5440 3504 sd_clk R0 28
        IOMARKER 5440 3616 sd_do R0 28
        IOMARKER 5440 3728 sd_cs R0 28
        BEGIN BRANCH tx_enable
            WIRE 2720 3728 2752 3728
            WIRE 2752 3728 2800 3728
            BEGIN DISPLAY 2752 3728 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH tx_fifo_empty
            WIRE 3744 3520 3760 3520
            WIRE 3760 3520 3856 3520
            BEGIN DISPLAY 3760 3520 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        IOMARKER 3024 3728 uart_rxd R180 28
        IOMARKER 4784 3712 sd_di R180 28
        BEGIN BRANCH uart_txd
            WIRE 6128 3984 6256 3984
        END BRANCH
        BEGIN INSTANCE XLXI_552 5744 4272 R0
        END INSTANCE
        BEGIN BRANCH clk_30
            WIRE 5648 3984 5664 3984
            WIRE 5664 3984 5744 3984
            BEGIN DISPLAY 5664 3984 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset_30
            WIRE 5648 4048 5664 4048
            WIRE 5664 4048 5744 4048
            BEGIN DISPLAY 5664 4048 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH XLXN_2165(7:0)
            WIRE 5328 4048 5520 4048
            WIRE 5520 4048 5520 4240
            WIRE 5520 4240 5744 4240
        END BRANCH
        BEGIN BRANCH clk_30
            WIRE 5584 4448 5616 4448
            WIRE 5616 4448 5744 4448
            BEGIN DISPLAY 5616 4448 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH reset_30
            WIRE 5584 4512 5616 4512
            WIRE 5616 4512 5744 4512
            BEGIN DISPLAY 5616 4512 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH XLXN_2169
            WIRE 5680 4176 5680 4304
            WIRE 5680 4304 6224 4304
            WIRE 6224 4304 6224 4640
            WIRE 5680 4176 5744 4176
            WIRE 6128 4640 6224 4640
        END BRANCH
        BEGIN BRANCH reset_30
            WIRE 4544 4688 4592 4688
            WIRE 4592 4688 4896 4688
            WIRE 4896 4672 4896 4688
            BEGIN DISPLAY 4592 4688 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH tx_enable
            WIRE 5600 4112 5664 4112
            WIRE 5664 4112 5744 4112
            BEGIN DISPLAY 5664 4112 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH tx_fifo_empty
            WIRE 5328 4400 5392 4400
            WIRE 5392 4400 5440 4400
            WIRE 5440 4400 5472 4400
            WIRE 5392 4400 5392 4576
            WIRE 5392 4576 5744 4576
            BEGIN DISPLAY 5440 4400 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN INSTANCE XLXI_582 5744 4672 R0
        END INSTANCE
        BEGIN BRANCH XLXN_2181
            WIRE 5680 4336 5680 4640
            WIRE 5680 4640 5744 4640
            WIRE 5680 4336 6144 4336
            WIRE 6128 4240 6144 4240
            WIRE 6144 4240 6144 4336
        END BRANCH
        BEGIN INSTANCE XLXI_577 4752 3968 R0
        END INSTANCE
        BEGIN BRANCH XLXN_2168
            WIRE 4672 4208 4752 4208
            WIRE 4672 4208 4672 4736
            WIRE 4672 4736 6144 4736
            WIRE 6128 4448 6144 4448
            WIRE 6144 4448 6144 4736
        END BRANCH
        BEGIN BRANCH clk_30
            WIRE 4544 4336 4592 4336
            WIRE 4592 4336 4752 4336
            BEGIN DISPLAY 4592 4336 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        IOMARKER 6256 3984 uart_txd R0 28
        BEGIN BRANCH dram_wb_ack
            WIRE 3680 3904 3712 3904
            WIRE 3712 3904 3856 3904
            BEGIN DISPLAY 3712 3904 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_odata(31:0)
            WIRE 3680 3968 3696 3968
            WIRE 3696 3968 3856 3968
            BEGIN DISPLAY 3696 3968 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_stb
            WIRE 4352 3904 4400 3904
            WIRE 4400 3904 4448 3904
            BEGIN DISPLAY 4400 3904 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_we
            WIRE 4352 3968 4400 3968
            WIRE 4400 3968 4448 3968
            BEGIN DISPLAY 4400 3968 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_addr(22:0)
            WIRE 4352 4032 4384 4032
            WIRE 4384 4032 4448 4032
            BEGIN DISPLAY 4384 4032 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH dram_wb_idata(31:0)
            WIRE 4352 4096 4400 4096
            WIRE 4400 4096 4448 4096
            BEGIN DISPLAY 4400 4096 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN INSTANCE XLXI_583 2320 3040 R0
        END INSTANCE
        BEGIN BRANCH reset
            WIRE 2240 2560 2256 2560
            WIRE 2256 2560 2320 2560
            BEGIN DISPLAY 2256 2560 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH clk_80
            WIRE 2240 2496 2256 2496
            WIRE 2256 2496 2320 2496
            BEGIN DISPLAY 2256 2496 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH mem_wr
            WIRE 1984 2624 2320 2624
        END BRANCH
        IOMARKER 1984 2624 mem_wr R180 28
        BEGIN BRANCH spi_cs
            WIRE 1984 2688 2256 2688
            WIRE 2256 2688 2320 2688
            BEGIN DISPLAY 2256 2688 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH spi_si
            WIRE 1984 2816 2256 2816
            WIRE 2256 2816 2320 2816
            BEGIN DISPLAY 2256 2816 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH spi_clk
            WIRE 1984 2752 2256 2752
            WIRE 2256 2752 2320 2752
            BEGIN DISPLAY 2256 2752 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH spi_so
            WIRE 1984 2880 2256 2880
            WIRE 2256 2880 2320 2880
            BEGIN DISPLAY 2256 2880 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        IOMARKER 1984 2688 spi_cs R180 28
        IOMARKER 1984 2752 spi_clk R180 28
        IOMARKER 1984 2816 spi_si R180 28
        IOMARKER 1984 2880 spi_so R180 28
        BEGIN BRANCH wr_addr(23:0)
            WIRE 2848 2880 2944 2880
            WIRE 2944 2880 2992 2880
            BEGIN DISPLAY 2944 2880 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH capture_active
            WIRE 3200 3072 3296 3072
        END BRANCH
        INSTANCE XLXI_260 2976 3104 R0
        IOMARKER 3296 3072 capture_active R0 28
        BEGIN BRANCH XLXN_2233
            WIRE 2848 3072 2976 3072
        END BRANCH
        BEGIN BRANCH wr_ack
            WIRE 2144 2272 3920 2272
            WIRE 2144 2272 2144 2944
            WIRE 2144 2944 2192 2944
            WIRE 2192 2944 2320 2944
            WIRE 3584 1248 3920 1248
            WIRE 3920 1248 3920 2272
            BEGIN DISPLAY 2192 2944 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH wr_data(31:0)
            WIRE 2848 3008 2912 3008
            WIRE 2912 3008 2992 3008
            BEGIN DISPLAY 2912 3008 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH rd_data(31:0)
            WIRE 3584 1632 3696 1632
            WIRE 3696 1632 3744 1632
            BEGIN DISPLAY 3696 1632 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH rd_data(31:0)
            WIRE 2160 3008 2192 3008
            WIRE 2192 3008 2320 3008
            BEGIN DISPLAY 2192 3008 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH wr_we
            WIRE 2912 1312 2960 1312
            WIRE 2960 1312 3120 1312
            BEGIN DISPLAY 2960 1312 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH wr_we
            WIRE 2848 2752 2912 2752
            WIRE 2912 2752 2992 2752
            BEGIN DISPLAY 2912 2752 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
        BEGIN BRANCH spi_so_emu
            WIRE 2848 2496 3008 2496
        END BRANCH
        IOMARKER 3008 2496 spi_so_emu R0 28
        BEGIN BRANCH reset
            WIRE 752 912 880 912
            WIRE 880 912 1328 912
            WIRE 1328 912 1360 912
            BEGIN DISPLAY 1328 912 ATTR Name
                ALIGNMENT SOFT-BCENTER
            END DISPLAY
        END BRANCH
    END SHEET
END SCHEMATIC
