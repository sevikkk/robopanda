`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    03:34:35 04/01/2008 
// Design Name: 
// Module Name:    vga_sync_gen 
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
module vga_sync_gen(clk, reset, hsync, vsync, active, x, y, load, next_addr, reset_addr);
    input clk;
    input reset;
    output hsync;
    output vsync;
    output active;
    output [10:0] x;
    output [10:0] y;
    output load;
    output next_addr;
    output reset_addr;
	 
	 reg [10:0] CounterX;
	 reg [10:0] CounterY;
	 wire CounterXmaxed = (CounterX==11'h2FF);
	 
	 reg vga_HS, vga_VS;
	 reg activeX, activeY;
	 reg load, next_addr, reset_addr;
		
always @(posedge clk)
begin
   if (reset == 1) 
	   begin
		   CounterX <= 0;
			CounterY <= 0;
      	vga_HS <= 1'h0;
      	vga_VS <= 1'h0;
	      activeX <= 1'h1;
	      activeY <= 1'h1;
      	load <= 1'h0;
      	next_addr <= 1'h0;
      	reset_addr <= 1'h0;
		end
	else
	   begin
	      if (CounterX == 1032)
	      	vga_HS <= 1'h1;
      
	      if (CounterX == 1152)
		      vga_HS <= 1'h0;

	      if (CounterY == 784)
		      vga_VS <= 1'h1;

	      if (CounterX == 787)
		      vga_VS <= 1'h0;
				
			if (CounterX[4:0] == 31 && activeX && activeY)
			   load <= 1;

			if (CounterX[4:0] == 0 && activeX && activeY)
			   next_addr <= 1;
				
			if (load)
			   load <= 0;
			   
	      if (CounterX == 1360)
		      begin
			      CounterX <= 0;
			      activeX <= 1;
			      load <= 1;
		         if (CounterY == 823)
			         begin
					      CounterY <= 0;
					      activeY <= 1;
				      end
			      else
					  begin
	                if (CounterY == 767)
			             begin
		                  activeY <= 0;
			            	reset_addr <= 1;
			             end

				       CounterY <= CounterY + 1;
					  end
		      end
	      else
		      CounterX <= CounterX + 1;

			if (reset_addr)
			  begin
			   reset_addr <= 0;
			  end

			if (next_addr)
			  begin
			   next_addr <= 0;
			  end

	      if (CounterX == 1023)
		      activeX <= 0;
		end
end

assign active = activeX && activeY;
assign hsync = ~vga_HS;
assign vsync = ~vga_VS;
assign x = CounterX;
assign y = CounterY;

endmodule
