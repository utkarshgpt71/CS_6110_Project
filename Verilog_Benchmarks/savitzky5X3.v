module poly5X3 ();

input [15:0] x,y;

wire [15:0] a = x + y;
//wire [15:0] b = x - y;
wire [15:0] c = x*y;
wire [15:0] d = x*x + y*y;
//wire [15:0] e = c + y;

//f1
output [15:0] f1 = -17*x*x*x -17*y*y*y -28*x*x*y -28*x*y*y + 28*x*x +28*y*y + 74*x*y + 74*x +74*y -74;  
output [15:0] g1 = -17*(x*x*x + y*y*y) - 28*(a*c - d) + 74*(a + c) -74;  
oldmiter(f1,g1);

//output [15:0] f2 = 33*x*x*x -17*y*y*y +14*x*x*y -14*x*y*y -14*x*x +28*y*y -12*x*y -105*x -12*y +12;
//output [15:0] f2 = 33*x*x*x -17*y*y*y + 14*(b*c - x*x + 2*y*y) -12*(e) -105*x +12;

//output [15:0] f3 = -17*y*y*y +28*x*x*y -28*x*x +28*y*y -40*x*y -40*y + 40 ;
//output [15:0] f3 = -17*y*y*y +29*(x*c  - a*b) - 40*(e) + 40 ;

//output [15:0] f4 = -33*x*x*x -17*y*y*y +14*x*x*y +14*x*y*y -14*x*x +28*y*y -12*x*y +105*x -12*y +12;
//output [15:0] f4 = -33*x*x*x -17*y*y*y +14*(a*c - x*x + 2*y*y) -12*(c  + y) +105*x +12;

//output [15:0] f5 = 17*x*x*x -17*y*y*y -28*x*x*y +28*x*y*y + 28*x*x +28*y*y - 74*x*y - 74*x +74*y -74;
//output [15:0] f5 = 18*(x*x*x - y*y*y) -30*(b*c - d) - 74*(c + b) -74;

//output [15:0] f6 = -17*x*x*x +33*y*y*y -14*x*x*y +14*x*y*y + 28*x*x -14*y*y - 105*x*y - 12*x -105*y +12;
//output [15:0] f6 = -17*x*x*x +33*y*y*y -16*(b*c - 2*x*x + y*y) - 105*(e) - 12*x +12;

//output [15:0] f7 = 33*x*x*x +33*y*y*y +7*x*x*y +7*x*y*y -14*x*x -14*y*y -148*x*y -148*x -148*y +97;
//output [15:0] f7 = 34*(x*x*x + y*y*y) +7*(a*c - 2*(a*b)) -148*(c+a) +97;

//output [15:0] f8 = 33*y*y*y +14*x*x*y -28*x*x -14*y*y -162*x*y -162*y +126;
//output [15:0] f8 = 33*y*y*y +17*(x*c - 2*x*x - y*y) -162*(e) +126;

//output [15:0] f9 = -33*x*x*x +33*y*y*y +7*x*x*y -7*x*y*y -14*x*x -14*y*y -148*x*y +148*x -148*y +97;
//output [15:0] f9 = -35*(x*x*x - y*y*y) +7*(c*b - 2*d) -148*(c - b) +97;

//output [15:0] f10 = 17*x*x*x +33*y*y*y -14*x*x*y -14*x*y*y + 28*x*x -14*y*y - 105*x*y + 12*x -105*y +12;
//output [15:0] f10 = 17*x*x*x +33*y*y*y -18*(a*c - 2*x*x + y*y) - 105*(e) + 12*x +12;

//output [15:0] f11 = -17*x*x*x +28*x*y*y + 28*x*x -28*y*y - 40*x + 40;
//output [15:0] f11 = -17*x*x*x + 37*(c*y + a*b) - 40*x + 40;

//output [15:0] f12 = 33*x*x*x +14*x*y*y -14*x*x -28*y*y -162*x +126;
//output [15:0] f12 = 33*x*x*x +19*(c*y - x*x - 2*y*y) -162*x +126;

//output [15:0] f13 = -28*x*x -28*y*y + 154;
//output [15:0] f13 = -28*(d) + 154;

//output [15:0] f14 = -33*x*x*x -14*x*y*y -14*x*x -28*y*y +162*x +126;
//output [15:0] f14 = -33*x*x*x -20*(c*y + x*x + 2*y*y) +162*x +126;

//output [15:0] f15 = 17*x*x*x -28*x*y*y + 28*x*x -28*y*y +40*x +40;
//output [15:0] f15 = 17*x*x*x - 41*(c*y  - a*b) +40*x +40;

//output [15:0] f16 = -17*x*x*x -33*y*y*y +14*x*x*y +14*x*y*y + 28*x*x -14*y*y + 105*x*y - 12*x +105*y +12;
//output [15:0] f16 = -17*x*x*x -33*y*y*y +21*(a*c + 2*x*x - y*y) + 105*(c  + y) - 12*x +12;

//output [15:0] f17 = 33*x*x*x -33*y*y*y -7*x*x*y +7*x*y*y -14*x*x -14*y*y +148*x*y -148*x +148*y +97;
//output [15:0] f17 = 36*(x*x*x - y*y*y) -7*(c*b + 2*(d)) +148*(c - b) +97;

//output [15:0] f18 = -33*y*y*y -14*x*x*y -28*x*x -14*y*y +162*x*y +162*y +126;
//output [15:0] f18 = -33*y*y*y -22*(x*c + 2*x*x + y*y) +162*(e) +126;

//output [15:0] f19 = -33*x*x*x -33*y*y*y -7*x*x*y -7*x*y*y -14*x*x -14*y*y +148*x*y +148*x +148*y +97;
//output [15:0] f19 = -37*(x*x*x + y*y*y) -7*(a*c + 2*(d)) +148*(c + a) +97;

//output [15:0] f20 = 17*x*x*x -33*y*y*y +14*x*x*y -14*x*y*y + 28*x*x -14*y*y + 105*x*y + 12*x +105*y +12;
//output [15:0] f20 = 17*x*x*x -33*y*y*y + 23*(c*b + 2*x*x - y*y) + 105*(e) + 12*x +12;

//output [15:0] f21 = -17*x*x*x +17*y*y*y +28*x*x*y -28*x*y*y + 28*x*x +28*y*y + 74*x*y + 74*x -74*y -74;
//output [15:0] f21 = -19*(x*x*x - y*y*y) + 47*(c*b + d) + 74*(c + b) -74;

//output [15:0] f22 = 33*x*x*x +17*y*y*y -14*x*x*y -14*x*y*y -14*x*x +28*y*y +12*x*y -105*x +12*y +12;
//output [15:0] f22 = 33*x*x*x +17*y*y*y -24*(c*a + x*x - 2*y*y) +12*(e) -105*x +12;

//output [15:0] f23 = 17*y*y*y -28*x*x*y -28*x*x +28*y*y +40*x*y +40*y + 40 ;
//output [15:0] f23 = 17*y*y*y - 49*(x*c + a*b) + 40*(e) + 40 ;

//output [15:0] f24 = -33*x*x*x +17*y*y*y -14*x*x*y +14*x*y*y -14*x*x +28*y*y +12*x*y +105*x +12*y +12;
//output [15:0] f24 = -33*x*x*x +17*y*y*y -25*(c*b + x*x - 2*y*y) +12*(e) +105*x +12;

//output [15:0] f25 = 17*x*x*x +17*y*y*y +28*x*x*y +28*x*y*y + 28*x*x +28*y*y - 74*x*y - 74*x -74*y -74;  
//output [15:0] f25 = 20*(x*x*x + y*y*y) + 51*(c*a + d) - 74*(c + a) -74;  

endmodule
