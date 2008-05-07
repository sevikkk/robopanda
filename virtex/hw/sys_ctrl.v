`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:59:55 04/21/2008 
// Design Name: 
// Module Name:    sys_ctrl 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module sys_ctrl(
    rx_data,
    rx_rdy,
    rx_rd,
    tx_data,
    tx_empty,
    tx_stb,
    spim_stb,
    spim_we,
    spim_addr,
    spim_odata,
    spim_ack,
    spim_idata,
    dram_stb,
    dram_we,
    dram_addr,
    dram_odata,
    dram_ack,
    dram_idata,
    clk,
    reset
    );

    input [7:0] rx_data;
    input rx_rdy;
    output rx_rd;
    output [7:0] tx_data;
	 input tx_empty;
    output tx_stb;
    output spim_stb;
    output spim_we;
    output [7:0] spim_addr;
    output [7:0] spim_odata;
    input spim_ack;
    input [7:0] spim_idata;
    output dram_stb;
    output dram_we;
    output [22:0] dram_addr;
    output [31:0] dram_odata;
    input dram_ack;
    input [31:0] dram_idata;
    input clk;
    input reset;
	 
	 reg rx_rd;
	 reg [7:0] tx_data;
	 reg tx_stb;
	 
	 reg spim_stb;
	 reg spim_we;
	 reg [7:0] spim_addr;
	 reg [7:0] spim_odata;
	 
	 reg [9:0] load_addr;
	 reg [9:0] next_load_addr;
	 
	 reg dram_stb;
	 reg dram_we;
	 reg [22:0] dram_addr;
	 reg [31:0] dram_odata;
	 
	 reg [5:0] state;
	 reg [7:0] tmp;
	 reg [31:0] tmp32;
	 reg [22:0] tmp_addr;

	 reg [5:0] next_state;
	 reg [7:0] next_tmp;
	 reg [31:0] next_tmp32;
	 reg [22:0] next_tmp_addr;
	 
	 reg next_rx_rd;
	 reg next_spim_stb;
	 reg next_dram_stb;
	 
	 reg [31:0] ram [0:1023];
	 
	 reg [31:0] pc;
	 reg [31:0] next_pc;
	 reg [31:0] acc;
	 reg [31:0] next_acc;
	 reg [31:0] idx;
	 reg [31:0] next_idx;
	 reg [31:0] idx2;
	 reg [31:0] next_idx2;
	 reg [31:0] cnt;
	 reg [31:0] next_cnt;
	 reg [31:0] cmd;
	 reg [31:0] next_cmd;
	 
	 reg [31:0] r0;
	 reg [31:0] next_r0;
	 reg [31:0] r1;
	 reg [31:0] next_r1;
	 reg [31:0] r2;
	 reg [31:0] next_r2;
	 reg [31:0] r3;
	 reg [31:0] next_r3;
	 
	 reg [9:0] int_ram_addr;
	 reg [31:0] int_ram_data;
	 reg int_ram_we;

	 reg [9:0] int_ram_raddr;
	 reg [9:0] next_int_ram_raddr;
	 wire [31:0] int_ram_rdata;
	 
	 `define	STATE_LOAD				0
	 `define	STATE_LOAD1				1
	 
	 `define	STATE_FETCH				2
	 `define	STATE_DECODE			3
	 `define	STATE_BAD_COMMAND		4
	 `define	STATE_BAD_COMMAND_1	5
	 `define	STATE_BAD_COMMAND_2	6
	 `define	STATE_BAD_COMMAND_3	7
	 `define	STATE_BAD_COMMAND_4	8
	 `define	STATE_BAD_COMMAND_5	9

	 `define	STATE_UARTWRITE_1		10
	 `define	STATE_UARTWRITE_2		11

	 `define	STATE_INT_RAM_READ	12

	 `define	STATE_WRITE_HEX		13

	 `define	STATE_READWB			14
	 `define	STATE_WRITEWB			15
	 `define	STATE_READDRAM			16
	 `define	STATE_WRITEDRAM		17
	 `define	STATE_READDRAM_2		18
 
	always @(rx_data, rx_rdy, tx_empty, spim_ack, spim_idata, state, tmp, spim_stb, dram_ack, tmp32, tmp_addr, 
			dram_idata, dram_stb, cmd, pc, idx, acc, int_ram_raddr, int_ram_rdata, idx2, cnt, load_addr)
	begin

		spim_we <= 0;
		spim_addr <= 0;
		spim_odata <= 0;
		
		tx_data <= 0;
		tx_stb <= 0;

		dram_we <= 0;
		dram_addr <= 0;
		dram_odata <= 0;
		
		next_rx_rd <= 0;
		
		next_spim_stb <= spim_stb;
		next_dram_stb <= dram_stb;
		next_state <= state;
		next_tmp <= tmp;
		next_tmp32 <= tmp32;
		next_tmp_addr <= tmp_addr;
		next_int_ram_raddr <= int_ram_raddr;
		
		next_pc <= pc;
		next_acc <= acc;
		next_idx <= idx;
		next_idx2 <= idx2;
		next_cnt <= cnt;
		
		next_r0 <= r0;
		next_r1 <= r1;
		next_r2 <= r2;
		next_r3 <= r3;
	
		next_cmd <= cmd;
		int_ram_we <= 0;
		int_ram_addr <= 0;
		int_ram_data <= 0;
		next_load_addr <= 0;
		
		case (state)
			`STATE_LOAD: begin
				next_state <= `STATE_LOAD1;
				next_tmp32 <= 0;
				next_load_addr <= 0;
			end
			`STATE_LOAD1: begin
				int_ram_addr <= tmp32[9:0];
				int_ram_we <= 1;
			   case (load_addr)
					0: int_ram_data <= 32'h20000080;
					1: int_ram_data <= 32'h00000000;
					2: int_ram_data <= 32'h00000000;
					3: int_ram_data <= 32'h00000000;
					4: int_ram_data <= 32'h00000000;
					5: int_ram_data <= 32'h00000000;
					6: int_ram_data <= 32'h00000000;
					7: int_ram_data <= 32'h00000000;
					8: int_ram_data <= 32'h00000000;
					9: int_ram_data <= 32'h00000000;
					10: int_ram_data <= 32'h00000000;
					11: int_ram_data <= 32'h00000000;
					12: int_ram_data <= 32'h00000000;
					13: int_ram_data <= 32'h00000000;
					14: int_ram_data <= 32'h00000000;
					15: int_ram_data <= 32'h00000000;
					16: int_ram_data <= 32'h00000000;
					17: int_ram_data <= 32'h00000000;
					18: int_ram_data <= 32'h00000000;
					19: int_ram_data <= 32'h00000000;
					20: int_ram_data <= 32'h00000000;
					21: int_ram_data <= 32'h00000000;
					22: int_ram_data <= 32'h00000000;
					23: int_ram_data <= 32'h00000000;
					24: int_ram_data <= 32'h00000000;
					25: int_ram_data <= 32'h00000000;
					26: int_ram_data <= 32'h00000000;
					27: int_ram_data <= 32'h00000000;
					28: int_ram_data <= 32'h00000000;
					29: int_ram_data <= 32'h00000000;
					30: int_ram_data <= 32'h00000000;
					31: int_ram_data <= 32'h00000000;
					32: int_ram_data <= 32'h00000000;
					33: int_ram_data <= 32'h00000000;
					34: int_ram_data <= 32'h00000000;
					35: int_ram_data <= 32'h00000000;
					36: int_ram_data <= 32'h00000000;
					37: int_ram_data <= 32'h00000000;
					38: int_ram_data <= 32'h00000000;
					39: int_ram_data <= 32'h00000000;
					40: int_ram_data <= 32'h00000000;
					41: int_ram_data <= 32'h00000000;
					42: int_ram_data <= 32'h00000000;
					43: int_ram_data <= 32'h00000000;
					44: int_ram_data <= 32'h00000000;
					45: int_ram_data <= 32'h00000000;
					46: int_ram_data <= 32'h00000000;
					47: int_ram_data <= 32'h00000000;
					48: int_ram_data <= 32'h00000000;
					49: int_ram_data <= 32'h00000000;
					50: int_ram_data <= 32'h00000000;
					51: int_ram_data <= 32'h00000000;
					52: int_ram_data <= 32'h00000000;
					53: int_ram_data <= 32'h00000000;
					54: int_ram_data <= 32'h00000000;
					55: int_ram_data <= 32'h00000000;
					56: int_ram_data <= 32'h00000000;
					57: int_ram_data <= 32'h00000000;
					58: int_ram_data <= 32'h00000000;
					59: int_ram_data <= 32'h00000000;
					60: int_ram_data <= 32'h00000000;
					61: int_ram_data <= 32'h00000000;
					62: int_ram_data <= 32'h00000000;
					63: int_ram_data <= 32'h00000000;
					64: int_ram_data <= 32'h00000000;
					65: int_ram_data <= 32'h00000000;
					66: int_ram_data <= 32'h00000000;
					67: int_ram_data <= 32'h00000000;
					68: int_ram_data <= 32'h00000000;
					69: int_ram_data <= 32'h00000000;
					70: int_ram_data <= 32'h00000000;
					71: int_ram_data <= 32'h00000000;
					72: int_ram_data <= 32'h00000000;
					73: int_ram_data <= 32'h00000000;
					74: int_ram_data <= 32'h00000000;
					75: int_ram_data <= 32'h00000000;
					76: int_ram_data <= 32'h00000000;
					77: int_ram_data <= 32'h00000000;
					78: int_ram_data <= 32'h00000000;
					79: int_ram_data <= 32'h00000000;
					80: int_ram_data <= 32'h00000000;
					81: int_ram_data <= 32'h00000000;
					82: int_ram_data <= 32'h00000000;
					83: int_ram_data <= 32'h00000000;
					84: int_ram_data <= 32'h00000000;
					85: int_ram_data <= 32'h00000000;
					86: int_ram_data <= 32'h00000000;
					87: int_ram_data <= 32'h00000000;
					88: int_ram_data <= 32'h00000000;
					89: int_ram_data <= 32'h00000000;
					90: int_ram_data <= 32'h00000000;
					91: int_ram_data <= 32'h00000000;
					92: int_ram_data <= 32'h00000000;
					93: int_ram_data <= 32'h00000000;
					94: int_ram_data <= 32'h00000000;
					95: int_ram_data <= 32'h00000000;
					96: int_ram_data <= 32'h00000000;
					97: int_ram_data <= 32'h00000000;
					98: int_ram_data <= 32'h00000000;
					99: int_ram_data <= 32'h00000000;
					100: int_ram_data <= 32'h00000000;
					101: int_ram_data <= 32'h00000000;
					102: int_ram_data <= 32'h00000000;
					103: int_ram_data <= 32'h00000000;
					104: int_ram_data <= 32'h00000000;
					105: int_ram_data <= 32'h00000000;
					106: int_ram_data <= 32'h00000000;
					107: int_ram_data <= 32'h00000000;
					108: int_ram_data <= 32'h00000000;
					109: int_ram_data <= 32'h00000000;
					110: int_ram_data <= 32'h00000000;
					111: int_ram_data <= 32'h00000000;
					112: int_ram_data <= 32'h00000000;
					113: int_ram_data <= 32'h00000000;
					114: int_ram_data <= 32'h00000000;
					115: int_ram_data <= 32'h00000000;
					116: int_ram_data <= 32'h00000000;
					117: int_ram_data <= 32'h00000000;
					118: int_ram_data <= 32'h00000000;
					119: int_ram_data <= 32'h00000000;
					120: int_ram_data <= 32'h00000000;
					121: int_ram_data <= 32'h00000000;
					122: int_ram_data <= 32'h00000000;
					123: int_ram_data <= 32'h00000000;
					124: int_ram_data <= 32'h00000000;
					125: int_ram_data <= 32'h00000000;
					126: int_ram_data <= 32'h00000000;
					127: int_ram_data <= 32'h00000000;
					128: int_ram_data <= 32'h13555241;
					129: int_ram_data <= 32'h13212121;
					130: int_ram_data <= 32'h120d0a00;
					131: int_ram_data <= 32'h13436c65;
					132: int_ram_data <= 32'h13617220;
					133: int_ram_data <= 32'h13445241;
					134: int_ram_data <= 32'h134d2e2e;
					135: int_ram_data <= 32'h102e0000;
					136: int_ram_data <= 32'h3e008000;
					137: int_ram_data <= 32'h43000000;
					138: int_ram_data <= 32'h3e000000;
					139: int_ram_data <= 32'h42000000;
					140: int_ram_data <= 32'h3e345678;
					141: int_ram_data <= 32'h3f000012;
					142: int_ram_data <= 32'h1f000000;
					143: int_ram_data <= 32'h2f00008e;
					144: int_ram_data <= 32'h13646f6e;
					145: int_ram_data <= 32'h13650d0a;
					146: int_ram_data <= 32'h13496e69;
					147: int_ram_data <= 32'h13742053;
					148: int_ram_data <= 32'h13444361;
					149: int_ram_data <= 32'h1372642e;
					150: int_ram_data <= 32'h122e2e00;
					151: int_ram_data <= 32'h3e000001;
					152: int_ram_data <= 32'h19000002;
					153: int_ram_data <= 32'h19000003;
					154: int_ram_data <= 32'h18000004;
					155: int_ram_data <= 32'h26000001;
					156: int_ram_data <= 32'h2000009a;
					157: int_ram_data <= 32'h13646f6e;
					158: int_ram_data <= 32'h13652c20;
					159: int_ram_data <= 32'h13636f64;
					160: int_ram_data <= 32'h13653a20;
					161: int_ram_data <= 32'h18000005;
					162: int_ram_data <= 32'h17000000;
					163: int_ram_data <= 32'h120d0a00;
					164: int_ram_data <= 32'h130d0a4f;
					165: int_ram_data <= 32'h136b3e20;
					166: int_ram_data <= 32'h240000a6;
					167: int_ram_data <= 32'h220000a7;
					168: int_ram_data <= 32'h30000000;
					169: int_ram_data <= 32'h40000000;
					170: int_ram_data <= 32'h120d0a00;
					171: int_ram_data <= 32'h26000072;
					172: int_ram_data <= 32'h200000b4;
					173: int_ram_data <= 32'h26000069;
					174: int_ram_data <= 32'h20000092;
					175: int_ram_data <= 32'h26000067;
					176: int_ram_data <= 32'h20000000;
					177: int_ram_data <= 32'h13457272;
					178: int_ram_data <= 32'h136f7221;
					179: int_ram_data <= 32'h200000a4;
					180: int_ram_data <= 32'h13534420;
					181: int_ram_data <= 32'h13526561;
					182: int_ram_data <= 32'h13642e2e;
					183: int_ram_data <= 32'h102e0000;
					184: int_ram_data <= 32'h3e000000;
					185: int_ram_data <= 32'h19000007;
					186: int_ram_data <= 32'h19000008;
					187: int_ram_data <= 32'h19000009;
					188: int_ram_data <= 32'h1900000a;
					189: int_ram_data <= 32'h3e000002;
					190: int_ram_data <= 32'h19000002;
					191: int_ram_data <= 32'h3e000001;
					192: int_ram_data <= 32'h19000003;
					193: int_ram_data <= 32'h18000004;
					194: int_ram_data <= 32'h26000001;
					195: int_ram_data <= 32'h200000c1;
					196: int_ram_data <= 32'h13646f6e;
					197: int_ram_data <= 32'h13652c20;
					198: int_ram_data <= 32'h13636f64;
					199: int_ram_data <= 32'h13653a20;
					200: int_ram_data <= 32'h18000005;
					201: int_ram_data <= 32'h17000000;
					202: int_ram_data <= 32'h130d0a43;
					203: int_ram_data <= 32'h136f756e;
					204: int_ram_data <= 32'h13743a20;
					205: int_ram_data <= 32'h18000012;
					206: int_ram_data <= 32'h17000000;
					207: int_ram_data <= 32'h18000013;
					208: int_ram_data <= 32'h17000000;
					209: int_ram_data <= 32'h120d0a00;
					210: int_ram_data <= 32'h3e00007f;
					211: int_ram_data <= 32'h43000000;
					212: int_ram_data <= 32'h3e000000;
					213: int_ram_data <= 32'h42000000;
					214: int_ram_data <= 32'h3e000000;
					215: int_ram_data <= 32'h18000010;
					216: int_ram_data <= 32'h50100000;
					217: int_ram_data <= 32'h18000010;
					218: int_ram_data <= 32'h50100000;
					219: int_ram_data <= 32'h18000010;
					220: int_ram_data <= 32'h50100000;
					221: int_ram_data <= 32'h18000010;
					222: int_ram_data <= 32'h14000000;
					223: int_ram_data <= 32'h10200000;
					224: int_ram_data <= 32'h49000000;
					225: int_ram_data <= 32'h240000e1;
					226: int_ram_data <= 32'h2f0000d6;
					227: int_ram_data <= 32'h120d0a00;
					228: int_ram_data <= 32'h200000a4;
					229: begin
						next_state <= `STATE_FETCH;
						int_ram_we <= 0;
					end
				endcase
				next_tmp32 <= tmp32 + 1;
				next_load_addr <= tmp32 + 1;
			end
			`STATE_FETCH: begin
				next_int_ram_raddr <= pc[9:0];
				next_pc <= pc + 1;
				next_state <= `STATE_DECODE;
			end
			`STATE_DECODE: begin
				next_state <= `STATE_BAD_COMMAND;
				next_cmd <= int_ram_rdata;
			   case (int_ram_rdata[31:28])
					1: // UARTWRITE
						begin
							case (int_ram_rdata[27:26])
								0: // WRITEUART "X"
									begin
										tx_data <= int_ram_rdata[23:16];
										tx_stb <= 1;
										if (int_ram_rdata[25])
											next_state <= `STATE_UARTWRITE_1;
										else
											next_state <= `STATE_FETCH;
									end
								1: // WRITEUART acc, hex[4321]
									begin
										case (int_ram_rdata[25:24])
										0: begin
												next_tmp32 <= acc;
												next_tmp <= 7;
											end
										1: begin
												next_tmp32 <= acc<<8;
												next_tmp <= 5;
											end
										2: begin
												next_tmp32 <= acc<<16;
												next_tmp <= 3;
											end
										3: begin
												next_tmp32 <= acc<<24;
												next_tmp <= 1;
											end
										endcase
										next_state <= `STATE_WRITE_HEX;
									end
								2: 
									case (int_ram_rdata[25:24])
										0: // READWB @X
										begin
											next_tmp <= int_ram_rdata[7:0];
											spim_addr <= int_ram_rdata[7:0];
											next_spim_stb <= 1;
											
											next_state <= `STATE_READWB;
										end

										1: // WRITEWB @X
										begin
											next_tmp <= int_ram_rdata[7:0];
											spim_addr <= int_ram_rdata[7:0];
											spim_we <= 1;
											spim_odata <= acc[7:0];
											next_spim_stb <= 1;
											
											next_state <= `STATE_WRITEWB;
										end
										2: // READDRAM @X
										begin
											next_tmp32 <= int_ram_rdata[23:0];
											next_state <= `STATE_READDRAM;
										end

										3: // WRITEDRAM @X
										begin
											next_tmp32 <= int_ram_rdata[23:0];
											next_state <= `STATE_WRITEDRAM;
										end
									endcase
								3: 
									case (int_ram_rdata[25:24])
									0: // READDRAM @idx
										begin
											next_tmp32 <= idx;
											next_state <= `STATE_READDRAM;
										end

									1: // WRITEDRAM @idx2
										begin
											next_tmp32 <= idx2;
											next_state <= `STATE_WRITEDRAM;
										end
									2: // READDRAM @idx+
										begin
											next_tmp32 <= idx;
											next_state <= `STATE_READDRAM;
											next_idx <= idx + 1;
										end

									3: // WRITEDRAM @idx2+
										begin
											next_tmp32 <= idx2[23:0];
											next_state <= `STATE_WRITEDRAM;
											next_idx2 <= idx2 + 1;
										end
									endcase
							endcase
						end
					2: // JUMP
						begin
							case (int_ram_rdata[27:24])
								0: // JUMP #X
									begin
										next_pc <= int_ram_rdata[23:0];
										next_state <= `STATE_FETCH;
									end
								1: // JUMP #X, rx_rdy
									begin
										if (rx_rdy)
											next_pc <= int_ram_rdata[23:0];
										next_state <= `STATE_FETCH;
									end
								2: // JUMP #X, !rx_rdy
									begin
										if (!rx_rdy)
											next_pc <= int_ram_rdata[23:0];
										next_state <= `STATE_FETCH;
									end
								3: // JUMP #X, tx_empty
									begin
										if (tx_empty)
											next_pc <= int_ram_rdata[23:0];
										next_state <= `STATE_FETCH;
									end
								4: // JUMP #X, !tx_empty
									begin
										if (!tx_empty)
											next_pc <= int_ram_rdata[23:0];
										next_state <= `STATE_FETCH;
									end
								5: // SKIP =X
									begin
										if (acc[23:0] == int_ram_rdata[23:0])
											next_pc <= pc + 1;
										next_state <= `STATE_FETCH;
									end
								6: // SKIP !X
									begin
										if (acc[23:0] != int_ram_rdata[23:0])
											next_pc <= pc + 1;
										next_state <= `STATE_FETCH;
									end
								14: // JUMP acc
									begin
										next_pc <= acc;
										next_state <= `STATE_FETCH;
									end
								15: // LOOP #X
									begin
										if (cnt != 0)
											next_pc <= int_ram_rdata[23:0];
										next_cnt <= cnt - 1;
										next_state <= `STATE_FETCH;
									end
							endcase
						end
					3: // READ
						begin
							case (int_ram_rdata[27:24])
								0: // READ uart
									begin
										next_acc <= rx_data;
										next_rx_rd <= 1;
										next_state <= `STATE_FETCH;
									end
								1: // READ idx
									begin
										next_acc <= idx;
										next_state <= `STATE_FETCH;
									end
								2: // READ idx2
									begin
										next_acc <= idx2;
										next_state <= `STATE_FETCH;
									end
								3: // READ cnt
									begin
										next_acc <= cnt;
										next_state <= `STATE_FETCH;
									end
								4: // READ r0
									begin
										next_acc <= r0;
										next_state <= `STATE_FETCH;
									end
								5: // READ r1
									begin
										next_acc <= r1;
										next_state <= `STATE_FETCH;
									end
								6: // READ r2
									begin
										next_acc <= r2;
										next_state <= `STATE_FETCH;
									end
								7: // READ r3
									begin
										next_acc <= r3;
										next_state <= `STATE_FETCH;
									end
								8: // READ @idx
									begin
										next_int_ram_raddr <= idx[9:0];
										next_state <= `STATE_INT_RAM_READ;
									end
								9: // READ @idx+
									begin
										next_int_ram_raddr <= idx[9:0];
										next_state <= `STATE_INT_RAM_READ;
										next_idx <= idx + 1;
									end
								10: // READ @X
									begin
										next_int_ram_raddr <= int_ram_rdata[9:0];
										next_state <= `STATE_INT_RAM_READ;
									end
								14: // READ #X
									begin
										next_acc <= int_ram_rdata[23:0];
										next_state <= `STATE_FETCH;
									end
								15: // READH #X
									begin
										next_acc[31:24] <= int_ram_rdata[7:0];
										next_state <= `STATE_FETCH;
									end
							endcase
						end
					4: // WRITE
						begin
							case (int_ram_rdata[27:24])
								0: //WRITE uart
									begin
										tx_data <= acc[7:0];
										tx_stb <= 1;
										next_state <= `STATE_FETCH;
									end
								1: // WRITE idx
									begin
										next_idx <= acc;
										next_state <= `STATE_FETCH;
									end
								2: // WRITE idx2
									begin
										next_idx2 <= acc;
										next_state <= `STATE_FETCH;
									end
								3: // WRITE cnt
									begin
										next_cnt <= acc;
										next_state <= `STATE_FETCH;
									end
								4: // WRITE r0
									begin
										next_r0 <= acc;
										next_state <= `STATE_FETCH;
									end
								5: // WRITE r1
									begin
										next_r1 <= acc;
										next_state <= `STATE_FETCH;
									end
								6: // WRITE r2
									begin
										next_r2 <= acc;
										next_state <= `STATE_FETCH;
									end
								7: // WRITE r3
									begin
										next_r3 <= acc;
										next_state <= `STATE_FETCH;
									end
								8: // WRITE @idx2
									begin
										int_ram_addr <= idx2[9:0];
										int_ram_data <= acc;
										int_ram_we <= 1;
										next_state <= `STATE_FETCH;
									end
								9: // WRITE @idx2+
									begin
										int_ram_addr <= idx2[9:0];
										int_ram_data <= acc;
										int_ram_we <= 1;
										next_state <= `STATE_FETCH;
										next_idx2 <= idx2 + 1;
									end
								10: // WRITE @X
									begin
										int_ram_addr <= int_ram_rdata[9:0];
										int_ram_data <= acc;
										int_ram_we <= 1;
										next_state <= `STATE_FETCH;
									end
							endcase
						end
					5: // ALU
						begin
							next_state <= `STATE_FETCH;
							case (int_ram_rdata[27:24])
								0: // shift
									case (int_ram_rdata[23:20])
										0: // shift left1
											next_acc <= acc << 1;
										1: // shift left8
											next_acc <= acc << 8;
										2: // shift right1
											next_acc <= acc >> 1;
										3: // shift right8
											next_acc <= acc >> 8;
										default:
											next_state <= `STATE_BAD_COMMAND;

									endcase
								1: // ops #X
									case (int_ram_rdata[23:20])
										0: // ANDL
											next_acc[15:0] <= acc[15:0] & int_ram_rdata[15:0];
										1: // ANDH
											next_acc[31:16] <= acc[31:16] & int_ram_rdata[15:0];
										2: // ORL
											next_acc[15:0] <= acc[15:0] | int_ram_rdata[15:0];
										3: // ORH
											next_acc[31:16] <= acc[31:16] | int_ram_rdata[15:0];
										4: // XORL
											next_acc[15:0] <= acc[15:0] & int_ram_rdata[15:0];
										5: // XORH
											next_acc[31:16] <= acc[31:16] ^ int_ram_rdata[15:0];
										6: // ADDL
											next_acc[31:0] <= acc[31:0] + int_ram_rdata[15:0];
										7: // ADDH
											next_acc[31:16] <= acc[31:16] + int_ram_rdata[15:0];
										8: // SUBL
											next_acc[31:0] <= acc[31:0] - int_ram_rdata[15:0];
										9: // SUBH
											next_acc[31:16] <= acc[31:16] - int_ram_rdata[15:0];
										12: // SUB r0
											next_acc <= acc - r0;
										13: // SUB r1
											next_acc <= acc - r1;
										14: // SUB r2
											next_acc <= acc - r2;
										15: // SUB r3
											next_acc <= acc - r3;
										default:
											next_state <= `STATE_BAD_COMMAND;
									endcase
								2: // ops rX
									case (int_ram_rdata[23:20])
										0: // AND r0
											next_acc <= acc & r0;
										1: // AND r1
											next_acc <= acc & r1;
										2: // AND r2
											next_acc <= acc & r2;
										3: // AND r3
											next_acc <= acc & r3;
										4: // OR r0
											next_acc <= acc | r0;
										5: // OR r1
											next_acc <= acc | r1;
										6: // OR r2
											next_acc <= acc | r2;
										7: // OR r3
											next_acc <= acc | r3;
										8: // XOR r0
											next_acc <= acc ^ r0;
										9: // XOR r1
											next_acc <= acc ^ r1;
										10: // XOR r2
											next_acc <= acc ^ r2;
										11: // XOR r3
											next_acc <= acc ^ r3;
										12: // ADD r0
											next_acc <= acc + r0;
										13: // ADD r1
											next_acc <= acc + r1;
										14: // ADD r2
											next_acc <= acc + r2;
										15: // ADD r3
											next_acc <= acc + r3;
									endcase
								default:
									next_state <= `STATE_BAD_COMMAND;
							endcase
						end
				endcase
			end
			`STATE_INT_RAM_READ: begin
				next_acc <= int_ram_rdata;
				next_state <= `STATE_FETCH;
			end
			`STATE_WRITE_HEX: begin
			   if (tmp32[31:28]<10)
					tx_data <= "0" + tmp32[31:28];
				else
					tx_data <= "A" + tmp32[31:28] - 10;
					
				tx_stb <= 1;
				next_tmp32 <= tmp32<<4;
				next_tmp <= tmp - 1;
				if (tmp == 0)
					next_state <= `STATE_FETCH;
			end

			`STATE_READWB: begin
				spim_addr <= tmp;
				if (spim_ack)
					begin
						next_spim_stb <= 0;
						next_acc[7:0] <= spim_idata;
						next_state <= `STATE_FETCH;
					end
			end

			`STATE_WRITEWB: begin
				spim_addr <= tmp;
				spim_we <= 1;
				spim_odata <= acc[7:0];
				if (spim_ack)
					begin
						next_spim_stb <= 0;
						next_state <= `STATE_FETCH;
					end
			end

			`STATE_READDRAM: begin
				next_dram_stb <= 1;
				dram_addr <= tmp32[23:0];
				if (dram_ack)
					begin
						next_state <= `STATE_READDRAM_2;
					end
			end
			`STATE_READDRAM_2: begin
					next_acc <= dram_idata;
					next_dram_stb <= 0;
					next_state <= `STATE_FETCH;
			end

			`STATE_WRITEDRAM: begin
				dram_addr <= tmp32[23:0];
				dram_we <= 1;
				next_dram_stb <= 1;
				dram_odata <= acc;
				if (dram_ack)
					begin
						next_dram_stb <= 0;
						next_state <= `STATE_FETCH;
					end
			end

			`STATE_BAD_COMMAND: begin
				next_tmp <= 0;
				next_state <= `STATE_BAD_COMMAND_1;
			end
			`STATE_BAD_COMMAND_1: begin
				tx_stb <= 1;
				next_tmp <= tmp + 1;
				case (tmp)
					0:
						tx_data <= "B";
					1:
						tx_data <= "a";
					2:
						tx_data <= "d";
					3:
						tx_data <= " ";
					4:
						tx_data <= "c";
					5:
						tx_data <= "m";
					6:
						tx_data <= "d";
					7:
						tx_data <= " ";
					8:
						begin
							tx_stb <= 0;
							next_state <= `STATE_BAD_COMMAND_2;
							next_tmp32 <= pc - 1;
							next_tmp <= 0;
						end
				endcase
			end
			`STATE_BAD_COMMAND_2: begin
			   if (tmp32[31:28]<10)
					tx_data <= "0" + tmp32[31:28];
				else
					tx_data <= "A" + tmp32[31:28] - 10;
					
				tx_stb <= 1;
				next_tmp32 <= tmp32<<4;
				next_tmp <= tmp + 1;
				if (tmp == 7)
					begin
						next_state <= `STATE_BAD_COMMAND_3;
					end
			end
			`STATE_BAD_COMMAND_3: begin
				tx_data <= " ";
				tx_stb <= 1;
				next_tmp32 <= cmd;
				next_tmp <= 0;
				next_state <= `STATE_BAD_COMMAND_4;
			end
			`STATE_BAD_COMMAND_4: begin
			   if (tmp32[31:28]<10)
					tx_data <= "0" + tmp32[31:28];
				else
					tx_data <= "A" + tmp32[31:28] - 10;
					
				tx_stb <= 1;
				next_tmp32 <= tmp32<<4;
				next_tmp <= tmp + 1;
				if (tmp == 7)
					next_state <= `STATE_BAD_COMMAND_5;
			end
			`STATE_BAD_COMMAND_5: begin
				// endless loop
			end
			`STATE_UARTWRITE_1: begin
				tx_data <= cmd[15:8];
				tx_stb <= 1;
				if (cmd[24])
					next_state <= `STATE_UARTWRITE_2;
				else
					next_state <= `STATE_FETCH;
			end
			`STATE_UARTWRITE_2: begin
				tx_data <= cmd[7:0];
				tx_stb <= 1;
				next_state <= `STATE_FETCH;
			end
		endcase
	end

	always @(posedge clk)
		begin
			if (reset)
				begin
					state <= `STATE_LOAD;
					tmp <= 0;
					rx_rd <= 0;
					spim_stb <= 0;
					dram_stb <= 0;
					tmp32 <= 0;
					tmp_addr <= 0;
					pc <= 0;
					acc <= 0;
					idx <= 0;
					idx2 <= 0;
					cnt <= 0;
					cmd <= 0;
					r0 <= 0;
					r1 <= 0;
					r2 <= 0;
					r3 <= 0;
				end
			else
				begin
					state <= next_state;
					tmp <= next_tmp;
					tmp32 <= next_tmp32;
					tmp_addr <= next_tmp_addr;
					rx_rd <= next_rx_rd;
					spim_stb <= next_spim_stb;
					dram_stb <= next_dram_stb;
					pc <= next_pc;
					acc <= next_acc;
					idx <= next_idx;
					idx2 <= next_idx2;
					cnt <= next_cnt;
					cmd <= next_cmd;
					r0 <= next_r0;
					r1 <= next_r1;
					r2 <= next_r2;
					r3 <= next_r3;
					int_ram_raddr <= next_int_ram_raddr;
					load_addr <= next_load_addr;
					if (int_ram_we)
						ram[int_ram_addr] <= int_ram_data;
				end
		end

assign int_ram_rdata = ram[int_ram_raddr];

endmodule
