////////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995-2008 Xilinx, Inc.  All rights reserved.
////////////////////////////////////////////////////////////////////////////////
//   ____  ____ 
//  /   /\/   / 
// /___/  \  /    Vendor: Xilinx 
// \   \   \/     Version : 10.1
//  \   \         Application : sch2verilog
//  /   /         Filename : super_top.vf
// /___/   /\     Timestamp : 04/21/2008 00:25:27
// \   \  /  \ 
//  \___\/\___\ 
//
//Command: C:\xilinx\10.1\ISE\bin\nt\unwrapped\sch2verilog.exe -intstyle ise -family virtexe -w C:/xilinx/vga/super_top.sch super_top.vf
//Design Name: super_top
//Device: virtexe
//Purpose:
//    This verilog netlist is translated from an ECS schematic.It can be 
//    synthesized and simulated, but it should not be modified. 
//
`timescale 1ns / 1ps

module super_top(CLK25, 
                 CLK60, 
                 ir_in, 
                 PIN_J1_20, 
                 PIN_J1_22, 
                 PIN_J1_24, 
                 PIN_J1_26, 
                 PIN_SW2, 
                 rx1, 
                 rx2, 
                 SD_DI, 
                 PIN_DRAM_A0, 
                 PIN_DRAM_A1, 
                 PIN_DRAM_A2, 
                 PIN_DRAM_A3, 
                 PIN_DRAM_A4, 
                 PIN_DRAM_A5, 
                 PIN_DRAM_A6, 
                 PIN_DRAM_A7, 
                 PIN_DRAM_A8, 
                 PIN_DRAM_A9, 
                 PIN_DRAM_A10, 
                 PIN_DRAM_A11, 
                 PIN_DRAM_A12, 
                 PIN_DRAM_CAS0, 
                 PIN_DRAM_CAS1, 
                 PIN_DRAM_CAS2, 
                 PIN_DRAM_CAS3, 
                 PIN_DRAM_RAS0, 
                 PIN_DRAM_RAS1, 
                 PIN_DRAM_WE, 
                 PIN_D3, 
                 PIN_EEPROM_A0, 
                 PIN_EEPROM_A1, 
                 PIN_EEPROM_A2, 
                 PIN_EEPROM_SCL, 
                 PIN_EEPROM_SDA, 
                 PIN_EEPROM_WP, 
                 PIN_JP6, 
                 PIN_JP9_1, 
                 PIN_JP9_3, 
                 PIN_JP9_5, 
                 PIN_J1_10, 
                 PIN_J1_12, 
                 PIN_J1_14, 
                 PIN_J1_16, 
                 PIN_J1_18, 
                 PIN_TP16, 
                 PIN_TP17, 
                 PIN_TP18, 
                 SD_CLK, 
                 SD_CS, 
                 SD_DO, 
                 tx1, 
                 tx2, 
                 VGA_B, 
                 VGA_G, 
                 VGA_HS, 
                 VGA_R, 
                 VGA_VS, 
                 DRAM_DQ0, 
                 DRAM_DQ1, 
                 DRAM_DQ2, 
                 DRAM_DQ3, 
                 DRAM_DQ4, 
                 DRAM_DQ5, 
                 DRAM_DQ6, 
                 DRAM_DQ7, 
                 DRAM_DQ8, 
                 DRAM_DQ9, 
                 DRAM_DQ10, 
                 DRAM_DQ11, 
                 DRAM_DQ12, 
                 DRAM_DQ13, 
                 DRAM_DQ14, 
                 DRAM_DQ15, 
                 DRAM_DQ16, 
                 DRAM_DQ17, 
                 DRAM_DQ18, 
                 DRAM_DQ19, 
                 DRAM_DQ20, 
                 DRAM_DQ21, 
                 DRAM_DQ22, 
                 DRAM_DQ23, 
                 DRAM_DQ24, 
                 DRAM_DQ25, 
                 DRAM_DQ26, 
                 DRAM_DQ27, 
                 DRAM_DQ28, 
                 DRAM_DQ29, 
                 DRAM_DQ30, 
                 DRAM_DQ31);

    input CLK25;
    input CLK60;
    input ir_in;
    input PIN_J1_20;
    input PIN_J1_22;
    input PIN_J1_24;
    input PIN_J1_26;
    input PIN_SW2;
    input rx1;
    input rx2;
    input SD_DI;
   output PIN_DRAM_A0;
   output PIN_DRAM_A1;
   output PIN_DRAM_A2;
   output PIN_DRAM_A3;
   output PIN_DRAM_A4;
   output PIN_DRAM_A5;
   output PIN_DRAM_A6;
   output PIN_DRAM_A7;
   output PIN_DRAM_A8;
   output PIN_DRAM_A9;
   output PIN_DRAM_A10;
   output PIN_DRAM_A11;
   output PIN_DRAM_A12;
   output PIN_DRAM_CAS0;
   output PIN_DRAM_CAS1;
   output PIN_DRAM_CAS2;
   output PIN_DRAM_CAS3;
   output PIN_DRAM_RAS0;
   output PIN_DRAM_RAS1;
   output PIN_DRAM_WE;
   output PIN_D3;
   output PIN_EEPROM_A0;
   output PIN_EEPROM_A1;
   output PIN_EEPROM_A2;
   output PIN_EEPROM_SCL;
   output PIN_EEPROM_SDA;
   output PIN_EEPROM_WP;
   output PIN_JP6;
   output PIN_JP9_1;
   output PIN_JP9_3;
   output PIN_JP9_5;
   output PIN_J1_10;
   output PIN_J1_12;
   output PIN_J1_14;
   output PIN_J1_16;
   output PIN_J1_18;
   output PIN_TP16;
   output PIN_TP17;
   output PIN_TP18;
   output SD_CLK;
   output SD_CS;
   output SD_DO;
   output tx1;
   output tx2;
   output VGA_B;
   output VGA_G;
   output VGA_HS;
   output VGA_R;
   output VGA_VS;
    inout DRAM_DQ0;
    inout DRAM_DQ1;
    inout DRAM_DQ2;
    inout DRAM_DQ3;
    inout DRAM_DQ4;
    inout DRAM_DQ5;
    inout DRAM_DQ6;
    inout DRAM_DQ7;
    inout DRAM_DQ8;
    inout DRAM_DQ9;
    inout DRAM_DQ10;
    inout DRAM_DQ11;
    inout DRAM_DQ12;
    inout DRAM_DQ13;
    inout DRAM_DQ14;
    inout DRAM_DQ15;
    inout DRAM_DQ16;
    inout DRAM_DQ17;
    inout DRAM_DQ18;
    inout DRAM_DQ19;
    inout DRAM_DQ20;
    inout DRAM_DQ21;
    inout DRAM_DQ22;
    inout DRAM_DQ23;
    inout DRAM_DQ24;
    inout DRAM_DQ25;
    inout DRAM_DQ26;
    inout DRAM_DQ27;
    inout DRAM_DQ28;
    inout DRAM_DQ29;
    inout DRAM_DQ30;
    inout DRAM_DQ31;
   
   wire cnt15;
   wire [11:0] DRAM_A;
   wire DRAM_CAS;
   wire [31:0] DRAM_I;
   wire [31:0] DRAM_O;
   wire DRAM_RAS;
   wire DRAM_T;
   wire DRAM_WE;
   wire LED;
   wire spi_clk;
   wire spi_cs;
   wire spi_si;
   wire spi_so;
   wire XLXN_285;
   wire XLXN_397;
   wire XLXN_398;
   wire XLXN_399;
   wire XLXN_400;
   wire XLXN_401;
   wire XLXN_414;
   wire XLXN_419;
   wire XLXN_420;
   wire PIN_SW2_DUMMY;
   
   assign PIN_SW2_DUMMY = PIN_SW2;
   top XLXI_1 (.CLK60(CLK60), 
               .dram_dq(DRAM_O[31:0]), 
               .mem_wr(XLXN_420), 
               .sd_di(SD_DI), 
               .spi_clk(spi_clk), 
               .spi_cs(spi_cs), 
               .spi_si(spi_si), 
               .spi_so(spi_so), 
               .uart_rxd(rx2), 
               .dram_a(DRAM_A[11:0]), 
               .dram_cas(DRAM_CAS), 
               .dram_di(DRAM_I[31:0]), 
               .dram_ras(DRAM_RAS), 
               .dram_t(DRAM_T), 
               .dram_we(DRAM_WE), 
               .oc1(cnt15), 
               .reset(LED), 
               .sd_clk(SD_CLK), 
               .sd_cs(SD_CS), 
               .sd_do(SD_DO), 
               .uart_txd(tx2), 
               .vga_b(XLXN_401), 
               .vga_g(XLXN_400), 
               .vga_hsync(XLXN_398), 
               .vga_r(XLXN_399), 
               .vga_vsync(XLXN_397));
   BUF XLXI_2 (.I(XLXN_399), 
               .O(VGA_R));
   BUF XLXI_3 (.I(XLXN_400), 
               .O(VGA_G));
   BUF XLXI_4 (.I(XLXN_401), 
               .O(VGA_B));
   BUF XLXI_5 (.I(XLXN_398), 
               .O(VGA_HS));
   BUF XLXI_6 (.I(XLXN_397), 
               .O(VGA_VS));
   IOBUF XLXI_12 (.I(DRAM_I[0]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[0]), 
                  .IO(DRAM_DQ0));
   IOBUF XLXI_36 (.I(DRAM_I[1]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[1]), 
                  .IO(DRAM_DQ1));
   IOBUF XLXI_38 (.I(DRAM_I[2]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[2]), 
                  .IO(DRAM_DQ2));
   IOBUF XLXI_39 (.I(DRAM_I[3]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[3]), 
                  .IO(DRAM_DQ3));
   IOBUF XLXI_40 (.I(DRAM_I[4]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[4]), 
                  .IO(DRAM_DQ4));
   IOBUF XLXI_41 (.I(DRAM_I[5]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[5]), 
                  .IO(DRAM_DQ5));
   IOBUF XLXI_42 (.I(DRAM_I[6]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[6]), 
                  .IO(DRAM_DQ6));
   IOBUF XLXI_43 (.I(DRAM_I[7]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[7]), 
                  .IO(DRAM_DQ7));
   IOBUF XLXI_44 (.I(DRAM_I[8]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[8]), 
                  .IO(DRAM_DQ8));
   IOBUF XLXI_45 (.I(DRAM_I[9]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[9]), 
                  .IO(DRAM_DQ9));
   IOBUF XLXI_46 (.I(DRAM_I[10]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[10]), 
                  .IO(DRAM_DQ10));
   IOBUF XLXI_47 (.I(DRAM_I[11]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[11]), 
                  .IO(DRAM_DQ11));
   IOBUF XLXI_48 (.I(DRAM_I[12]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[12]), 
                  .IO(DRAM_DQ12));
   IOBUF XLXI_49 (.I(DRAM_I[13]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[13]), 
                  .IO(DRAM_DQ13));
   IOBUF XLXI_50 (.I(DRAM_I[14]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[14]), 
                  .IO(DRAM_DQ14));
   IOBUF XLXI_51 (.I(DRAM_I[15]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[15]), 
                  .IO(DRAM_DQ15));
   IOBUF XLXI_77 (.I(DRAM_I[16]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[16]), 
                  .IO(DRAM_DQ16));
   IOBUF XLXI_78 (.I(DRAM_I[17]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[17]), 
                  .IO(DRAM_DQ17));
   IOBUF XLXI_79 (.I(DRAM_I[18]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[18]), 
                  .IO(DRAM_DQ18));
   IOBUF XLXI_80 (.I(DRAM_I[19]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[19]), 
                  .IO(DRAM_DQ19));
   IOBUF XLXI_81 (.I(DRAM_I[20]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[20]), 
                  .IO(DRAM_DQ20));
   IOBUF XLXI_82 (.I(DRAM_I[21]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[21]), 
                  .IO(DRAM_DQ21));
   IOBUF XLXI_83 (.I(DRAM_I[22]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[22]), 
                  .IO(DRAM_DQ22));
   IOBUF XLXI_84 (.I(DRAM_I[23]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[23]), 
                  .IO(DRAM_DQ23));
   IOBUF XLXI_85 (.I(DRAM_I[24]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[24]), 
                  .IO(DRAM_DQ24));
   IOBUF XLXI_86 (.I(DRAM_I[25]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[25]), 
                  .IO(DRAM_DQ25));
   IOBUF XLXI_87 (.I(DRAM_I[26]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[26]), 
                  .IO(DRAM_DQ26));
   IOBUF XLXI_88 (.I(DRAM_I[27]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[27]), 
                  .IO(DRAM_DQ27));
   IOBUF XLXI_89 (.I(DRAM_I[28]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[28]), 
                  .IO(DRAM_DQ28));
   IOBUF XLXI_90 (.I(DRAM_I[29]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[29]), 
                  .IO(DRAM_DQ29));
   IOBUF XLXI_91 (.I(DRAM_I[30]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[30]), 
                  .IO(DRAM_DQ30));
   IOBUF XLXI_92 (.I(DRAM_I[31]), 
                  .T(DRAM_T), 
                  .O(DRAM_O[31]), 
                  .IO(DRAM_DQ31));
   OBUF XLXI_100 (.I(DRAM_A[0]), 
                  .O(PIN_DRAM_A0));
   OBUF XLXI_101 (.I(DRAM_A[1]), 
                  .O(PIN_DRAM_A1));
   OBUF XLXI_102 (.I(DRAM_A[2]), 
                  .O(PIN_DRAM_A2));
   OBUF XLXI_103 (.I(DRAM_A[3]), 
                  .O(PIN_DRAM_A3));
   OBUF XLXI_104 (.I(DRAM_A[4]), 
                  .O(PIN_DRAM_A4));
   OBUF XLXI_105 (.I(DRAM_A[5]), 
                  .O(PIN_DRAM_A5));
   OBUF XLXI_106 (.I(DRAM_A[6]), 
                  .O(PIN_DRAM_A6));
   OBUF XLXI_107 (.I(DRAM_A[7]), 
                  .O(PIN_DRAM_A7));
   OBUF XLXI_108 (.I(DRAM_A[8]), 
                  .O(PIN_DRAM_A8));
   OBUF XLXI_109 (.I(DRAM_A[9]), 
                  .O(PIN_DRAM_A9));
   OBUF XLXI_110 (.I(DRAM_A[10]), 
                  .O(PIN_DRAM_A10));
   OBUF XLXI_111 (.I(DRAM_A[11]), 
                  .O(PIN_DRAM_A11));
   OBUF XLXI_112 (.I(XLXN_414), 
                  .O(PIN_DRAM_A12));
   OBUF XLXI_113 (.I(DRAM_RAS), 
                  .O(PIN_DRAM_RAS0));
   OBUF XLXI_114 (.I(DRAM_RAS), 
                  .O(PIN_DRAM_RAS1));
   OBUF XLXI_115 (.I(DRAM_CAS), 
                  .O(PIN_DRAM_CAS0));
   OBUF XLXI_116 (.I(DRAM_CAS), 
                  .O(PIN_DRAM_CAS1));
   OBUF XLXI_117 (.I(DRAM_CAS), 
                  .O(PIN_DRAM_CAS2));
   OBUF XLXI_118 (.I(DRAM_CAS), 
                  .O(PIN_DRAM_CAS3));
   OBUF XLXI_119 (.I(DRAM_WE), 
                  .O(PIN_DRAM_WE));
   BUF XLXI_219 (.I(XLXN_285), 
                 .O(PIN_TP16));
   BUF XLXI_221 (.I(XLXN_285), 
                 .O(PIN_TP17));
   BUF XLXI_223 (.I(XLXN_285), 
                 .O(PIN_TP18));
   BUF XLXI_224 (.I(XLXN_285), 
                 .O(PIN_JP6));
   BUF XLXI_225 (.I(XLXN_285), 
                 .O(PIN_J1_10));
   BUF XLXI_226 (.I(XLXN_285), 
                 .O(PIN_J1_12));
   BUF XLXI_227 (.I(XLXN_285), 
                 .O(PIN_J1_14));
   BUF XLXI_228 (.I(XLXN_285), 
                 .O(PIN_J1_16));
   BUF XLXI_229 (.I(XLXN_285), 
                 .O(PIN_J1_18));
   BUF XLXI_230 (.I(PIN_J1_20), 
                 .O(spi_clk));
   BUF XLXI_231 (.I(PIN_J1_22), 
                 .O(spi_cs));
   BUF XLXI_232 (.I(PIN_J1_24), 
                 .O(spi_si));
   BUF XLXI_233 (.I(PIN_J1_26), 
                 .O(spi_so));
   BUF XLXI_234 (.I(LED), 
                 .O(PIN_D3));
   BUF XLXI_236 (.I(cnt15), 
                 .O(PIN_JP9_1));
   BUF XLXI_237 (.I(XLXN_285), 
                 .O(PIN_JP9_3));
   BUF XLXI_238 (.I(XLXN_285), 
                 .O(PIN_JP9_5));
   BUF XLXI_240 (.I(XLXN_285), 
                 .O(PIN_EEPROM_A0));
   BUF XLXI_241 (.I(XLXN_285), 
                 .O(PIN_EEPROM_A1));
   BUF XLXI_242 (.I(XLXN_285), 
                 .O(PIN_EEPROM_A2));
   BUF XLXI_243 (.I(XLXN_285), 
                 .O(PIN_EEPROM_WP));
   BUF XLXI_244 (.I(XLXN_285), 
                 .O(PIN_EEPROM_SCL));
   BUF XLXI_245 (.I(XLXN_285), 
                 .O(PIN_EEPROM_SDA));
   GND XLXI_246 (.G(XLXN_285));
   VCC XLXI_247 (.P(XLXN_414));
   IBUF XLXI_248 (.I(PIN_SW2_DUMMY), 
                  .O(XLXN_419));
   PULLUP XLXI_250 (.O(PIN_SW2_DUMMY));
   INV XLXI_251 (.I(XLXN_419), 
                 .O(XLXN_420));
   BUF XLXI_252 (.I(CLK25), 
                 .O());
   BUF XLXI_255 (.I(ir_in), 
                 .O());
   BUF XLXI_258 (.I(rx1), 
                 .O(tx1));
endmodule
