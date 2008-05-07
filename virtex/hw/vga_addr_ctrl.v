`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    00:25:28 04/02/2008 
// Design Name: 
// Module Name:    vga_addr_ctrl 
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
module vga_addr_ctrl(clk, reset, next_addr, reset_addr, addr, req, ack);
    input clk;
    input reset;
    input next_addr;
    input reset_addr;
    output [23:0] addr;
    output req;
    input ack;

	 reg [23:0] addr;
	 reg req;

	 
always @(posedge clk)
begin
	if (reset == 1)
	  begin
		 addr <= 0;
		 req <= 0;
	  end
	else
	  begin
		 if (next_addr)
			 begin
				req <= 1;
				addr <= addr + 1;
			 end

		 if (reset_addr)
			 begin
				req <= 1;
				addr <= 0;
			 end

	    if (ack == 1)
				 req <= 0;
	  end
end
	 
endmodule
