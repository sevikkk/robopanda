`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    00:38:52 04/22/2008 
// Design Name: 
// Module Name:    tx_fifo_ctrl 
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
module tx_fifo_ctrl(
    clk,
    reset,
    fifo_empty,
    tx_buf_empty,
    fifo_rd,
    tx_load
    );

    input clk;
    input reset;
    input fifo_empty;
    input tx_buf_empty;
    output fifo_rd;
    output tx_load;
	 
	 reg tx_load;
	 reg fifo_rd;
	 
	 reg [1:0] state;
	 
	 always @(posedge clk)
	   if (reset)
		  begin
		    tx_load <= 0;
			 fifo_rd <= 0;
			 state <= 0;
		  end
		else
        case (state) 
			 0: begin
			      if (!fifo_empty)
					  begin
					    fifo_rd <= 1;
						 state <= 1;
					  end
			    end
			 1: begin
			      fifo_rd <= 0;
					tx_load <= 1;
					state <= 2;
				 end
			 2: begin
					tx_load <= 0;
					state <= 3;
				 end
			 3: begin
			      if (tx_buf_empty)
					  begin
						 state <= 0;
					  end
				 end
		  endcase


endmodule
