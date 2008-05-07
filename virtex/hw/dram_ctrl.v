`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    21:29:12 04/10/2008 
// Design Name: 
// Module Name:    dram_ctrl 
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
module dram_ctrl(
    addr1,
    idata1,
    req1,
    we1,
    odata1,
    ack1,
    addr2,
    req2,
    odata2,
    ack2,
    clk,
    reset,
    dram_dq,
    dram_di,
    dram_t,
    dram_a,
    dram_we,
    dram_ras,
    dram_cas,
	 req_r,
	 ack_r,
	 wb_addr,
	 wb_idata,
	 wb_odata,
	 wb_stb,
	 wb_we,
	 wb_ack
	 
    );

    input [23:0] addr1;
    input [31:0] idata1;
    input req1;
    input we1;
    output [31:0] odata1;
    output ack1;
    input [23:0] addr2;
    input req2;
    output [31:0] odata2;
    output ack2;
    input clk;
    input reset;
    input [31:0] dram_dq;
    output [31:0] dram_di;
    output dram_t;
    output [11:0] dram_a;
    output dram_we;
    output dram_ras;
    output dram_cas;
    input req_r;
    output ack_r;
	 input [22:0] wb_addr;
	 input [31:0] wb_idata;
	 output [31:0] wb_odata;
	 input wb_stb;
	 input wb_we;
	 output wb_ack;

	 
	 `define STATE_IDLE 0
	 `define STATE_READ1_0 1
	 `define STATE_READ1_1 2
	 `define STATE_READ1_2 3
	 `define STATE_READ1_3 4
	 `define STATE_READ1_4 5
	 `define STATE_READ1_5 6
	 `define STATE_READ1_6 7
	 `define STATE_READ1_7 8
	 `define STATE_READ1_8 9

	 `define STATE_WRITE1_0 10
	 `define STATE_WRITE1_1 11
	 `define STATE_WRITE1_2 12
	 `define STATE_WRITE1_3 13
	 `define STATE_WRITE1_4 14
	 `define STATE_WRITE1_5 15
	 `define STATE_WRITE1_6 16
	 `define STATE_WRITE1_7 17
	 `define STATE_WRITE1_8 18
	 
	 `define STATE_READ2_0 19
	 `define STATE_READ2_1 20
	 `define STATE_READ2_2 21
	 `define STATE_READ2_3 22
	 `define STATE_READ2_4 23
	 `define STATE_READ2_5 24
	 `define STATE_READ2_6 25
	 `define STATE_READ2_7 26
	 `define STATE_READ2_8 27
	 
	 `define STATE_REFR_0 28
	 `define STATE_REFR_1 29
	 `define STATE_REFR_2 30
	 `define STATE_REFR_3 31
	 `define STATE_REFR_4 32
	 `define STATE_REFR_5 33
	 `define STATE_REFR_6 34
	 `define STATE_REFR_7 35
	 `define STATE_REFR_8 36
	 
	 `define STATE_READWB_S 55
	 `define STATE_READWB_0 37
	 `define STATE_READWB_1 38
	 `define STATE_READWB_2 39
	 `define STATE_READWB_3 40
	 `define STATE_READWB_4 41
	 `define STATE_READWB_5 42
	 `define STATE_READWB_6 43
	 `define STATE_READWB_7 44
	 `define STATE_READWB_8 45

	 `define STATE_WRITEWB_S 56
	 `define STATE_WRITEWB_0 46
	 `define STATE_WRITEWB_1 47
	 `define STATE_WRITEWB_2 48
	 `define STATE_WRITEWB_3 49
	 `define STATE_WRITEWB_4 50
	 `define STATE_WRITEWB_5 51
	 `define STATE_WRITEWB_6 52
	 `define STATE_WRITEWB_7 53
	 `define STATE_WRITEWB_8 54

	 reg [5:0] state;
	 reg dram_we;
	 reg dram_ras;
	 reg dram_cas;
	 reg [11:0] dram_a;
	 reg dram_t;
	 reg [31:0] dram_di;
	 reg ack1;
	 reg ack2;
	 reg ack_r;
	 reg [31:0] odata1;
	 reg [31:0] odata2;
	 reg [31:0] wb_odata;
	 reg wb_ack;

	 reg [22:0] wb_addr_resync;
	 reg [31:0] wb_idata_resync;
	 reg wb_stb_resync;
	 reg wb_we_resync;

	 always @(posedge clk)
	   begin
		 wb_addr_resync <= wb_addr;
		 wb_idata_resync <= wb_idata;
		 wb_stb_resync <= wb_stb;
		 wb_we_resync <= wb_we;
		end

	 always @(posedge clk)
	 begin
		if (reset == 1)
		 begin
			state <= 0;
			dram_we <= 1;
			dram_ras <= 1;
			dram_cas <= 1;
			dram_a <= 0;
			dram_t <= 1;
			dram_di <= 0;
			ack1 <= 0;
			ack2 <= 0;
			ack_r <= 0;
			odata1 <= 0;
			odata2 <= 0;
			wb_odata <= 0;
			wb_ack <= 0;
		 end
		else
		 case (state)
			`STATE_IDLE: 
				begin
				 if (req1 == 1)
				   begin
					  dram_a[11:0] <= addr1[22:11];
					  if (we1 == 1)
					    begin
							state <= `STATE_WRITE1_0;
						 end
					  else
					    begin
							state <= `STATE_READ1_0;
						 end
					end
				 else if (wb_stb_resync == 1)
				   begin
					  dram_a[11:0] <= wb_addr_resync[22:11];
					  if (wb_we_resync == 1)
					    begin
							state <= `STATE_WRITEWB_0;
						 end
					  else
					    begin
							state <= `STATE_READWB_0;
						 end
					end
			    else if (req2 == 1)
				   begin
					  dram_a[11:0] <= addr2[22:11];
					  state <= `STATE_READ2_0;
					end
			    else if (req_r == 1)
				   begin
					  state <= `STATE_REFR_0;
					end
				end
				
			`STATE_READ1_0: 
				begin
					dram_ras <= 0;
					state <= `STATE_READ1_1;
				end
			`STATE_READ1_1: 
				begin
					dram_a[10:0] <= addr1[10:0];
					dram_a[11] <= 0;
					state <= `STATE_READ1_2;
				end
			`STATE_READ1_2: 
				begin
					dram_cas <= 0;
					state <= `STATE_READ1_3;
				end
			`STATE_READ1_3: 
				state <= `STATE_READ1_4;
			`STATE_READ1_4: 
				state <= `STATE_READ1_5;
			`STATE_READ1_5: 
				state <= `STATE_READ1_6;
			`STATE_READ1_6: 
			   begin
					dram_ras <= 1;
					dram_cas <= 1;
					dram_a[11:0] <= 0;
					odata1 <= dram_dq;
					state <= `STATE_READ1_7;
				end
			`STATE_READ1_7:			
			   begin
					ack1 <= 1;
					state <= `STATE_READ1_8;
				end
			`STATE_READ1_8:			
			   begin
					ack1 <= 0;
					state <= `STATE_IDLE;
				end

			`STATE_WRITE1_0: 
				begin
					dram_ras <= 0;
					state <= `STATE_WRITE1_1;
				end
			`STATE_WRITE1_1: 
				begin
					dram_a[10:0] <= addr1[10:0];
					dram_a[11] <= 0;
					dram_we <= 0;
					dram_di <= idata1;
					dram_t <= 0;
					state <= `STATE_WRITE1_2;
				end
			`STATE_WRITE1_2: 
				begin
					dram_cas <= 0;
					state <= `STATE_WRITE1_3;
				end
			`STATE_WRITE1_3: 
				state <= `STATE_WRITE1_4;
			`STATE_WRITE1_4: 
				state <= `STATE_WRITE1_5;
			`STATE_WRITE1_5: 
			   begin
					dram_we <= 1;
					state <= `STATE_WRITE1_6;
				end
			`STATE_WRITE1_6: 
			   begin
					dram_ras <= 1;
					dram_cas <= 1;
					dram_a[11:0] <= 0;
					dram_t <= 1;
					dram_di <= 0;
					state <= `STATE_WRITE1_7;
				end
			`STATE_WRITE1_7:			
			   begin
					ack1 <= 1;
					state <= `STATE_WRITE1_8;
				end
			`STATE_WRITE1_8:			
			   begin
					ack1 <= 0;
					state <= `STATE_IDLE;
				end


			`STATE_READ2_0: 
				begin
					dram_ras <= 0;
					state <= `STATE_READ2_1;
				end
			`STATE_READ2_1: 
				begin
					dram_a[10:0] <= addr2[10:0];
					dram_a[11] <= 0;
					state <= `STATE_READ2_2;
				end
			`STATE_READ2_2: 
				begin
					dram_cas <= 0;
					state <= `STATE_READ2_3;
				end
			`STATE_READ2_3: 
				state <= `STATE_READ2_4;
			`STATE_READ2_4: 
				state <= `STATE_READ2_5;
			`STATE_READ2_5: 
				state <= `STATE_READ2_6;
			`STATE_READ2_6: 
			   begin
					dram_ras <= 1;
					dram_cas <= 1;
					dram_a[11:0] <= 0;
					odata2 <= dram_dq;
					state <= `STATE_READ2_7;
				end
			`STATE_READ2_7:			
			   begin
					ack2 <= 1;
					state <= `STATE_READ2_8;
				end
			`STATE_READ2_8:			
			   begin
					ack2 <= 0;
					state <= `STATE_IDLE;
				end


			`STATE_REFR_0: 
				begin
					dram_cas <= 0;
					state <= `STATE_REFR_1;
				end
			`STATE_REFR_1: 
				begin
					dram_ras <= 0;
					state <= `STATE_REFR_2;
				end
			`STATE_REFR_2: 
				begin
					state <= `STATE_REFR_3;
				end
			`STATE_REFR_3: 
			   begin
				  state <= `STATE_REFR_4;
				  dram_cas <= 1;
				end
			`STATE_REFR_4: 
				state <= `STATE_REFR_5;
			`STATE_REFR_5: 
				state <= `STATE_REFR_6;
			`STATE_REFR_6: 
			   begin
					dram_ras <= 1;
					state <= `STATE_REFR_7;
				end
			`STATE_REFR_7:			
			   begin
					ack_r <= 1;
					state <= `STATE_REFR_8;
				end
			`STATE_REFR_8:			
			   begin
					ack_r <= 0;
					state <= `STATE_IDLE;
				end


			`STATE_READWB_S: 
				begin
				   dram_a[11:0] <= wb_addr_resync[22:11];
					state <= `STATE_READWB_0;
				end
			`STATE_READWB_0: 
				begin
					dram_ras <= 0;
					state <= `STATE_READWB_1;
				end
			`STATE_READWB_1: 
				begin
					dram_a[10:0] <= wb_addr_resync[10:0];
					dram_a[11] <= 0;
					state <= `STATE_READWB_2;
				end
			`STATE_READWB_2: 
				begin
					dram_cas <= 0;
					state <= `STATE_READWB_3;
				end
			`STATE_READWB_3: 
				state <= `STATE_READWB_4;
			`STATE_READWB_4: 
				state <= `STATE_READWB_5;
			`STATE_READWB_5: 
				state <= `STATE_READWB_6;
			`STATE_READWB_6: 
			   begin
					dram_ras <= 1;
					dram_cas <= 1;
					dram_a[11:0] <= 0;
					wb_odata <= dram_dq;
					state <= `STATE_READWB_7;
				end
			`STATE_READWB_7:			
			   begin
					wb_ack <= 1;
					state <= `STATE_READWB_8;
				end
			`STATE_READWB_8:			
			   begin
				   if (wb_stb_resync == 0)
					  begin
						wb_ack <= 0;
						state <= `STATE_IDLE;
					  end
				end

			`STATE_WRITEWB_S: 
				begin
				   dram_a[11:0] <= wb_addr_resync[22:11];
					state <= `STATE_WRITEWB_0;
				end
			`STATE_WRITEWB_0: 
				begin
					dram_ras <= 0;
					state <= `STATE_WRITEWB_1;
				end
			`STATE_WRITEWB_1: 
				begin
					dram_a[10:0] <= wb_addr_resync[10:0];
					dram_a[11] <= 0;
					dram_we <= 0;
					dram_di <= wb_idata_resync;
					dram_t <= 0;
					state <= `STATE_WRITEWB_2;
				end
			`STATE_WRITEWB_2: 
				begin
					dram_cas <= 0;
					state <= `STATE_WRITEWB_3;
				end
			`STATE_WRITEWB_3: 
				state <= `STATE_WRITEWB_4;
			`STATE_WRITEWB_4: 
				state <= `STATE_WRITEWB_5;
			`STATE_WRITEWB_5: 
			   begin
					dram_we <= 1;
					state <= `STATE_WRITEWB_6;
				end
			`STATE_WRITEWB_6: 
			   begin
					dram_ras <= 1;
					dram_cas <= 1;
					dram_a[11:0] <= 0;
					dram_t <= 1;
					dram_di <= 0;
					state <= `STATE_WRITEWB_7;
				end
			`STATE_WRITEWB_7:			
			   begin
					wb_ack <= 1;
					state <= `STATE_WRITEWB_8;
				end
			`STATE_WRITEWB_8:			
			   begin
				   if (wb_stb_resync == 0)
					  begin
						wb_ack <= 0;
						state <= `STATE_IDLE;
					  end
				end
		 endcase
	 end


endmodule
