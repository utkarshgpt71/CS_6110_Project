/*
8) Janez's filter(n1=12,m=16, 1 Var: H(z) numerator scaled *1000)
   Original:  19666*x^4+38886*x^3+16667*x^2+52202*x+1 
   Mid:  3282*x^4+6118*x^3+33051*x^2+19434*x+1
   Reduced:  3282*x^4+6118*x^3+283*x^2+52202*x+1
   Vanishing: 16384*x^4+32768*x^3+16384*x^2
*/

module foo();
	wire [11:0] x;
	wire [15:0] f;
	wire [15:0] g;
	assign f=19666*x*x*x*x+38886*x*x*x+16667*x*x+52202*x+1;
	assign g=3282*x*x*x*x+6118*x*x*x+283*x*x+52202*x+1;
	oldmiter(f,g);
endmodule
