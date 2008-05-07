`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    22:55:29 04/16/2008 
// Design Name: 
// Module Name:    wr_fifo_read_ctrl 
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
module wr_fifo_read_ctrl(
	clk,
	reset,
	dram_req,
	dram_ack,
	dram_addr,
	dram_we,
	dram_data,
	sniffer_data,
	sniffer_data_stb,
	trigger,
	wr_en,
	rd_addr,
	rd_addr_changed
	);

	input clk;
	input reset;
	output dram_req;
	input dram_ack;
	output [23:0] dram_addr;
	output dram_we;
	output [31:0] dram_data;
	input [63:0] sniffer_data;
	input sniffer_data_stb;
	input trigger;
	output wr_en;
	input [21:0] rd_addr;
	input rd_addr_changed;

	reg dram_req;
	reg fifo_rd;

	reg [4:0] state;
	reg [23:0] wr_addr;
	reg [23:0] dram_addr;
	reg [31:0] dram_data;
	reg wr_en;
	reg dram_we;
	
	reg trigger_req;
	reg rd_req;
	reg sniffer_req;
	
	`define STATE_DISPATCH 		0
	`define STATE_WR_WAIT_1 	1
	`define STATE_WR_START_2 	2
	`define STATE_WR_WAIT_2 	3
	`define STATE_RD_WAIT 		4
	 
	always @(posedge clk)
		if (reset)
			begin
				dram_req <= 0;
				dram_addr <= 0;
				dram_we <= 0;
				dram_data <= 0;
				
				fifo_rd <= 0;
				wr_en <= 0;
				wr_addr <= 0;

				state <= `STATE_DISPATCH;
				
				trigger_req <= 0;
				rd_req <= 0;
				sniffer_req <= 0;
			end
		else
			begin
				fifo_rd <= 0;
				if (!wr_en && trigger)
					trigger_req <= 1;
					
				if (rd_addr_changed)
					rd_req <= 1;

				if (sniffer_data_stb)
					sniffer_req <= 1;
					
				case (state)
					`STATE_DISPATCH: begin
						if (rd_req)
							begin
								rd_req <= 0;
								dram_req <= 1;
								dram_we <= 0;
								dram_addr <= 24'h600000 | rd_addr;
								state <= `STATE_RD_WAIT;
							end
						if (trigger_req)
							begin
								wr_addr <= 0;
								wr_en <= 1;
								trigger_req <= 0;
							end
						else if (sniffer_req)
							begin
								sniffer_req <= 0;
								if (wr_en)
									begin
										dram_req <= 1;
										dram_we <= 1;
										dram_addr <= wr_addr;
										dram_data <= sniffer_data[63:32];
										state <= `STATE_WR_WAIT_1;
									end
							end
					end
					`STATE_WR_WAIT_1: begin
						if (dram_ack)
							begin
								dram_req <= 0;
								dram_we <= 0;
								dram_addr <= 0;
								state <= `STATE_WR_START_2;
								wr_addr <= wr_addr + 1;
							end
					end
					`STATE_WR_START_2: begin
						dram_req <= 1;
						dram_we <= 1;
						dram_addr <= wr_addr;
						dram_data <= sniffer_data[31:0];
						state <= `STATE_WR_WAIT_2;
					end
					`STATE_WR_WAIT_2: begin
						if (dram_ack)
							begin
								dram_req <= 0;
								dram_we <= 0;
								dram_addr <= 0;
								state <= `STATE_DISPATCH;
								if (wr_addr == 24'h5FFF00)
									wr_en <= 0;
								else
									wr_addr <= wr_addr + 1;
							end
					end
					`STATE_RD_WAIT: begin
						if (dram_ack)
							begin
								dram_req <= 0;
								dram_we <= 0;
								dram_addr <= 0;
								state <= `STATE_DISPATCH;
							end
					end
				endcase
			end
endmodule
