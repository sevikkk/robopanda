`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    23:55:36 04/15/2008 
// Design Name: 
// Module Name:    wr_addr_ctrl 
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
module wr_addr_ctrl(
    clk,
    reset,
    ce,
    addr
    );

    input clk;
    input reset;
    input ce;
    output [23:0] addr;
	 
    reg [4:0] addrX;
    reg [9:0] addrY;
	 
	 
	 always @(posedge clk)
		  if (reset)
		    begin
			    addrX <= 0;
				 addrY <= 0;
			 end
		  else
		    if (ce)
			   if (addrY==767)
					  begin
					     addrY <= 0;
						  if (addrX == 31)
						     addrX <= 0;
						  else
						     addrX <= addrX + 1;
					  end
				else
					  addrY <= addrY + 1;
					    
	assign addr[4:0] = addrX;
	assign addr[14:5] = addrY;
	assign addr[23:15] = 0;
	
endmodule
