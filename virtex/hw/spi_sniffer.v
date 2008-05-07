`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    23:37:34 04/17/2008 
// Design Name: 
// Module Name:    spi_sniffer 
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
module spi_sniffer(
	spi_cs,
	spi_clk,
	spi_si,
	spi_so,
	clk,
	reset,
	data,
	data_stb,
	enable,
	addr_hi,
	addr_lo,
	addr_changed,
	load,
	shift
	);

	input spi_cs;
	input spi_clk;
	input spi_si;
	input spi_so;
	input clk;
	input reset;
	input enable;

	output [31:0] data;
	output data_stb;
	
	output [21:0] addr_hi;
	output [1:0] addr_lo;
	output addr_changed;
	output load;
	output shift;

	reg [63:0] data;
	reg data_stb;

	reg [21:0] addr_hi;
	reg [21:0] last_addr_hi;
	reg [1:0] addr_lo;
	reg addr_changed;
	reg load;
	reg shift;

	reg [31:0] ts;
	reg [3:0] cmd_id;
	reg [7:0] cmd;
	reg [23:0] addr;
	reg [8:0] byte_cnt;
	reg [4:0] bit_cnt;

	reg sync_spi_cs;
	reg sync_spi_clk;
	reg sync_spi_si;
	reg sync_spi_so;

	reg [5:0] state;
	
	`define STATE_INIT 		0
	`define STATE_RESET_1 	1
	`define STATE_RESET_2 	2
	`define STATE_CMD_0 		5
	`define STATE_CMD_1 		6
	`define STATE_UNKNOWN 	7
	`define STATE_ADDR_0 	8
	`define STATE_ADDR_1 	9
	`define STATE_DATA_0 	10
	`define STATE_DATA_1 	11

	wire [23:0] next_addr;
	wire [23:0] next_addr2;
	wire [7:0] next_cmd;

	assign next_addr = addr[22:0] << 1 | sync_spi_si;
	assign next_addr2 = addr + byte_cnt + 1;
	assign next_cmd = cmd[6:0] << 1 | sync_spi_si;


	always @(posedge clk)
		if (reset)
			begin
				data <= 0;
				data_stb <= 0;

				ts <= 0;
				cmd_id <= 0;
				cmd <= 8'hff;
				addr <= 24'hffffff;
				byte_cnt <= 0;
				bit_cnt <= 0;

				addr_hi <= 24'hffffff;
				last_addr_hi <= 24'hffffff;
				addr_lo <= 0;
				addr_changed <= 0;
				load <= 0;
				shift <= 0;

				sync_spi_cs <= 0;
				sync_spi_clk <= 0;
				sync_spi_si <= 0;
				sync_spi_so <= 0;
				state <= `STATE_INIT;
			end
		else
			begin
				sync_spi_cs <= spi_cs;
				sync_spi_clk <= spi_clk;
				sync_spi_si <= spi_si;
				sync_spi_so <= spi_so;

				last_addr_hi <= addr_hi;
				if (last_addr_hi != addr_hi)
					addr_changed <= 1;
				else
					addr_changed <= 0;
					
				load <= 0;
				shift <= 0;
				
				ts <= ts + 1;
				data_stb <= 0;
				case (state)
					`STATE_INIT: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_2;
					end
					`STATE_RESET_1: begin
						state <= `STATE_RESET_2;
						if (enable)
							begin
								data[63:61] <= 3; // timestamp
								data[60:57] <= cmd_id;
								data[56:48] <= byte_cnt;
								data[47:32] <= ts[20:5]; 
								if (cmd == 3)
									begin
										data[31:29] <= 5; // read
										data[28:25] <= cmd_id;
										data[24] <= 1; // normal read
										data[23:0] <= addr; 
									end
								else
									begin
										data[31:29] <= 1; // unknown
										data[28:25] <= cmd_id;
										data[24:8] <= 0;
										data[7:0] <= cmd;
									end
								data_stb <= 1;
								cmd_id <= cmd_id + 1;
							end
				  end
					`STATE_RESET_2: begin
						if (!sync_spi_cs)
							begin
								state <= `STATE_CMD_0;
								if (sync_spi_clk)
									state <= `STATE_CMD_1;
									
								addr <= 0;
								cmd <= 0;
								byte_cnt <= 0;
								bit_cnt <= 0;
							end
					end
					`STATE_CMD_0: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_1;
						else if (sync_spi_clk)
							begin
								cmd <= next_cmd;
								bit_cnt <= bit_cnt + 1;
								state <= `STATE_CMD_1;
								if (bit_cnt == 7)
									begin
										if (next_cmd == 3)
											begin
												state <= `STATE_ADDR_1;
												bit_cnt <= 0;
											end
										else
											state <= `STATE_UNKNOWN;
									end
							end
					end
					`STATE_CMD_1: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_1;
						else if (!sync_spi_clk)
							state <= `STATE_CMD_0;
					end
					`STATE_ADDR_0: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_1;
						else if (sync_spi_clk)
							begin
								addr <= next_addr;
								bit_cnt <= bit_cnt + 1;
								state <= `STATE_ADDR_1;
								if (bit_cnt == 21)
									addr_hi <= next_addr[21:0];
								if (bit_cnt == 23)
									begin
										state <= `STATE_DATA_1;
										bit_cnt <= 0;
										byte_cnt <= 0;
										addr_lo <= next_addr[1:0];
									end
							end
					end
					`STATE_ADDR_1: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_1;
						else if (!sync_spi_clk)
							state <= `STATE_ADDR_0;
					end
					`STATE_DATA_0: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_1;
						else if (sync_spi_clk)
							begin
								state <= `STATE_DATA_1;
								if (bit_cnt == 7)
									begin
										bit_cnt <= 0;
										byte_cnt <= byte_cnt + 1;
										addr_hi <= next_addr2[23:2];
										addr_lo <= next_addr2[1:0];
									end
								else
									bit_cnt <= bit_cnt + 1;
							end
					end
					`STATE_DATA_1: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_1;
						else if (!sync_spi_clk)
							begin
								state <= `STATE_DATA_0;
								if (bit_cnt == 0)
									load <= 1;
								else
									shift <= 1;
							end
					end
					`STATE_UNKNOWN: begin
						if (sync_spi_cs)
							state <= `STATE_RESET_1;
					end

				endcase
			end
endmodule
