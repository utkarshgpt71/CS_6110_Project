/*
10) Anti-alias filter:(n1=11,m=16, 1 Var,Scaled *10^4)
    Original: 156*c^6+62724*c^5+17968*c^4+18661*c^3+43593*c^2+40224*c+13281
    Mid: 156*c^6+5380*c^5+1584*c^4+43237*c^3+27209*c^2+40224*c+13281
    Reduced: 156*c^6+5380*c^5+1584*c^4+10469*c^3+27209*c^2+7456*c+13281
    Vanishing: 57344*c^5+16384*c^4+8192*c^3+16384*c^2+32768*c
*/

module foo();
	wire [10:0] c;
	wire [15:0] f;
	wire [15:0] g;
	
	assign f=156*c*c*c*c*c*c+62724*c*c*c*c*c+17968*c*c*c*c+18661*c*c*c+43593*c*c+40224*c+13281;
	assign g=156*c*c*c*c*c*c+5380*c*c*c*c*c+1584*c*c*c*c+10469*c*c*c+27209*c*c+7456*c+13281;
	oldmiter(f,g);
endmodule
