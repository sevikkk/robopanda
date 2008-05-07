`timescale 1ns / 1ps

////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer:
//
// Create Date:   10:22:09 05/06/2008
// Design Name:   wr_fifo_read_ctrl
// Module Name:   C:/xilinx/vga/test_wr_fifo_read_ctrl.v
// Project Name:  vga
// Target Device:  
// Tool versions:  
// Description: 
//
// Verilog Test Fixture created by ISE for module: wr_fifo_read_ctrl
//
// Dependencies:
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
////////////////////////////////////////////////////////////////////////////////

module test_wr_fifo_read_ctrl;

	// Inputs
	reg clk;
	reg reset;
	reg trigger;
	reg dram_ack;
	
	reg spi_cs;
	reg spi_clk;
	reg spi_si;
	reg spi_so;

	// Outputs
	wire dram_req;
	wire [23:0] dram_addr;
	wire dram_we;
	wire [31:0] dram_data;
	wire [1:0] addr_lo;
	wire load;
	wire shift;

	// Internal wires
	wire rd_addr_changed;
	wire [63:0] sniffer_data;
	wire sniffer_data_stb;
	wire [21:0] rd_addr;
	wire enable;
	
	reg [31:0] dram_odata;

	wr_fifo_read_ctrl uut_ctrl (
		.clk(clk), 
		.reset(reset), 
		.dram_req(dram_req), 
		.dram_ack(dram_ack), 
		.dram_addr(dram_addr), 
		.dram_we(dram_we), 
		.dram_data(dram_data), 
		.sniffer_data(sniffer_data), 
		.sniffer_data_stb(sniffer_data_stb), 
		.trigger(trigger), 
		.wr_en(enable), 
		.rd_addr(rd_addr), 
		.rd_addr_changed(rd_addr_changed)
	);

	spi_sniffer uut_sniffer (
		.spi_cs(spi_cs), 
		.spi_clk(spi_clk), 
		.spi_si(spi_si), 
		.spi_so(spi_so), 
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
	
	// Clock
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
	
	initial begin
		// Initialize Inputs
		spi_cs = 0;
		spi_clk = 0;
		spi_si = 0;
		spi_so = 0;
		reset = 0;
		dram_ack <= 0;
		dram_cnt <= 0;
		// Wait 100 ns for global reset to finish
		#100;
		
		// Add stimulus here
		reset = 1;

		#124;
		reset = 0;
		
		#120;
		trigger = 1;

		#120;
		trigger = 0;
		
		#120;

`include "tb.v"
	end
	
	reg [4:0] dram_cnt;
	always @(posedge clk)
		begin
			dram_ack <= 0;
			if (dram_req)
				begin
					if (dram_cnt == 0)
						dram_cnt <= 12;
					else if (dram_cnt == 2 && dram_we == 0)
						begin
							dram_odata <= 0;
							case ((dram_addr - 24'h600000) << 2)
								24'h00000: dram_odata <= 32'h2000BBCC;
								24'h02000: dram_odata <= 32'h89230000;
								24'h13244: dram_odata <= 32'h00020000;
								24'h02004: dram_odata <= 32'h000c6477;
								24'h02008: dram_odata <= 32'h01aa63cb;
								24'h0e8ec: dram_odata <= 32'h000001A1;
								24'h0e794: dram_odata <= 32'hc0950000;
							endcase
							dram_cnt <= dram_cnt - 1;
						end
					else if (dram_cnt == 1)
						begin
							dram_cnt <= 0;
							dram_ack <= 1;
						end
					else
						dram_cnt <= dram_cnt - 1;
				end
		end
		
	reg [7:0] shift_reg;
	wire so;

	always @(posedge clk)
		begin
			if (load)
				begin
					shift_reg <= 0;
					case (addr_lo)
						0: shift_reg <= dram_odata[7:0];
						1: shift_reg <= dram_odata[15:8];
						2: shift_reg <= dram_odata[23:16];
						3: shift_reg <= dram_odata[31:24];
					endcase
				end
			if (shift)
				shift_reg <= shift_reg << 1;
		end
	
	assign so = shift_reg[7];

endmodule

