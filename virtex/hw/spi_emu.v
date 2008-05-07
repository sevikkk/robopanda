`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    12:04:19 05/06/2008 
// Design Name: 
// Module Name:    spi_emu 
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
	module spi_emu(
		input clk,
		input reset,
		input trigger,
		input spi_cs,
		input spi_clk,
		input spi_si,
		input spi_so_sniffer,
		output spi_so,
		output dram_req,
		output [23:0] dram_addr,
		output dram_we,
		output [31:0] dram_odata,
		input [31:0] dram_idata,
		input dram_ack,
		output enable
	);

	wire rd_addr_changed;
	wire [63:0] sniffer_data;
	wire sniffer_data_stb;
	wire [21:0] rd_addr;
	
	wire [1:0] addr_lo;
	wire load;
	wire shift;

	wr_fifo_read_ctrl ctrl (
		.clk(clk), 
		.reset(reset), 
		.dram_req(dram_req), 
		.dram_ack(dram_ack), 
		.dram_addr(dram_addr), 
		.dram_we(dram_we), 
		.dram_data(dram_odata), 
		.sniffer_data(sniffer_data), 
		.sniffer_data_stb(sniffer_data_stb), 
		.trigger(trigger), 
		.wr_en(enable), 
		.rd_addr(rd_addr), 
		.rd_addr_changed(rd_addr_changed)
	);

	spi_sniffer sniffer (
		.spi_cs(spi_cs), 
		.spi_clk(spi_clk), 
		.spi_si(spi_si), 
		.spi_so(spi_so_sniffer), 
		.clk(clk), 
		.reset(reset), 
		.data(sniffer_data), 
		.data_stb(sniffer_data_stb), 
		.enable(enable),
		.addr_hi(rd_addr),
		.addr_lo(addr_lo),
		.addr_changed(rd_addr_changed),
		.load(load),
		.shift(shift)
	);

	reg [7:0] shift_reg;

	always @(posedge clk)
		begin
			if (load)
				begin
					case (addr_lo)
						0: shift_reg <= dram_idata[7:0];
						1: shift_reg <= dram_idata[15:8];
						2: shift_reg <= dram_idata[23:16];
						3: shift_reg <= dram_idata[31:24];
					endcase
				end
			else if (shift)
				shift_reg <= shift_reg << 1;
		end
	
	assign spi_so = shift_reg[7];
	
endmodule
