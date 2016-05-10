module poly4X3 ();

input [15:0] x,y;
output [15:0] f1;
output [15:0] g1;

wire [15:0] a;
//wire [15:0] b = x - y;
wire [15:0] c;
wire [15:0] d;
//wire [15:0] e = x + 3*y;
//wire [15:0] f = x - 3*y;
//wire [15:0] g = 3*x + y;
//wire [15:0] h = 3*x - y;
//wire [15:0] i = a*b;
wire [15:0] j ;
//wire [15:0] k = c*b; 
//wire [15:0] m = c*e;
//wire [15:0] n = c*f;
//wire [15:0] p = c*g;
//wire [15:0] q = c*h;
wire [15:0] r;

assign a = x + y; 
assign c = x*y;
assign d = x*x + y*y;
assign j = c*a;
assign r = 30*c;
assign f1 = -42*x*x*x -42*y*y*y -75*x*x*y -75*x*y*y + 63*x*x +63*y*y + 90*x*y+104*x +104*y -94;  
assign g1 = -42*(x*x*x + y*y*y) - 75*(j) + 63*(d) + 3*r + 104*(a) -94;  
oldmiter(f1,g1);

//output [15:0] f2 = 125*x*x*x -42*y*y*y +75*x*x*y -25*x*y*y - 63*x*x +63*y*y + 30*x*y-250*x -84*y -63;
//output [15:0] g2 = 25*(5*x*(x*x - 2) + q) - 64*(i)  -42*(y*y*y + 2*y) + r -63;

//output [15:0] f3 = -125*x*x*x -42*y*y*y +75*x*x*y +25*x*y*y - 63*x*x +63*y*y - 30*x*y+250*x -84*y -63;
//output [15:0] g3 = -25*(5*x*(x*x + 2)  - p) - 65*(i) - r -42*(y*y*y - 2*y) -63;

//output [15:0] f4 = 42*x*x*x -42*y*y*y -75*x*x*y +75*x*y*y + 63*x*x +63*y*y - 90*x*y-104*x +104*y -94;
//output [15:0] g4 = 42*(x*x*x - y*y*y) - 75*k + 66*(d) - 3*r - 104*(b) -94;

//output [15:0] f5 = -42*x*x*x +125*y*y*y -25*x*x*y +75*x*y*y + 63*x*x -63*y*y +30*x*y-84*x -250*y +63;
//output [15:0] g5 = 25*(5*y*(y*y - 2) - n) + 67*(i) + r  -42*(x*x*x + 2*x)  +63;

//output [15:0] f6 = 125*x*x*x +125*y*y*y +25*x*x*y +25*x*y*y - 63*x*x -63*y*y + 10*x*y-313*x -313*y +219;
//output [15:0] g6 = 25*(5*(x*x*x + y*y*y) + j) - 68*(d) + 10*c -313*(a) +219;

//output [15:0] f7 = -125*x*x*x +125*y*y*y +25*x*x*y -25*x*y*y - 63*x*x -63*y*y - 10*x*y+313*x -313*y +219;
//output [15:0] g7 = -25*(5*(x*x*x - y*y*y) - k) - 69*(d) - 10*c + 313*(b) +219;

//output [15:0] f8 = 42*x*x*x +125*y*y*y -25*x*x*y -75*x*y*y + 63*x*x -63*y*y -30*x*y+84*x -250*y +63;
//output [15:0] g8 = 25*(5*y*(y*y - 2) - m) + 70*(i) - r  + 42*(x*x*x + 2*x)  +63;

//output [15:0] f9 = -42*x*x*x -125*y*y*y +25*x*x*y +75*x*y*y + 63*x*x -63*y*y -30*x*y-84*x +250*y +63;
//output [15:0] g9 = -25*(5*y*(y*y + 2) + m) + 71*(i) - r  -42*(x*x*x + 2*x)  +63;

//output [15:0] f10 = 125*x*x*x -125*y*y*y -25*x*x*y +25*x*y*y - 63*x*x -63*y*y - 10*x*y-313*x +313*y +219;
//output [15:0] g10 = 25*(5*(x*x*x - y*y*y) - k) - 72*(d) - 10*c - 313*(b) +219;

//output [15:0] f11 = -125*x*x*x -125*y*y*y -25*x*x*y -25*x*y*y - 63*x*x -63*y*y + 10*x*y+313*x +313*y +219;
//output [15:0] g11 = -25*(5*(x*x*x + y*y*y) + j) - 73*(d) + 10*c + 313*(a) +219;

//output [15:0] f12 = -42*x*x*x -125*y*y*y +25*x*x*y -75*x*y*y + 63*x*x -63*y*y +30*x*y+84*x +250*y +63;
//output [15:0] g12 = -25*(5*y*(y*y - 2) - n) + 74*(i) +r - 42*(x*x*x - 2*x) +63;

//output [15:0] f13 = -42*x*x*x +42*y*y*y +75*x*x*y -75*x*y*y + 63*x*x +63*y*y - 90*x*y+104*x -104*y -94;
//output [15:0] g13 = -42*(x*x*x - y*y*y) +75*(k) + 76*(d) - 3*r + 104*(b) -94;

//output [15:0] f14 = 125*x*x*x +42*y*y*y -75*x*x*y -25*x*y*y - 63*x*x +63*y*y - 30*x*y-250*x +84*y +63;
//output [15:0] g14 = 25*(5*x*(x*x -2) - p ) - 77*(i) - r + 42*(y*y*y +2*y) +63;

//output [15:0] f15 = -125*x*x*x +42*y*y*y -75*x*x*y +25*x*y*y - 63*x*x +63*y*y + 30*x*y+250*x +84*y +63;
//output [15:0] g15 = -25*(5*x*(x*x - 2)  + q ) - 78*(i) + r + 42*(y*y*y + 2*y) +63;

//output [15:0] f16 = 42*x*x*x +42*y*y*y +75*x*x*y +75*x*y*y + 63*x*x +63*y*y + 90*x*y-104*x -104*y -94;
//output [15:0] g16 = 42*(x*x*x + y*y*y) +75*(j) + 79*(d) + 3*r - 104*(a) -94;

endmodule
