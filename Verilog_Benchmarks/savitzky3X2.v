module poly3X2 ();

input [15:0] x, y;

output [15:0] f1 = 16*x*x + 16*y*y + 25*x*y - 16*x - 16*y - 11;
output [15:0] g1 = 16*(x*x + y*y  - x - y) + 25*x*y - 11;
oldmiter(f1,g1);

//output [15:0] f2 = -33*x*x + 16*y*y  - 16*y + 22;
//output [15:0] g2 = -33*x*x + 16*y*(y  - 1) + 22;
//oldmiter(f2,g2);

//output [15:0] f3 = 16*x*x + 16*y*y - 25*x*y + 16*x - 16*y - 11;
//output [15:0] g3 = 16*(x*x + y*y  + x - y) - 25*x*y - 11;

//output [15:0] f4 = 16*x*x - 33*y*y  - 16*x + 22;
//output [15:0] g4 = 16*x*(x   - 1) - 33*y*y + 22;

//output [15:0] f5 = -33*x*x - 33*y*y  + 55;
//output [15:0] g5 = -33*(x*x + y*y)  + 55;

//output [15:0] f6 = 16*x*x - 33*y*y  + 16*x + 22;
//output [15:0] g6 = 16*x*(x   + 1) - 33*y*y + 22;

//output [15:0] f7 = 16*x*x + 16*y*y - 25*x*y - 16*x + 16*y - 11;
//output [15:0] g7 = 16*(x*x + y*y  - x + y) - 25*x*y - 11;

//output [15:0] f8 = -33*x*x + 16*y*y  + 16*y + 22;
//output [15:0] g8 = -33*x*x + 16*y*(y  + 1) + 22;

//output [15:0] f9 = 16*x*x + 16*y*y + 25*x*y + 16*x + 16*y - 11;
//output [15:0] g9 = 16*(x*x + y*y  + x + y) + 25*x*y - 11;

endmodule
