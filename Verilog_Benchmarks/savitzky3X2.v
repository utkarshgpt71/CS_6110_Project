module poly3X2 ();

input [15:0] x, y;
output [15:0] f1;
output [15:0] g1;

assign f1 = 16*x*x + 16*y*y + 25*x*y - 16*x - 16*y - 11;
assign g1 = 16*(x*x + y*y  - x - y) + 25*x*y - 11;
oldmiter(f1,g1);

//assign f2 = -33*x*x + 16*y*y  - 16*y + 22;
//assign g2 = -33*x*x + 16*y*(y  - 1) + 22;
//oldmiter(f2,g2);

//assign f3 = 16*x*x + 16*y*y - 25*x*y + 16*x - 16*y - 11;
//assign g3 = 16*(x*x + y*y  + x - y) - 25*x*y - 11;

//assign f4 = 16*x*x - 33*y*y  - 16*x + 22;
//assign g4 = 16*x*(x   - 1) - 33*y*y + 22;

//assign f5 = -33*x*x - 33*y*y  + 55;
//assign g5 = -33*(x*x + y*y)  + 55;

//assign f6 = 16*x*x - 33*y*y  + 16*x + 22;
//assign g6 = 16*x*(x   + 1) - 33*y*y + 22;

//assign f7 = 16*x*x + 16*y*y - 25*x*y - 16*x + 16*y - 11;
//assign g7 = 16*(x*x + y*y  - x + y) - 25*x*y - 11;

//assign f8 = -33*x*x + 16*y*y  + 16*y + 22;
//assign g8 = -33*x*x + 16*y*(y  + 1) + 22;

//assign f9 = 16*x*x + 16*y*y + 25*x*y + 16*x + 16*y - 11;
//assign g9 = 16*(x*x + y*y  + x + y) + 25*x*y - 11;

endmodule
