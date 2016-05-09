/*
6) POLYNOMIAL UNOPTIMISED: (n1=12,m=16, 1 Var)
   Original: 40960*x^4+20994*x^3+63371*x^2+16384*x+1277
   Reduced:  4610*x^3+6027*x^2+1277
   Vanishing: 40960*x^4+16384*x^3+57344*x^2+16384*x
*/

module foo(x,z);
	input [11:0] x;
	wire [15:0] f;
	wire [15:0] g;

	assign f=40960*x*x*x*x+20994*x*x*x+63371*x*x+16384*x+1277;
	assign g=4610*x*x*x+6027*x*x+1277;
	oldmiter(f,g);

endmodule
