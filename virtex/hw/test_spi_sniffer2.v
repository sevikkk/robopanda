`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   21:29:48 05/03/2008
// Design Name:   spi_sniffer
// Module Name:   C:/xilinx/vga/test_spi_sniffer2.v
// Project Name:  vga
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: spi_sniffer
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module test_spi_sniffer2;

	// Inputs
	reg spi_cs;
	reg spi_clk;
	reg spi_si;
	reg spi_so;
	reg clk;
	reg reset;
	reg enable;

	// Outputs
	wire [31:0] data;
	wire data_stb;
	
	wire [21:0] addr_hi;
	wire [1:0] addr_lo;
	wire addr_changed;
	wire load;
	wire shift;

	// Instantiate the Unit Under Test (UUT)
	spi_sniffer uut (
		.spi_cs(spi_cs), 
		.spi_clk(spi_clk), 
		.spi_si(spi_si), 
		.spi_so(spi_so), 
		.clk(clk), 
		.reset(reset), 
		.data(data), 
		.data_stb(data_stb), 
		.enable(enable),
		.addr_hi(addr_hi),
		.addr_lo(addr_lo),
		.addr_changed(addr_changed),
		.load(load),
		.shift(shift)
	);

	parameter PERIOD = 12;
	parameter real DUTY_CYCLE = 0.5;
	parameter OFFSET = 100;

	initial    // Clock process for clk
		begin
			#OFFSET;
			forever
				begin
					clk = 1'b0;
					#(PERIOD-(PERIOD*DUTY_CYCLE)) clk = 1'b1;
					#(PERIOD*DUTY_CYCLE);
				end
		end
		
	reg [7:0] shift_reg;
	always @(posedge clk)
		begin
			if (load)
				begin
					shift_reg <= 0;
					case (addr_hi <<2 | addr_lo)
						0: shift_reg <= 8'hCC;
						1: shift_reg <= 8'hBB;
						2: shift_reg <= 8'h00;
						3: shift_reg <= 8'h20;
						24'h2002: shift_reg <= 8'h23;
						24'h2003: shift_reg <= 8'h89;
						24'h13246: shift_reg <= 8'h02;
						24'h13247: shift_reg <= 8'h00;
						24'h2004: shift_reg <= 8'h77;
						24'h2005: shift_reg <= 8'h64;
						24'h2006: shift_reg <= 8'h0c;
						24'h2007: shift_reg <= 8'h00;
						24'h2008: shift_reg <= 8'hcb;
						24'h2009: shift_reg <= 8'h63;
						24'h200A: shift_reg <= 8'hAA;
						24'h200B: shift_reg <= 8'h01;
						24'he8ec: shift_reg <= 8'hA1;
						24'he8ed: shift_reg <= 8'h01;
						24'he796: shift_reg <= 8'h95;
						24'he797: shift_reg <= 8'hc0;
					endcase
				end
			if (shift)
				shift_reg <= shift_reg << 1;
		end
	wire so;
	
	assign so = shift_reg[7];

	initial begin
		// Initialize Inputs
		spi_cs = 0;
		spi_clk = 0;
		spi_si = 0;
		spi_so = 0;
		reset = 0;
		enable = 0;

		// Wait 100 ns for global reset to finish
		#100;
		
		// Add stimulus here
		reset = 1;

		#124;
		reset = 0;
		
		#120;
		enable = 1;

`include "tb.v"
	end
      
endmodule

